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
  blocks = json.loads(rest_answer.content.decode())

  subnets = list()
  groups = list()
  for block in blocks:
    sub = Subnet(block['subnet_name'], block['start_hostaddr'], helpers.MAP_NETMASK_v4[block['subnet_size']], adom, _id=block['subnet_id'])
    subnets.append(sub)

  for s in subnets:
    s.push_to_FMG()
  # for g in groups:
  #   g.push_to_FMG()

  helpers.api.logout()

if __name__ == "__main__":
  main(sys.argv)