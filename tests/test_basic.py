# -*- coding: utf-8 -*-

import unittest
import time
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
    code,data = sub.push_to_FMG()
    self.assertTrue(code['code'] == 1)
    self.assertTrue(sub.FMG_delete())
    code,data = helpers.firewall_table(context.adom, sub.get_FMG_name())
    self.assertTrue(code['code'] == -6)

  def test_add_new_ipv6_subnet_update_and_delete(self):
    """Add a new IPV6 subnet, update and delete it"""
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    sub = Subnet(random_str, "fe80::1", "128", context.adom, ipv6=True)
    sub.push_to_FMG()
    sub.push_to_FMG()
    code,data = helpers.firewall_table(context.adom, sub.get_FMG_name(), ipv6=True)
    self.assertTrue(code['code'] == 0)
    sub.FMG_delete()
    code,data = helpers.firewall_table(context.adom, sub.get_FMG_name(), ipv6=True)
    self.assertTrue(code['code'] == -6)

  def test_subnet_in_group_not_push(self):
    """Push a group an FMG with subnet not push on the FMG"""
    sub = Subnet("gall32", "0.0.0.0", "255.255.0.0", context.adom)
    grp = Group("test_group", context.adom)
    grp.add_member(sub)
    with self.assertRaises(RuntimeError):
      grp.push_to_FMG()

  def test_subnet_and_group_create_and_push(self):
    """Push a group an FMG with subnet not push on the FMG"""
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    sub = Subnet(random_str, "0.0.0.0", "255.255.0.0", context.adom)
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    sub2 = Subnet(random_str, "10.0.0.0", "255.0.0.0", context.adom)
    # sub.push_to_FMG()

    subnets = list()
    subnets.append(sub)
    subnets.append(sub2)

    grp = Group("test_group", context.adom)
    grp.add_member(sub)
    grp.add_member(sub2)

    grp2 = Group("test_group_2", context.adom)
    grp2.add_member(sub)

    groups = list()
    groups.append(grp)
    groups.append(grp2)

    for s in subnets:
      s.push_to_FMG()
    for g in groups:
      g.push_to_FMG()
    for g in groups:
      g.FMG_delete()
    for s in subnets:
      s.FMG_delete()

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