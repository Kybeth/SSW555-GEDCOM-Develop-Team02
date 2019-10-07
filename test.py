#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test cases for user stories 
"""

import unittest
from main import Gedcom


class UserStoryTest(unittest.TestCase):
    test_file = Gedcom('My-Family-1-Oct-2019-939.ged')
    def test_us07(self):
        expect = [['ERROR US07', '@I22@'], ['ERROR US07', '@I23@']]
        result = UserStoryTest.test_file.US07()
        self.assertEqual(expect, result)
if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
