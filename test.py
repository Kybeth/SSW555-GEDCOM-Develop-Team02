#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
from main import Repo

class UserStoryTest(unittest.TestCase):
    """Vignesh Mohan"""
    def test_US01(self):
        repo = Repo()
        repo.read_file("ged/das.ged")
        self.assertEqual(repo.US01(), True)
        self.assertNotEqual(repo.US01(), False)
        self.assertTrue(repo.US01())

    def test_US02(self):
        repo = Repo()
        repo.read_file("ged/das.ged")
        self.assertEqual(repo.US02(), True)
        self.assertNotEqual(repo.US02(), False)
        self.assertTrue(repo.US02())
    
    """Anirudh Bezzam"""
    def test_US03(self):
        repo = Repo()
        repo.read_file("ged/das.ged")
        self.assertEqual(repo.US03(), True)
        self.assertNotEqual(repo.US03(), False)
        self.assertTrue(repo.US03())

    def test_US04(self):
        repo = Repo()
        repo.read_file("ged/das.ged")
        self.assertEqual(repo.US04(), True)
        self.assertNotEqual(repo.US04(), False)
        self.assertTrue(repo.US04())

    def test_US13(self):
        repo = Repo()
        repo.read_file("ged/das.ged")
        self.assertEqual(repo.US13(), True)
        self.assertNotEqual(repo.US13(), False)
        self.assertTrue(repo.US13())

    def test_US14(self):
        repo = Repo()
        repo.read_file("ged/das.ged")
        self.assertEqual(repo.US14(), True)
        self.assertNotEqual(repo.US14(), False)
        self.assertTrue(repo.US14())

    """Lifu Xiao"""
    def test_US07(self):
        repo = Repo()
        repo.read_file("ged/myfamily.ged")
        self.assertEqual(repo.US07(),['@I22@', '@I24@', '@I25@'])

    def test_US08(self):
        repo = Repo()
        repo.read_file("ged/myfamily.ged")
        self.assertEqual(repo.US08(),['@I1@', '@I24@'])

    def test_US17(self):
        repo = Repo()
        repo.read_file("ged/us17.ged")
        self.assertEqual(repo.US17(),['@I1@', '@I3@'])

    def test_US18(self):
        repo = Repo()
        repo.read_file("ged/myfamily.ged")
        self.assertEqual(repo.US18(),['@I12@', '@I13@', '@I15@', '@I16@'])

    def test_US27(self):
        repo = Repo()
        repo.read_file("ged/myfamily.ged")
        self.assertEqual(repo.US27(),list())
    
    def test_US28(self):
        repo = Repo()
        repo.read_file("ged/myfamily.ged")
        self.assertEqual(repo.US28()[0],[(-2982, '@I5@'), (7, '@I21@'), (36, '@I3@'), (54, '@I7@')])
        self.assertEqual(repo.US28()[1],[(85, '@I1@'), (239, '@I24@')])

if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)