# -*- coding: utf-8 -*-
from . import helpers
from ftntlib import FortiManagerJSON

class FMG_object:

  __id = None
  __name = None
  __adom = None
  __ipv6 = None
  __data = None

  def __init__(self, name, adom="global", ipv6=False, _id=0):
    self.__id = _id
    self.__name = str(_id) + '-' + name
    if adom == "global":
      self.__adom = adom
    else:
      self.__adom = "adom/" + adom
    self.__ipv6 = ipv6
    self.__data = None

  def push_to_FMG(self):
    try:
      if self._is_new():
        helpers.logger.info(self._FMG_create())
      else:
        helpers.logger.info(self._FMG_update())
    except RuntimeError as e:
      raise e

  def _FMG_create(self):
    pass

  def _FMG_update(self):
    pass

  def FMG_delete(self):
    pass

  def get_id(self):
    return self.__id

  def get_name(self):
    return self.__name

  def is_ipv6(self):
    return self.__ipv6

  def get_adom(self):
    return self.__adom

  def get_data(self):
    return self.__data

  def set_data(self, data):
    self.__data = data

  def _is_new(self):
    return False
