import logging
import json
import sys
from ftntlib import FortiManagerJSON

api = FortiManagerJSON()
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
logger = logging.getLogger()

def firewall_table(adom, address=""):
  status, data = api.get("/pm/config/" + adom + "/obj/firewall/address/" + address)
  logger.info("status: " + str(status))

  return status,data
