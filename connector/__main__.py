#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from .subnet import Subnet
from .group import Group
from . import helpers

# if len(sys.argv) < 2:
#   print('Usage: ' + sys.argv[0] + 'IP <JSON API URL>')
#   exit(1)

def main(argv):
  ip_FMG = "10.10.20.254" 
  user ='admin'
  passwd ='AdminFMG'
  adom = "global"
  helpers.api.login(ip_FMG, user, passwd)
  helpers.api.debug('off')
  sub = Subnet("gall32", "0.0.0.0", "255.255.0.0", adom)
  sub.push_to_FMG()

  grp = Group("test_group")
  grp.add_subnet(sub)
  grp.push_to_FMG()

  helpers.api.logout()

if __name__ == "__main__":
  main(sys.argv)