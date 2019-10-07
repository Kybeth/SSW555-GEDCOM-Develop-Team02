#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test cases for user stories 
"""

import unittest
from main import Gedcom


class UserStoryTest(unittest.TestCase):
    test_file = Gedcom('My-Family-7-Oct-2019-205.ged')

    def test_us01(self): # - By Vignesh Mohan
        expect = [['ERROR US01'], ['ERROR US01']]
        result = UserStoryTest.test_file.US01()
        self.assertNotEqual(expect, result)
    
    def test_us02(self): # - By Vignesh Mohan
        expect = [['ANOMALY US02', '@I1@'], ['ANOMALY US02', '@I24@']]
        result = UserStoryTest.test_file.US02()
        self.assertEqual(expect, result)
    
    def test_us07(self): # - By Lifu Xiao
        expect = [['ERROR US07', '@I22@'], ['ERROR US07', '@I24@'], ['ERROR US07', '@I25@']]
        result = UserStoryTest.test_file.US07()
        self.assertEqual(expect, result)

if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
