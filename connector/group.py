# -*- coding: utf-8 -*-
from . import helpers
from .subnet import Subnet
from ftntlib import FortiManagerJSON
from .fmgobject import FMG_object

class Group(FMG_object):
  def __init__(self, name, adom="global", ipv6=False):
    FMG_object.__init__(self, name, adom, ipv6)
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
      'comment': 'Created by efficientIP',
      'color': 13,
      'member': member
      }
    helpers.logger.debug("URL: " + url)
    code, data = helpers.api.add(url, obj)

    if code['code'] != 0:
      raise RuntimeError(code['message'])

    return code,data

  def _FMG_update(self):
    # TODO: Idempotence
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
    code, data = helpers.api.update(url, obj)

    if code['code'] != 0:
      raise RuntimeError(code['message'])

    return code,data

  def FMG_delete(self):
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

  def add_subnet(self, sub):
    if type(sub) is not Subnet:
      raise Exception("parameter type error")
    if self.is_ipv6() != sub.is_ipv6():
      raise RuntimeError("Error IP version")
    if sub in self.__subnets:
      raise RuntimeError("Subnet already added to group")

    helpers.logger.debug("Add " + sub.get_name() + " subnet to group " + self.get_name())
    self.__subnets.append(sub)
    return

  def del_subnet(self, sub):
    try:
      helpers.logger.debug("Remove " + sub.get_name() + " subnet from group " + self.get_name())
      self.__subnets.remove(sub)
    except:
      pass
    return

  def add_subgrp(self, grp):
    if type(grp) is not Group:
      raise Exception("parameter type error")
    if self.is_ipv6() != grp.is_ipv6():
      raise RuntimeError("Error IP version")
    if grp in self.__subgrp:
      raise RuntimeError("SubGroup already added to group")

    helpers.logger.debug("Add " + grp.get_name() + " subgroup to group " + self.get_name())
    self.__subgrp.append(grp)
    return

  def del_subgrp(self, grp):
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
