#
# Author: Charles Prevot - Fortinet
# Date: 04/2019
#
import logging
import json
import sys
from ftntlib import FortiManagerJSON

api = FortiManagerJSON()
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
logger = logging.getLogger()

MAP_NETMASK_v4 = {
  '1' : '255.255.255.255',
  '2' : '255.255.255.254',
  '4' : '255.255.255.252',
  '8' : '255.255.255.248',
  '16' : '255.255.255.240',
  '32' : '255.255.255.224',
  '64' : '255.255.255.192',
  '128' : '255.255.255.128',
  '256' : '255.255.255.0',
  '512' : '255.255.254.0',
  '1024' : '255.255.252.0',
  '2048' : '255.255.248.0',
  '4096' : '255.255.240.0',
  '8192' : '255.255.224.0',
  '16384' : '255.255.192.0',
  '32768' : '255.255.128.0',
  '65536' : '255.255.0.0',
  '131072' : '255.254.0.0',
  '262144' : '255.252.0.0',
  '524288' : '255.248.0.0',
  '1048576' : '255.240.0.0',
  '2097152' : '255.224.0.0',
  '4194304' : '255.192.0.0',
  '8388608' : '255.128.0.0',
  '16777216' : '255.0.0.0',
  '33554432' : '254.0.0.0',
  '67108864' : '252.0.0.0',
  '134217728' : '248.0.0.0',
  '268435456' : '240.0.0.0',
  '536870912' : '224.0.0.0',
  '1073741824' : '192.0.0.0',
  '2147483648' : '128.0.0.0'
}

def firewall_table(adom, address="", ipv6=False):
  """Get firewall objects on FMG
  By default, fetch list of all firewall objects on the FMG.
  If address is specified, the function will get the specific object if it exists"""
  url = "/pm/config/" + adom + "/obj/firewall/address/" + address
  if ipv6:
    url = "/pm/config/" + adom + "/obj/firewall/address6/" + address

  logger.debug("URL: " + url)
  status, data = api.get(url)
  logger.info("status: " + str(status))

  return status,data

def group_table(adom, group="", ipv6=False):
  """Get firewall address group objects on FMG
  By default, fetch list of all firewall objects on the FMG.
  If address is specified, the function will get the specific group if it exists"""
  url = "/pm/config/" + adom + "/obj/firewall/addrgrp/" + group
  if ipv6:
    url = "/pm/config/" + adom + "/obj/firewall/addrgrp6/" + group

  logger.debug("URL: " + url)
  status, data = api.get(url)
  logger.info("status: " + str(status))

  return status,data