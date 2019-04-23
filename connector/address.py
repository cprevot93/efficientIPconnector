# -*- coding: utf-8 -*-

from .subnet import Subnet

class Address(Subnet):
  def __init__(self, name, address, adom, ipv6=False, _id=0, parent=None):
    if ipv6:
      netmask = "128"
    else:
      netmask = "255.255.255.255"
    Subnet.__init__(self, name, address, netmask, adom, ipv6, _id, parent)

  def __eq__(self, other):
      """Override the default Equals behavior"""
      return self.get_FMG_name() == other.get_FMG_name() and self.get_adom() == other.get_adom() \
        and self.get_subnet() == other.get_subnet() and self.is_ipv6() == other.is_ipv6()

  def __ne__(self, other):
      """Override the default Unequal behavior"""
      return self.get_FMG_name() != other.get_FMG_name() or self.get_adom() != other.get_adom() \
        or self.get_subnet() != other.get_subnet() or self.is_ipv6() != other.is_ipv6()
