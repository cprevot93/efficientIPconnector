# -*- coding: utf-8 -*-

import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from connector import Subnet,Group,helpers
from tests import context

class AdvancedTestSuite(unittest.TestCase):
  """Advanced test cases."""

  def test_true(self):
    self.assertTrue(True)

if __name__ == '__main__':
  unittest.main()
