import logging
import json
from ftntlib import FortiManagerJSON

api = FortiManagerJSON()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def firewall_table(adom, address=""):
  status, data = api.get("/pm/config/" + adom + "/obj/firewall/address/" + address)
  logger.info("status: " + str(status))

  return status,data
