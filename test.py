#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
from main import Repo

class UserStoryTest(unittest.TestCase):

    path = 'ged/myfam.ged'
    repo = Repo()
    repo.read_file(path)

    """US01""" #By - Vignesh Mohan
    def test_US01(self):
        """US01 - Dates before current date"""
        self.assertEqual(UserStoryTest.repo.US01(), True)
        self.assertNotEqual(UserStoryTest.repo.US01(), False)
        self.assertTrue(UserStoryTest.repo.US01())

    """US02""" #By - Vignesh Mohan
    def test_US02(self):
        """US02 - Birth before Marriage"""
        self.assertEqual(UserStoryTest.repo.US02(), True)
        self.assertNotEqual(UserStoryTest.repo.US02(), False)
        self.assertTrue(UserStoryTest.repo.US02())
    
    """US03"""
    def test_US03(self):
        """US03 - Birth before Death of Individual"""
        self.assertEqual(UserStoryTest.repo.US03(), True)
        self.assertNotEqual(UserStoryTest.repo.US03(), False)
        self.assertTrue(UserStoryTest.repo.US03())

    """US04"""

    def test_US04(self):
        """US04	Marriage before divorce"""
        self.assertEqual(UserStoryTest.repo.US04(), True)
        self.assertNotEqual(UserStoryTest.repo.US04(), False)
        self.assertTrue(UserStoryTest.repo.US04())

    """US13"""

    def test_US13(self):
        """US13 - Birth Dates of Sibilings should be more than 8 months apart or less than 2 days apart"""
        self.assertEqual(UserStoryTest.repo.US13(), True)
        self.assertNotEqual(UserStoryTest.repo.US13(), False)
        self.assertTrue(UserStoryTest.repo.US13())

    """US14"""

    def test_US14(self):
        """US14 - Multiple births <= 5"""
        self.assertEqual(UserStoryTest.repo.US14(), True)
        self.assertNotEqual(UserStoryTest.repo.US14(), False)
        self.assertTrue(UserStoryTest.repo.US14())

if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)