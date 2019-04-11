# -*- coding: utf-8 -*-

from .context import connector

import unittest

class AdvancedTestSuite(unittest.TestCase):
  """Advanced test cases."""

  def test_thoughts(self):
    self.assertIsNone(True)


if __name__ == '__main__':
  unittest.main()
