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
        
    def test_us05(self):
        expect = [['ANOMALY US05', '@I1@'],['ANOMALY US05', '@I7@'],['ANOMALY US05', '@I8@'],['ANOMALY US05', '@I9@'],['ANOMALY US05', '@I11@'],['ANOMALY US05', '@I12@'],['ANOMALY US05', '@I14@'],['ANOMALY US05', '@I15@'],['ANOMALY US05', '@I17@'],['ANOMALY US05', '@I18@'],['ANOMALY US05', '@I19@'],['ANOMALY US05', '@I21@'],['ANOMALY US05', '@I24@']]
        result = UserStoryTest.test_file.US05()
        self.assertEqual(expect, result)
    
    def test_us06(self):
        expect = [['ANOMALY US06', '@I14@'],['ANOMALY US06', '@I15@']]
        result = UserStoryTest.test_file.US06()
        self.assertEqual(expect, result)


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
