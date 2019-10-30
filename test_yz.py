#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
from main import Repo


class UserStoryTest(unittest.TestCase):

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


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
