# -*- coding: utf-8 -*-

from .subnet import Subnet

class Address(Subnet):
  def __init__(self, name, address, adom, ipv6=False, _id=0, parent=None):
    if ipv6:
      netmask = "128"
    else:
      netmask = "255.255.255.255"
    Subnet.__init__(self, name, address, netmask, adom, ipv6, _id, parent)

  def get_FMG_name(self):
    return str(self.get_id()) + '-' + self.get_name() + '_' + self.get_parent()
