# -*- coding: utf-8 -*-

import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from connector import Subnet,Group,helpers
from tests import context

class AdvancedTestSuite(unittest.TestCase):
  """Advanced test cases."""

  def test_subnet_in_group_not_push(self):
    """Push a group an FMG with subnet not push on the FMG"""
    sub = Subnet("gall32", "0.0.0.0", "255.255.0.0", context.adom)
    grp = Group("test_group")
    grp.add_subnet(sub)
    with self.assertRaises(RuntimeError):
      grp.push_to_FMG()


if __name__ == '__main__':
  unittest.main()
