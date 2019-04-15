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

  def test_add_new_subnet_update_and_delete(self):
    """Add a new IPV4 subnet, update and delete it"""
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    sub = Subnet(random_str, "0.0.0.0", "255.255.0.0", context.adom)
    sub.push_to_FMG()
    sub.push_to_FMG()
    code,data = helpers.firewall_table(context.adom, random_str)
    self.assertTrue(code['code'] == 0)
    sub.FMG_delete()
    code,data = helpers.firewall_table(context.adom, random_str)
    self.assertTrue(code['code'] != 0)

  def test_add_new_ipv6_subnet_update_and_delete(self):
    """Add a new IPV6 subnet, update and delete it"""
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    sub = Subnet(random_str, "fe80::1", "128", context.adom, ipv6=True)
    sub.push_to_FMG()
    sub.push_to_FMG()
    code,data = helpers.firewall_table(context.adom, random_str, ipv6=True)
    self.assertTrue(code['code'] == 0)
    sub.FMG_delete()
    code,data = helpers.firewall_table(context.adom, random_str, ipv6=True)
    self.assertTrue(code['code'] != 0)

  def test_subnet_in_group_not_push(self):
    """Push a group an FMG with subnet not push on the FMG"""
    sub = Subnet("gall32", "0.0.0.0", "255.255.0.0", context.adom)
    grp = Group("test_group")
    grp.add_member(sub)
    with self.assertRaises(RuntimeError):
      grp.push_to_FMG()

  def test_subnet_ipv6_in_grp_ivp4(self):
    """Try to push a IPV6 in a IPV4 group"""
    sub = Subnet("gall32_v6", "fe80::1", "128", context.adom, ipv6=True)
    grp = Group("test_group")
    with self.assertRaises(RuntimeError):
      grp.add_member(sub)

  def test_end(self):
    """Logout from FMG"""
    helpers.api.logout()

if __name__ == '__main__':
  unittest.main()