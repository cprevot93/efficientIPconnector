# -*- coding: utf-8 -*-
import json
from . import helpers
from ftntlib import FortiManagerJSON

class Subnet(object):
  def __init__(self, name, subnet, netmask, adom="global"):
    self.__netmask = netmask
    self.__subnet = subnet
    self.__name = name
    if adom == "global":
      self.__adom = adom
    else:
      self.__adom = "adom/" + adom
    helpers.logger.debug("subnet name: " + self.__name)
    self.__data = None

  def push_to_FMG(self):
    if self._is_new():
      self._FMG_create()
    else:
      self._FMG_update()
  
  def _FMG_create(self):
    helpers.logger.info("Creating subnet " + self.__name + " on FMG")
    helpers.logger.debug("\n\tsubnet: " + self.__subnet + "\n\tnetmask: " + self.__netmask + "\n\tadom: " + self.__adom)
    obj = {
      'name': self.__name,
      'type': 'ipmask',
      'color': 13,
      'subnet': [self.__subnet, self.__netmask]
      }
    urlpf = "pm/config/" + self.__adom
    code, data = helpers.api.add(urlpf + '/obj/firewall/address', obj)
    if code['code'] != 0:
      raise RuntimeError(code['message'])

    return code,data

  def _FMG_update(self):
    helpers.logger.info("Creating subnet " + self.__name + " on FMG")
    helpers.logger.debug("\n\tsubnet: " + self.__subnet + "\n\tnetmask: " + self.__netmask + "\n\tadom: " + self.__adom)
    obj = {
      'name': self.__name,
      'type': 'ipmask',
      'subnet': [self.__subnet, self.__netmask]
      }
    urlpf = "pm/config/" + self.__adom
    code, data = helpers.api.update(urlpf + '/obj/firewall/address', obj)
    if code['code'] != 0:
      raise RuntimeError(code['message'])

    return code,data

  def _is_new(self):
    status,data = helpers.firewall_table(self.__adom, self.__name)
    if status['code'] == 0:
      self.__data = data
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