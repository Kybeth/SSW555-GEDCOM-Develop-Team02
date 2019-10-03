#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test cases for user stories 
"""

import unittest
from main import parse_file


class UserStoryTest(unittest.TestCase):

    def test_test(self):
        self.assertEqual('foo'.upper(), 'FOO')

if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
