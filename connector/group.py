# -*- coding: utf-8 -*-
from . import helpers
from .subnet import Subnet
from ftntlib import FortiManagerJSON
from .fmgobject import FMG_object

class Group(FMG_object):
  """Group object following FMG firewall object group"""
  def __init__(self, name, adom="global", ipv6=False, _id=0):
    FMG_object.__init__(self, name, adom, ipv6, _id)
    self.__subgrp = list()
    self.__subnets = list()
    self.__member = list()

  def _FMG_create(self):
    helpers.logger.info("Creating group " + self.get_name() + " on FMG")
    urlpf = "pm/config/" + self.get_adom()
    url = urlpf + "/obj/firewall/addrgrp"
    if self.is_ipv6():
      url += "6"

    member = list()
    for sub in self.__subnets:
      member.append(sub.get_name())
    debug = "\n\tsubnets: " + str(member)

    for grp in self.__subgrp:
      member.append(grp.get_name())
    debug += "\n\tsubgroups: " + str(self.__subgrp) + "\n\tadom: " + self.get_adom()
    helpers.logger.debug(debug)
    obj = {
      'name': self.get_name(),
      'comment': 'Created by EfficientIP',
      'color': 13,
      'member': member
      }
    helpers.logger.debug("URL: " + url)
    code, data = helpers.api.add(url, obj)

    if code['code'] != 0:
      raise RuntimeError(code['message'])

    return code,data

  def _FMG_update(self):
    helpers.logger.info("Updating group " + self.get_name() + " on FMG")
    urlpf = "pm/config/" + self.get_adom()
    url = urlpf + "/obj/firewall/addrgrp"
    if self.is_ipv6():
      url += "6"
    url += "/" + self.get_name()
    
    member = list()
    for sub in self.__subnets:
      member.append(sub.get_name())
    debug = "\n\tsubnets: " + str(member)

    for grp in self.__subgrp:
      member.append(grp.get_name())
    debug += "\n\tsubgroups: " + str(self.__subgrp) + "\n\tadom: " + self.get_adom()
    helpers.logger.debug(debug)
    obj = { 'member': member }
    helpers.logger.debug("URL: " + url)

    # Idempotence
    if self.get_data()['member'] == obj['member']:
      return {'code': 1, 'message': 'No change made'}

    code, data = helpers.api.update(url, obj)

    if code['code'] != 0:
      raise RuntimeError(code['message'])

    return code,data

  def FMG_delete(self):
    """Delete group on the FMG"""
    helpers.logger.info("Deleting group " + self.get_name() + " on FMG")
    urlpf = "pm/config/" + self.get_adom()
    url = urlpf + '/obj/firewall/addrgrp'
    if self.is_ipv6():
      url += "6"
    
    url += "/" + self.get_name()
    helpers.logger.debug("URL: " + url)
    code, data = helpers.api.delete(url)

    if code['code'] != 0:
      raise RuntimeError(code['message'])
    return

  def add_member(self, m):
    """Add a member to group (subnet or sub group)"""
    if type(m) is Subnet:
      self._add_subnet(m)
    elif type(m) is Group:
      self._add_subgrp(m)
    else:
      raise Exception("parameter type error")

  def del_member(self, m):
    """Delete a member to group (subnet or sub group)"""
    if type(m) is Subnet:
      self._del_subnet(m)
    elif type(m) is Group:
      self._del_subgrp(m)
    else:
      raise Exception("parameter type error")

  def _add_subnet(self, sub):
    if self.is_ipv6() != sub.is_ipv6():
      raise RuntimeError("Error IP version")
    if sub in self.__subnets:
      raise RuntimeError("Subnet already added to group")

    helpers.logger.debug("Add " + sub.get_name() + " subnet to group " + self.get_name())
    self.__subnets.append(sub)
    return

  def _del_subnet(self, sub):
    try:
      helpers.logger.debug("Remove " + sub.get_name() + " subnet from group " + self.get_name())
      self.__subnets.remove(sub)
    except:
      pass
    return

  def _add_subgrp(self, grp):
    if self.is_ipv6() != grp.is_ipv6():
      raise RuntimeError("Error IP version")
    if grp in self.__subgrp:
      raise RuntimeError("SubGroup already added to group")

    helpers.logger.debug("Add " + grp.get_name() + " subgroup to group " + self.get_name())
    self.__subgrp.append(grp)
    return

  def _del_subgrp(self, grp):
    try:
      helpers.logger.debug("Remove " + grp.get_name() + " subgroup from group " + self.get_name())
      self.__subgrp.remove(grp)
    except:
      pass
    return

  def _is_new(self):
    status,data = helpers.group_table(self.get_adom(), self.get_name())
    if status['code'] == 0:
      self.set_data(data)
      return False
    else:
      return True
