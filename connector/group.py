import json
from . import helpers
from .subnet import Subnet
from ftntlib import FortiManagerJSON

class Group(object):
  def __init__(self, name, subgrp: list, subnets: list, adom="global"):
    self.__name = name
    self.__subgrp = subgrp
    self.__subnets = subnets
    self.__adom = adom
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
    helpers.logger.info("Creating group " + self.__name + " on FMG")
    helpers.logger.debug("\n\tsubgroups: " + str(self.__subgrp) + "\n\tsubnets: " + str(self.__subnets) + "\n\tadom: " + self.__adom)
    urlpf = "pm/config/" + self.__adom
    member = list()
    for sub in self.__subnets:
      member.append(sub.get_name())
    for grp in self.__subgrp:
      member.append(grp.get_name())
    obj = {
      'name': self.__name,
      'comment': 'Created by efficientIP',
      'color': 13,
      'member': member
      }
    print(str(obj))
    code, data = helpers.api.add(urlpf + '/obj/firewall/addrgrp', obj)

    if code['code'] != 0:
      raise RuntimeError(code['message'])

    return code,data

  def _FMG_update(self):
    pass

  def get_name(self):
    return self.__name

  def _is_new(self):
    status,data = helpers.firewall_table(self.__adom, self.__name)
    if status['code'] == 0:
      self.__data = data
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