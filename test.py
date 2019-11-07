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
    
    def test_US11(self):
        repo = Repo()
        repo.read_file("ged/My-Family-29-Oct-2019-620.ged")
        self.assertNotEqual(repo.US11(), True)
        self.assertFalse(repo.US11())

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

    def test_US24(self):
        """US24 - Unique families by spouses"""
        repo = Repo()
        repo.read_file("ged/das.ged")
        self.assertEqual(repo.US24(), True)
        self.assertNotEqual(repo.US24(), False)
        self.assertTrue(repo.US24())
        self.assertIsNotNone(repo.US24())
        self.assertIsNot(repo.US24(), '')

    def test_US23(self):
        """US23 - No more than one individual with the same name and birth date should appear in a GEDCOM file"""
        repo = Repo()
        repo.read_file("ged/das.ged")
        self.assertEqual(repo.US23(), True)
        self.assertNotEqual(repo.US23(), False)
        self.assertTrue(repo.US23())
        self.assertIsNotNone(repo.US23())
        self.assertIsNot(repo.US23(), '')

    """Lifu Xiao"""

    def test_US07(self):
        repo = Repo()
        repo.read_file("ged/myfamily.ged")
        self.assertEqual(repo.US07(), ['@I22@', '@I24@', '@I25@'])

    def test_US08(self):
        repo = Repo()
        repo.read_file("ged/myfamily.ged")
        self.assertEqual(repo.US08(), ['@I1@', '@I24@'])

    def test_US17(self):
        repo = Repo()
        repo.read_file("ged/us17.ged")
        self.assertEqual(repo.US17(), ['@I1@', '@I3@'])

    def test_US18(self):
        repo = Repo()
        repo.read_file("ged/myfamily.ged")
        self.assertEqual(repo.US18(), ['@I12@', '@I13@', '@I15@', '@I16@'])

    def test_US27(self):
        repo = Repo()
        repo.read_file("ged/myfamily.ged")
        self.assertEqual(repo.US27(), list())

    def test_US28(self):
        repo = Repo()
        repo.read_file("ged/myfamily.ged")
        self.assertEqual(repo.US28()[0], [
                         (-2982, '@I5@'), (7, '@I21@'), (36, '@I3@'), (54, '@I7@')])
        self.assertEqual(repo.US28()[1], [(85, '@I1@'), (239, '@I24@')])

    """Yuan Zhang"""

    def test_US09(self):  # Birth before death of parents
        repo = Repo()
        repo.read_file("ged/test_yz.ged")
        result = repo.US09()
        expect = {'I7', 'I9'}
        self.assertEqual(result, expect)

    def test_US10(self):  # Marriage after 14
        repo = Repo()
        repo.read_file("ged/test_yz.ged")
        result = repo.US10()
        expect = {'I2', 'I3'}
        self.assertEqual(result, expect)

    def test_US19(self):  # First cousins should not marry
        repo = Repo()
        repo.read_file("ged/test_yz.ged")
        result = repo.US19()
        expect = {'F4', 'F5'}
        self.assertEqual(result, expect)

    def test_US20(self):  # Aunts and uncles
        repo = Repo()
        repo.read_file("ged/test_yz.ged")
        result = repo.US20()
        expect = {'F5'}
        self.assertEqual(result, expect)

    def test_US21(self):
        repo = Repo()
        repo.read_file("ged/My-Family-28-Oct-2019-667.ged")
        self.assertNotEqual(repo.US21(), list())

    def test_US22(self):
        repo = Repo()
        repo.read_file("ged/myfamily.ged")
        self.assertNotEqual(repo.US22(), list())

    def test_US29(self):  # List deceased
        repo = Repo()
        repo.read_file("ged/test_yz.ged")
        result = repo.US29()
        expect = {'I1', 'I5'}
        self.assertEqual(result, expect)

    def test_US30(self):  # List living married
        repo = Repo()
        repo.read_file("ged/test_yz.ged")
        result = repo.US30()
        expect = {'I2', 'I3', 'I4', 'I6', 'I7', 'I8', 'I9', 'I10'}
        self.assertEqual(result, expect)


    """Test for sprint3: US35 & US25- By Tanvi"""

    def test_US25(self):
        repo = Repo()
        repo.read_file("ged/myfamily.ged")
        self.assertEqual(repo.US25(), [['Surinder '], ['Nirmal '], ['Boney '], ['Sridevi '], ['Anil '], ['Sunita '], ['Sanjay '], ['Maheep '], ['Sonam '], ['Rhea '], ['Harshvardhan '], [
                         'Shanaya '], ['Jahaan '], ['Mona '], ['Arjun '], ['Anshula '], ['Khushi '], ['Janhvi '], ['John '], ['Allen '], ['Lily '], ['Vu '], ['Sue '], ['Shilpy '], ['Das '], ['Deepa ']])

    def test_US35(self):
        repo = Repo()
        repo.read_file("ged/My-Family-29-Oct-2019-793.ged")
        self.assertEqual(repo.US35(), ['@I27@'])


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
