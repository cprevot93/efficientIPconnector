# -*- coding: utf-8 -*-
import json
from . import helpers
from ftntlib import FortiManagerJSON

class Subnet(object):
  def __init__(self, name, subnet, netmask, adom="global", ipv6=False):
    self.__netmask = netmask
    self.__subnet = subnet
    self.__name = name
    if adom == "global":
      self.__adom = adom
    else:
      self.__adom = "adom/" + adom
    helpers.logger.debug("subnet name: " + self.__name)
    self.__ipv6 = ipv6
    self.__data = None

  def push_to_FMG(self):
    try:
      if self._is_new():
        self._FMG_create()
      else:
        self._FMG_update()
    except RuntimeError as e:
      raise e

  def _FMG_create(self):
    helpers.logger.info("Creating subnet " + self.__name + " on FMG")
    helpers.logger.debug("\n\tsubnet: " + self.__subnet + "\n\tnetmask: " + self.__netmask + "\n\tadom: " + self.__adom)
    urlpf = "pm/config/" + self.__adom
    url = urlpf + "/obj/firewall/address"
    if self.__ipv6:
      obj = {
        'name': self.__name,
        'type': 'ipprefix',
        'color': 13,
        'ipv6': self.__subnet + "/" + self.__netmask
        }
      url = url + "6"
    else:
      obj = {
        'name': self.__name,
        'type': 'ipmask',
        'color': 13,
        'subnet': [self.__subnet, self.__netmask]
        }
    helpers.logger.debug("URL: " + url)
    code, data = helpers.api.add(url, obj)

    if code['code'] != 0:
      raise RuntimeError(code['message'])

    return code,data

  def _FMG_update(self):
    helpers.logger.info("Updating subnet " + self.__name + " on FMG")
    helpers.logger.debug("\n\tsubnet: " + self.__subnet + "\n\tnetmask: " + self.__netmask + "\n\tadom: " + self.__adom)
    urlpf = "pm/config/" + self.__adom
    url = urlpf + "/obj/firewall/address"
    if self.__ipv6:
      obj = { 'ipv6': self.__subnet + "/" + self.__netmask }
      url = url + "6"
    else:
      obj = { 'subnet': [self.__subnet, self.__netmask] }
    
    helpers.logger.debug("URL: " + url)
    code, data = helpers.api.update(url + "/" + self.__name, obj)

    if code['code'] != 0:
      raise RuntimeError(code['message'])

    return code,data

  def FMG_delete(self):
    helpers.logger.info("Deleting subnet " + self.__name + " on FMG")
    urlpf = "pm/config/" + self.__adom
    if self.__ipv6:
      code, data = helpers.api.delete(urlpf + '/obj/firewall/address6/' + self.__name)
    else:
      code, data = helpers.api.delete(urlpf + '/obj/firewall/address/' + self.__name)

    if code['code'] != 0:
      raise RuntimeError(code['message'])
    return

  def get_name(self):
    return self.__name

  def _is_new(self):
    status,data = helpers.firewall_table(self.__adom, self.__name)
    if status['code'] == 0:
      self.__data = data
      return False
    else:
      return True
