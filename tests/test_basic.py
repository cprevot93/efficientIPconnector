# -*- coding: utf-8 -*-

import unittest
import random
import string
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from connector import Subnet,Group,helpers
from tests import context

class BasicTestSuite(unittest.TestCase):
  """Basic test cases."""

  def test_add_new_subnet_and_delete(self):
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    print(random_str)
    sub = Subnet(random_str, "0.0.0.0", "255.255.0.0", context.adom)
    sub.push_to_FMG()
    code,data = helpers.firewall_table(context.adom, random_str)
    self.assertTrue(code['code'] == 0)
    sub.FMG_delete()
    code,data = helpers.firewall_table(context.adom, random_str)
    helpers.api.logout()
    self.assertTrue(code['code'] == -3)


if __name__ == '__main__':
  unittest.main()