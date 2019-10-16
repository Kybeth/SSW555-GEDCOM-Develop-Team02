#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test cases for user stories 
"""

import unittest
from main import Gedcom


class UserStoryTest(unittest.TestCase):
    test_file = Gedcom('myfamily.ged')

    def test_us01(self):  # - By Vignesh Mohan
        expect = [['ERROR US01'], ['ERROR US01']]
        result = UserStoryTest.test_file.US01()
        self.assertNotEqual(expect, result)

    def test_us02(self):  # - By Vignesh Mohan
        expect = [['ANOMALY US02', '@I1@'], ['ANOMALY US02', '@I24@']]
        result = UserStoryTest.test_file.US02()
        self.assertEqual(expect, result)

    def test_us03(self):  # - By Anirudh Bezzam
        expect = []
        result = UserStoryTest.test_file.US03()
        self.assertEqual(expect, result)

    def test_us04(self):  # - By Anirudh Bezzam
        expect = [['ERROR: FAMILY: US04: ', '@F4@']]
        result = UserStoryTest.test_file.US04()
        self.assertEqual(expect, result)

    def test_us05(self):
        expect = [['ANOMALY US05', '@I1@'], ['ANOMALY US05', '@I9@'], ['ANOMALY US05', '@I10@'], ['ANOMALY US05', '@I11@'], ['ANOMALY US05', '@I12@'], ['ANOMALY US05', '@I13@'], [
            'ANOMALY US05', '@I15@'], ['ANOMALY US05', '@I16@'], ['ANOMALY US05', '@I17@'], ['ANOMALY US05', '@I18@'], ['ANOMALY US05', '@I19@'], ['ANOMALY US05', '@I20@'], ['ANOMALY US05', '@I24@']]
        result = UserStoryTest.test_file.US05()
        self.assertEqual(expect, result)

    def test_us06(self):
        expect = [['ANOMALY US06', '@I15@'], ['ANOMALY US06', '@I16@']]
        result = UserStoryTest.test_file.US06()
        self.assertEqual(expect, result)

    def test_us07(self):  # - By Lifu Xiao
        expect = [['ERROR US07', '@I22@'], [
            'ERROR US07', '@I24@'], ['ERROR US07', '@I25@']]
        result = UserStoryTest.test_file.US07()
        self.assertEqual(expect, result)

    def test_us08(self):  # - By Lifu Xiao
        expect = [['ANOMALY: FAMILY: US08:', '@I1@'],
                  ['ANOMALY: FAMILY: US08:', '@I24@']]
        result = UserStoryTest.test_file.US08()
        self.assertEqual(expect, result)

    def test_us09(self):  # - By Yuan Zhang
        expect = [['ERROR US09', '@I5@'], ['ERROR US09', '@I5@'],
                  ['ERROR US09', '@I20@'], ['ERROR US09', '@I21@']]
        result = UserStoryTest.test_file.US09()
        self.assertEqual(expect, result)

    def test_us10(self):  # - By Yuan Zhang
        expect = [['ANOMALY US10', '@F2@'], ['ANOMALY US10', '@F3@'], ['ANOMALY US10', '@F4@'], ['ANOMALY US10', '@F5@'], [
            'ANOMALY US10', '@F7@'], ['ANOMALY US10', '@F7@'], ['ANOMALY US10', '@F8@'], ['ANOMALY US10', '@F8@']]
        result = UserStoryTest.test_file.US10()
        self.assertEqual(expect, result)

    def test_us11(self):  # - By Vignesh Mohan
        expect = []
        result = UserStoryTest.test_file.US11()
        self.assertEqual(expect, result)

    def test_us12(self):  # - By Vignesh Mohan
        expect = []
        result = UserStoryTest.test_file.US12()
        self.assertEqual(expect, result)

    def test_us13(self):  # - Anirudh Bezzam
        expect = [['ANOMALY US13', '@F1@']]
        result = UserStoryTest.test_file.US13()

        self.assertEqual(expect, result)

    def test_us14(self):  # - Anirudh Bezzam
        expect = []
        result = UserStoryTest.test_file.US14()
        self.assertEqual(expect, result)

    def test_us15(self):  # - By Tanvi Hanamshet
        expect = [['ERROR US15'], ['ERROR US15']]
        result = UserStoryTest.test_file.us15()
        self.assertNotEqual(expect, result)

    def test_us17(self):  # - By Lifu Xiao
        expect = [[['ERROR: US18'], '@I13@'], [['ERROR: US18'], '@I13@']]
        result = UserStoryTest.test_file.US17()
        self.assertNotEqual(expect, result)

    def test_us18(self):  # - By Lifu Xiao
        expect = [[['ERROR: US18'], '@I13@', '@I12@'], [['ERROR: US18'], '@I13@', '@I12@']]
        result = UserStoryTest.test_file.US18()
        self.assertEqual(expect, result)

    def test_us19(self):  # - By Yuan Zhang
        expect = [['ANOMALY US19', '@F7@']]
        result = UserStoryTest.test_file.US19()
        self.assertEqual(expect, result)

    def test_us20(self):  # - By Yuan Zhang
        expect = [['ANOMALY US20', '@F8@']]
        result = UserStoryTest.test_file.US20()
        self.assertEqual(expect, result)


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
