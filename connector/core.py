# -*- coding: utf-8 -*-
import json
from . import helpers
from ftntlib import FortiManagerJSON

class Subnet(object):
  def __init__(self, name, subnet, netmask, adom="global"):
    self.netmask = netmask
    self.subnet = subnet
    self.name = name
    self.adom = adom
    helpers.logger.debug("subnet name: " + self.name)
    self.data = None

  def create_on_FMG(self):
    obj = {
      'name': self.name,
      'type': 'ipmask',
      'color': 13,
      'subnet': [self.subnet, self.netmask]
      }
    urlpf = "pm/config/" + self.adom
    code, data = helpers.api.add(urlpf + '/obj/firewall/address', obj)
    helpers.logger.info("status: " + str(code))

    return code,data

  def update(self):
    pass

  def is_new(self):
    status,data = helpers.firewall_table(self.adom, self.name)
    if status['code'] == 0:
      self.data = data
      return False
    else:
      return True

# def main(argv):
#   me, adom, package, objip = argv
#   addrgrp = 'Detected_BLOCK_IPs'
#   urlpf = 'pm/config/adom/' + adom
#   api = FortiManagerJSON()
#   api.debug('on')
#   api.login(ip, user, pwd)
#   objname = 'block_' + objip
#   obj = {
#     'name': objname,
#     'type': 'ipmask',
#     'color': 13,
#     'subnet': [objip,'255.255.255.255']
#     }
#   api.add(urlpf + '/obj/firewall/address', obj)
#   code,d = api.get(urlpf + '/obj/firewall/addrgrp/' + addrgrp)
  
#   if type(d['data']['member']) is list:
#     member = d['data']['member']
#   if objname not in member:
#     member.append(objname)
#   else:
#     member = [d['data']['member'], objname]
#     data = {'member':member}
#   api.update(urlpf + '/obj/firewall/addrgrp/' + addrgrp, data)
#   scope = [ {'name' : 'All_FortiGate'} ]
#   flags = ['install_chg','generate_rev']
#   ret_code, response = api.install_package(adom, package, scope, flags)
#   api.logout()
#   api.debug('off')
#   return