# -*- coding: utf-8 -*-
#
# Author: Charles Prevot - Fortinet
# Date: 04/2019
#
from . import helpers
from ftntlib import FortiManagerJSON

class FMG_object:

  __id = None
  __name = None
  __adom = None
  __ipv6 = None
  __data = None
  __parent = None

  def __init__(self, name, adom="global", ipv6=False, _id=0, parent=None):
    self.__id = _id
    self.__name = name
    if adom == "global":
      self.__adom = adom
    else:
      self.__adom = "adom/" + adom
    self.__ipv6 = ipv6
    self.__data = None
    self.__parent = parent

  def push_to_FMG(self):
    try:
      if self._is_new():
        code, data = self._FMG_create()
      else:
        code, data = self._FMG_update()
      helpers.logger.debug(code)
      if data:
        helpers.logger.debug(data)
      return code, data
    except RuntimeError as e:
      raise e

  def FMG_delete(self, _type="address"):
    """Delete object on the FMG"""
    helpers.logger.info("Deleting " + _type + ' ' +  self.get_FMG_name() + " on FMG")
    url = "pm/config/" + self.get_adom() + '/obj/firewall/' + _type
    if self.is_ipv6():
      url += '6'
    url += '/' + self.get_FMG_name()

    code, data = helpers.api.delete(url)
    helpers.logger.debug(code)
    # object firewall is been used
    if code['code'] == -10015:
      return False
    if code['code'] != 0:
      raise RuntimeError(code['message'])
    return True


  def _FMG_create(self):
    return None, None

  def _FMG_update(self):
    return None, None

  def _FMG_delete(self):
    return False

  def get_id(self):
    return self.__id

  def get_FMG_name(self):
    return str(self.__id) + '-' + self.__name

  def get_name(self):
    return self.__name

  def is_ipv6(self):
    return self.__ipv6
  
  def get_parent(self):
    return self.__parent

  def get_adom(self):
    return self.__adom

  def get_data(self):
    return self.__data

  def set_data(self, data):
    self.__data = data

  def _is_new(self):
    return False
