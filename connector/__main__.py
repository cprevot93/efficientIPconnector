#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import json
from .subnet import Subnet
from .group import Group
from .address import Address
from . import helpers
import SOLIDserverRest

# if len(sys.argv) < 2:
#   print('Usage: ' + sys.argv[0] + 'IP <JSON API URL>')
#   exit(1)

def main(argv):
  ip_FMG = "100.68.99.10"
  ip_SOLIDserver = "100.68.99.20"
  fmg_user ='admin'
  fmg_passwd ='fortinet'
  adom = "root"
  ipam_user = "ipmadmin"
  ipam_passwd = "admin"
  helpers.api.login(ip_FMG, fmg_user, fmg_passwd)
  helpers.api.debug('off')

  con = SOLIDserverRest.SOLIDserverRest(ip_SOLIDserver)
  con.use_native_ssd(user=ipam_user, password=ipam_passwd)

  sync_subnet_group(con, adom)
  sync_addr(con, adom)
  helpers.api.logout()

  return 0


def sync_subnet_group(con, adom):
  rest_answer = con.query("ip_subnet_list", "", ssl_verify=False)
  if rest_answer.content is not None:
    blocks_v4 = json.loads(rest_answer.content.decode())

  rest_answer = con.query("ip_subnet6_list", "", ssl_verify=False)
  if rest_answer.content is not None:
    blocks_v6 = json.loads(rest_answer.content.decode())

  subnets = list()
  groups = list()

  def loop(blocks, v6):
    if blocks is None:
      return
    _type = blocks[0]['type']
    for block in blocks:
      if v6:
        netmask = block[_type+'_prefix']
      else:
        netmask = helpers.MAP_NETMASK_v4[block['subnet_size']]

      parent = block['parent_' + _type + '_name']
      name = block[_type + '_name']
      _id = block[_type + '_id']

      helpers.logger.debug(json.dumps(block, indent=2))
      if bool(int(block['is_terminal'])):
        sub = Subnet(name, block['start_hostaddr'], netmask, adom, ipv6=v6, _id=_id, parent=parent)
        subnets.append(sub)
      else:
        grp = Group(name, adom, ipv6=v6, _id=_id, parent=parent)
        groups.append(grp)

  loop(blocks_v4, False)
  loop(blocks_v6, True)

  for s in subnets:
    for g in groups:
      if g.get_name() == s.get_parent() and g.is_ipv6() == s.is_ipv6():
        g.add_member(s)
    s.push_to_FMG()
  for g in groups:
    for g2 in groups:
      if g2.get_name() == g.get_parent() and g2.is_ipv6() == g.is_ipv6():
        g2.add_member(s)
    g.push_to_FMG()

  return 0

def sync_addr(con, adom):
  rest_answer = con.query("ip_address_list", "", ssl_verify=False)
  if rest_answer.content is not None:
    addr_json = json.loads(rest_answer.content.decode())

  rest_answer = con.query("ip_address6_list", "", ssl_verify=False)
  if rest_answer.content is not None:
    addr6_json = json.loads(rest_answer.content.decode())

  addresses = list()

  for a in addr_json:
    if a['type'] != 'ip':
      continue
    helpers.logger.debug(json.dumps(a, indent=2))
    addresses.append(Address(a['name'], a['hostaddr'], adom, _id=a['ip_id'], parent=a['subnet_name'] + '_' + a['parent_subnet_name']))
  for a in addr6_json:
    if a['type'] != 'ip6':
      continue
    helpers.logger.debug(json.dumps(a, indent=2))
    addresses.append(Address(a['ip6_name'], a['hostaddr'], adom, ipv6=True, _id=a['ip6_id'], parent=a['subnet6_name'] + '_' + a['parent_subnet6_name']))
  for a in addresses:
    a.push_to_FMG()
  for a in addresses:
    code, data = a.push_to_FMG()


if __name__ == "__main__":
  main(sys.argv)