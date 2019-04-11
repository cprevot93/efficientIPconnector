import logging
import json
import sys
from ftntlib import FortiManagerJSON

api = FortiManagerJSON()
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
logger = logging.getLogger()

def firewall_table(adom, address="", ipv6=False):
  if adom != "global":
    adom = "adom/" + adom

  url = "/pm/config/" + adom + "/obj/firewall/address/" + address
  if ipv6:
    url = "/pm/config/" + adom + "/obj/firewall/address6/" + address

  status, data = api.get(url)
  logger.info("status: " + str(status))

  return status,data

def group_table(adom, group="", ipv6=False):
  if adom != "global":
    adom = "adom/" + adom

  url = "/pm/config/" + adom + "/obj/firewall/addrgrp/" + group
  if ipv6:
    url = "/pm/config/" + adom + "/obj/firewall/addrgrp6/" + group

  status, data = api.get(url)
  logger.info("status: " + str(status))

  return status,data