# -*- coding: utf-8 -*-
from . import helpers
from ftntlib import FortiManagerJSON
from .fmgobject import FMG_object

class Subnet(FMG_object):
  def __init__(self, name, subnet, netmask, adom, ipv6=False):
    FMG_object.__init__(self, name, adom, ipv6)
    self.__netmask = netmask
    self.__subnet = subnet

  def _FMG_create(self):
    helpers.logger.info("Creating subnet " + self.get_name() + " on FMG")
    helpers.logger.debug("\n\tsubnet: " + self.__subnet + "\n\tnetmask: " + self.__netmask + "\n\tadom: " + self.get_adom())
    urlpf = "pm/config/" + self.get_adom()
    url = urlpf + "/obj/firewall/address"
    if self.is_ipv6():
      obj = {
        'name': self.get_name(),
        'type': 'ipprefix',
        'color': 13,
        'ip6': self.__subnet + "/" + self.__netmask
        }
      url += "6"
    else:
      obj = {
        'name': self.get_name(),
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
    helpers.logger.info("Updating subnet " + self.get_name() + " on FMG")
    helpers.logger.debug("\n\tsubnet: " + self.__subnet + "\n\tnetmask: " + self.__netmask + "\n\tadom: " + self.get_adom())

    urlpf = "pm/config/" + self.get_adom()
    url = urlpf + "/obj/firewall/address"

    if self.is_ipv6():
      obj = { 'ip6': self.__subnet + "/" + self.__netmask }
      url = url + "6"
    else:
      obj = { 'subnet': [self.__subnet, self.__netmask] }
    url += "/" + self.get_name()
    helpers.logger.debug("URL: " + url)

    # Idempotence
    code = {'code': 0, 'message': 'No change made'}
    if self.is_ipv6():
      if self.get_data()['ip6'] == obj['ip6']:
        return code
    else:
      if self.get_data()['subnet'] == obj['subnet']:
        return code
    code, data = helpers.api.update(url, obj)

    if code['code'] != 0:
      raise RuntimeError(code['message'])

    return code,data

  def FMG_delete(self):
    helpers.logger.info("Deleting subnet " + self.get_name() + " on FMG")
    urlpf = "pm/config/" + self.get_adom()
    if self.is_ipv6():
      code, data = helpers.api.delete(urlpf + '/obj/firewall/address6/' + self.get_name())
    else:
      code, data = helpers.api.delete(urlpf + '/obj/firewall/address/' + self.get_name())

    if code['code'] != 0:
      raise RuntimeError(code['message'])
    return True

  def _is_new(self):
    status,data = helpers.firewall_table(self.get_adom(), self.get_name(), self.is_ipv6())
    if status['code'] == 0:
      self.set_data(data)
      return False
    else:
      return True
