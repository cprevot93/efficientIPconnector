#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import json
from .subnet import Subnet
from .group import Group
from . import helpers
import SOLIDserverRest

# if len(sys.argv) < 2:
#   print('Usage: ' + sys.argv[0] + 'IP <JSON API URL>')
#   exit(1)

def main(argv):
  ip_FMG = "100.68.99.10"
  ip_SOLIDserver = "100.68.99.20"
  user ='admin'
  passwd ='fortinet'
  adom = "root"
  helpers.api.login(ip_FMG, user, passwd)
  helpers.api.debug('off')

  con = SOLIDserverRest.SOLIDserverRest(ip_SOLIDserver)
  con.use_native_ssd(user="ipmadmin", password="admin")
  rest_answer = con.query("ip_subnet_list", "", ssl_verify=False)
  if rest_answer.content:
    blocks_v4 = json.loads(rest_answer.content.decode())

  rest_answer = con.query("ip_subnet6_list", "", ssl_verify=False)
  if rest_answer.content:
    blocks_v6 = json.loads(rest_answer.content.decode())

  subnets = list()
  groups = list()

  def loop(blocks, v6):
    if blocks is None:
      return
    for block in blocks:
      # print(json.dumps(block, indent=2))
      if bool(int(block['is_terminal'])):
        sub = Subnet(block['subnet_name'], block['start_hostaddr'], helpers.MAP_NETMASK_v4[block['subnet_size']], adom, ipv6=v6, _id=block['subnet_id'], parent=block['parent_subnet_name'])
        subnets.append(sub)
      else:
        grp = Group(block['subnet_name'], adom, ipv6=v6, _id=block['subnet_id'], parent=block['parent_subnet_name'])
        groups.append(grp)

  loop(blocks_v4, False)
  # loop(blocks_v6, True)

  for s in subnets:
    for g in groups:
      if g.get_name() == s.get_parent():
        g.add_member(s)
    s.push_to_FMG()
  for g in groups:
    g.push_to_FMG()

  helpers.api.logout()

if __name__ == "__main__":
  main(sys.argv)