# -*- coding: utf-8 -*-
from . import helpers
from .subnet import Subnet
from ftntlib import FortiManagerJSON
from .fmgobject import FMG_object

class Group(FMG_object):
  def __init__(self, name, subgrp: list, subnets: list, adom="global", ipv6=False):
    FMG_object.__init__(self, name, adom, ipv6)
    self.__subgrp = subgrp
    self.__subnets = subnets
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
    pass

  def _is_new(self):
    status,data = helpers.firewall_table(self.get_adom(), self.get_name())
    if status['code'] == 0:
      self.set_data(data)
      return False
    else:
      return True

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