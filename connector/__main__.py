#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import json
import time
import re
from .subnet import Subnet
from .group import Group
from .address import Address
from .pool import Pool
from . import helpers
import SOLIDserverRest

if len(sys.argv) < 9:
  print('Usage: connector IP_FMG IP_SOLIDserver adom fmg_user fmg_passwd ipam_user ipam_passwd')
  exit(1)

addresses = list()
pools = list()
subnets = list()
groups = list()

def main(argv):
  ip_FMG = sys.argv[1]
  ip_SOLIDserver = sys.argv[2]
  adom = sys.argv[3]
  fmg_user = sys.argv[4] 
  fmg_passwd = sys.argv[5]
  ipam_user = sys.argv[6]
  ipam_passwd = sys.argv[7]
  sync_delete = bool(int(sys.argv[8]))
  time_refresh = int(sys.argv[8]) * 60 # timer refresh
  helpers.api.debug('off')

  sync_FMG(ip_FMG, fmg_user, fmg_passwd, adom)

  while True:
    helpers.api.login(ip_FMG, fmg_user, fmg_passwd)
    helpers.logger.info("Connecting to SOLIDserver @ " + ip_SOLIDserver + " with user: " + ipam_user + " pass: " + ipam_passwd)
    con = SOLIDserverRest.SOLIDserverRest(ip_SOLIDserver)
    con.use_native_ssd(user=ipam_user, password=ipam_passwd)
    sync_subnet_group(con, adom, sync_delete)
    sync_addr(con, adom, sync_delete)
    sync_pool(con, adom, sync_delete)
    helpers.api.logout()
    time.sleep(time)

  return 0


def sync_FMG(ip_FMG, fmg_user, fmg_passwd, adom):
  """Sync state of FMG at the beginning of the program.
  It will filter subnets and pool with the comment param in FMG"""

  global subnets
  global pools
  global groups
  global addresses

  def subnets_pools(ipv6):
    status, data = helpers.firewall_table("adom/" + adom, ipv6=ipv6)
    for d in data:
      if 'comment' in d and d['comment'] == "Created by EfficientIP":
        helpers.logger.debug(json.dumps(d, indent=2))
        m = re.split('[_|-]', d['name'])
        if d['type'] == 0:
          if ipv6:
            ip = re.split('[/]', d['ip6'])
            if ip[1] == '128':
              addresses.append(Address(m[1], ip[0], adom, ipv6=ipv6, _id=int(m[0]), parent=m[2] + '_' + m[3]))
            else:
              subnets.append(Subnet(m[1], ip[0], ip[1], adom, ipv6=ipv6, _id=int(m[0]), parent=m[2]))
          else:
            if d['subnet'][1] == '255.255.255.255':
              addresses.append(Address(m[1], d['subnet'][0], adom, ipv6=ipv6, _id=int(m[0]), parent=m[2] + '_' + m[3]))
            else:
              subnets.append(Subnet(m[1], d['subnet'][0], d['subnet'][1], adom, ipv6=ipv6, _id=int(m[0]), parent=m[2]))
        elif d['type'] == 1:
          pools.append(Pool(m[1], d['start-ip'], d['end-ip'], adom, ipv6=ipv6, _id=int(m[0]), parent=m[2] + '_' + m[3]))

  def group(ipv6):
    status, data = helpers.group_table("adom/" + adom, ipv6=ipv6)
    for d in data:
      if 'comment' in d and d['comment'] == "Created by EfficientIP":
        helpers.logger.debug(json.dumps(d, indent=2))
        m = re.split('[_|-]', d['name'])
        g = Group(m[1], adom, ipv6=ipv6, _id=int(m[0]))
        groups.append(g)

  helpers.api.login(ip_FMG, fmg_user, fmg_passwd)
  subnets_pools(False) # ipv4
  subnets_pools(True) # ipv6
  group(False) # ipv4
  group(True) # ipv6
  helpers.api.logout()
  time.sleep(1)

  return 0

def sync_subnet_group(con, adom, delete):
  rest_answer = con.query("ip_subnet_list", "", ssl_verify=False)
  if rest_answer.content is not None:
    blocks_v4 = json.loads(rest_answer.content.decode())

  rest_answer = con.query("ip_subnet6_list", "", ssl_verify=False)
  if rest_answer.content is not None:
    blocks_v6 = json.loads(rest_answer.content.decode())

  global subnets
  global groups
  current_subnets = list()
  current_groups = list()

  def loop(blocks, v6):
    if blocks is None:
      return
    _type = blocks[0]['type']
    for block in blocks:
      helpers.logger.debug(json.dumps(block, indent=2))
      if bool(int(block['is_in_orphan'])):
        continue
      if v6:
        netmask = block[_type+'_prefix']
      else:
        netmask = helpers.MAP_NETMASK_v4[block['subnet_size']]

      parent = block['parent_' + _type + '_name']
      name = block[_type + '_name']
      _id = block[_type + '_id']

      if bool(int(block['is_terminal'])):
        sub = Subnet(name, block['start_hostaddr'], netmask, adom, ipv6=v6, _id=_id, parent=parent)
        current_subnets.append(sub)
      else:
        grp = Group(name, adom, ipv6=v6, _id=_id, parent=parent)
        current_groups.append(grp)

  loop(blocks_v4, False)
  loop(blocks_v6, True)

  for s in current_subnets:
    for g in current_groups:
      if g.get_name() == s.get_parent() and g.is_ipv6() == s.is_ipv6():
        g.add_member(s)
    s.push_to_FMG()
    for x in subnets:
      if s.get_FMG_name() == x.get_FMG_name():
        subnets.remove(x)

  for g in current_groups:
    for g2 in current_groups:
      if g2.get_name() == g.get_parent() and g2.is_ipv6() == g.is_ipv6():
        g2.add_member(s)
    g.push_to_FMG()
    for x in groups:
      if g.get_FMG_name() == x.get_FMG_name():
        groups.remove(x)

  if delete:
    for g in groups:
      g.FMG_delete()
    for s in subnets:
      s.FMG_delete()

  subnets = current_subnets
  groups = current_groups

  return 0

def sync_addr(con, adom, delete):
  """Sync address object from SOLIDserver to FMG"""
  # fetch address from SOLIDserver
  rest_answer = con.query("ip_address_list", "", ssl_verify=False)
  if rest_answer.content is not None:
    addr_json = json.loads(rest_answer.content.decode())
  rest_answer = con.query("ip_address6_list", "", ssl_verify=False)
  if rest_answer.content is not None:
    addr6_json = json.loads(rest_answer.content.decode())
  helpers.logger.debug(json.dumps(addr_json, indent=2))
  helpers.logger.debug(json.dumps(addr6_json, indent=2))

  # old state on FMG
  global addresses
  current_addr = list()

  for a in addr_json:
    if a['type'] != 'ip':
      continue
    current_addr.append(Address(a['name'], a['hostaddr'], adom, _id=a['ip_id'], parent=a['subnet_name'] + '_' + a['parent_subnet_name']))

  for a in addr6_json:
    if a['type'] != 'ip6':
      continue
    current_addr.append(Address(a['ip6_name'], a['hostaddr'], adom, ipv6=True, _id=a['ip6_id'], parent=a['subnet6_name'] + '_' + a['parent_subnet6_name']))

  for a in current_addr:
    # push current SOLIDserver state to FMG with new subnet and update
    a.push_to_FMG()
    for x in addresses:
      if a.get_FMG_name() == x.get_FMG_name():
        # remove pushed subnet from old state
        addresses.remove(x)

  # addresses contains only deleted object from the last SOLIDserver state
  if delete: # delete option
    for a in addresses:
      a.FMG_delete()
  # save current state on FMG for next call
  addresses = current_addr

def sync_pool(con, adom, delete):
  """Sync pool object from SOLIDserver to FMG"""
  # fetch data from SOLIDserver
  rest_answer = con.query("ip_pool_list", "", ssl_verify=False)
  if rest_answer.content is not None:
    pool_json = json.loads(rest_answer.content.decode())
  
  global pools
  current_pool = list()

  for pool in pool_json:
    helpers.logger.debug(json.dumps(pool, indent=2))
    current_pool.append(Pool(pool['pool_name'], pool['start_hostaddr'], pool['end_hostaddr'], adom, _id=pool['pool_id'], parent=pool['subnet_name'] + '_' + pool['parent_subnet_name']))
  for p in current_pool:
    # push current state on FMG with new pools and update
    p.push_to_FMG()
    for x in pools:
      if p.get_FMG_name() == x.get_FMG_name():
        # remove pushed pools from old state
        pools.remove(x)

  # delete old object if option delete true
  if delete:
    for p in pools:
      p.FMG_delete()
  # save current state on FMG for next call
  pools = current_pool


if __name__ == "__main__":
  main(sys.argv)