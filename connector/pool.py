# -*- coding: utf-8 -*-
#
# Author: Charles Prevot - Fortinet
# Date: 04/2019
#
from . import helpers
from ftntlib import FortiManagerJSON
from .fmgobject import FMG_object

class Pool(FMG_object):
  """Pool object following FMG firewall object address"""
  
  __start_ip = None
  __end_ip = None

  def __init__(self, name, start_ip, end_ip, adom, ipv6=False, _id=0, parent=None):
    FMG_object.__init__(self, name, adom, ipv6, _id, parent)
    self.__start_ip = start_ip
    self.__end_ip = end_ip

  def _FMG_create(self):
    helpers.logger.info("Creating pool " + self.get_FMG_name() + " on FMG")
    helpers.logger.debug("\n\tStart_IP: " + self.get_start_ip() + "\n\tEnd_IP: " + self.get_end_ip() + "\n\tadom: " + self.get_adom())
    urlpf = "pm/config/" + self.get_adom()
    url = urlpf + "/obj/firewall/address"
    if self.is_ipv6():
      url += "6"
    obj = {
      'name': self.get_FMG_name(),
      'type': 'iprange',
      'color': 13,
      'start-ip': self.get_start_ip(),
      'end-ip': self.get_end_ip(),
      'comment': 'Created by EfficientIP'
    }

    helpers.logger.debug("URL: " + url)
    code, data = helpers.api.add(url, obj)
    if code['code'] != 0:
      raise RuntimeError(code['message'])

    return code,data

  
  def _FMG_update(self):
    helpers.logger.info("Updating pool " + self.get_FMG_name() + " on FMG")
    helpers.logger.debug("\n\tStart_IP: " + self.get_start_ip() + "\n\tEnd_IP: " + self.get_end_ip() + "\n\tadom: " + self.get_adom())

    urlpf = "pm/config/" + self.get_adom()
    url = urlpf + "/obj/firewall/address"
    if self.is_ipv6():
      url = url + "6"

    obj = {
      'start-ip': self.get_start_ip(),
      'end-ip': self.get_end_ip()
    }
    url += "/" + self.get_FMG_name()
    helpers.logger.debug("URL: " + url)

    # Idempotence
    code = {'code': 1, 'message': 'No change made'}
    if self.get_data()['start-ip'] == obj['start-ip'] and self.get_data()['end-ip'] == obj['end-ip']:
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

  def get_start_ip(self):
    return self.__start_ip

  def get_end_ip(self):
    return self.__end_ip

  def get_FMG_name(self):
    return str(self.get_id()) + '-' + self.get_name() + '_' + self.get_parent()