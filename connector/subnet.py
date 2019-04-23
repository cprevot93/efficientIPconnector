# -*- coding: utf-8 -*-
#
# Author: Charles Prevot - Fortinet
# Date: 04/2019
#
from . import helpers
from ftntlib import FortiManagerJSON
from .fmgobject import FMG_object

class Subnet(FMG_object):
  """Subnet object following FMG firewall object address"""

  __netmask = None
  __subnet = None

  def __init__(self, name, subnet, netmask, adom, ipv6=False, _id=0, parent=None):
    FMG_object.__init__(self, name, adom, ipv6, _id, parent)
    self.__netmask = netmask
    self.__subnet = subnet

  def _FMG_create(self):
    helpers.logger.info("Creating subnet " + self.get_FMG_name() + " on FMG")
    helpers.logger.debug("\n\tsubnet: " + self.__subnet + "\n\tnetmask: " + self.__netmask + "\n\tadom: " + self.get_adom())
    urlpf = "pm/config/" + self.get_adom()
    url = urlpf + "/obj/firewall/address"
    obj = {
      'name': self.get_FMG_name(),
      'type': 'ipmask',
      'color': 13,
      'comment': 'Created by EfficientIP'
    }
    if self.is_ipv6():
      obj['type'] = 'ipprefix'
      obj['ip6'] = self.__subnet + "/" + self.__netmask
      url += "6"
    else:
      obj['subnet'] = [self.__subnet, self.__netmask]

    helpers.logger.debug("URL: " + url)
    code, data = helpers.api.add(url, obj)
    if code['code'] != 0:
      raise RuntimeError(code['message'])

    return code,data

  def _FMG_update(self):
    helpers.logger.info("Updating subnet " + self.get_FMG_name() + " on FMG")
    helpers.logger.debug("\n\tsubnet: " + self.__subnet + "\n\tnetmask: " + self.__netmask + "\n\tadom: " + self.get_adom())

    urlpf = "pm/config/" + self.get_adom()
    url = urlpf + "/obj/firewall/address"

    if self.is_ipv6():
      obj = { 'ip6': self.__subnet + "/" + self.__netmask }
      url = url + "6"
    else:
      obj = { 'subnet': [self.__subnet, self.__netmask] }
    url += "/" + self.get_FMG_name()
    helpers.logger.debug("URL: " + url)

    # Idempotence
    # _FMG_update is called in _is_net, so get_data is updated with the call firewall_table
    code = {'code': 1, 'message': 'No change made'}
    if self.is_ipv6():
      if self.get_data()['ip6'] == obj['ip6']:
        return code, None
    else:
      if self.get_data()['subnet'] == obj['subnet']:
        return code, None

    code, data = helpers.api.update(url, obj)
    if code['code'] != 0:
      raise RuntimeError(code['message'])

    return code,data


  def _is_new(self):
    status,data = helpers.firewall_table(self.get_adom(), self.get_FMG_name(), self.is_ipv6())
    if status['code'] == 0:
      self.set_data(data)
      return False
    else:
      return True

  def get_subnet(self):
    return self.__subnet

  def get_FMG_name(self):
    return str(self.get_id()) + '-' + self.get_name() + '_' + self.get_parent()