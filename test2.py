import unittest
import main2
from main2 import Repo

class UserStoryTest(unittest.TestCase):
    
    """US03"""
    def test_validate_death_after_birth(self):
        """US03 - Birth before Death of Individual"""
        path = 'Das.ged'
        repo = Repo()
        repo.read_file(path)
        self.assertEqual(repo.validate_death_after_birth(), True)
        self.assertNotEqual(repo.validate_death_after_birth(), False)
        self.assertTrue(repo.validate_death_after_birth())

    """US04"""

    def test_validate_family_marriage_before_divorce(self):
        """US04	Marriage before divorce"""
        path = 'Das.ged'
        repo = Repo()
        repo.read_file(path)
        self.assertEqual(repo.validate_family_marriage_before_divorce(), True)
        self.assertNotEqual(repo.validate_family_marriage_before_divorce(), False)
        self.assertTrue(repo.validate_family_marriage_before_divorce())

    """US13"""

    def test_validate_sibling_spacing(self):
        """US13 - Birth Dates of Sibilings should be more than 8 months apart or less than 2 days apart"""
        path = 'Das.ged'
        repo = Repo()
        repo.read_file(path)
        self.assertEqual(repo.validate_sibiling_spacing(), True)
        self.assertNotEqual(repo.validate_sibiling_spacing(), False)
        self.assertTrue(repo.validate_sibiling_spacing())

    """US14"""

    def test_validate_multiple_births(self):
        """US14 - Multiple births <= 5"""
        path = 'Das.ged'
        repo = Repo()
        repo.read_file(path)
        self.assertEqual(repo.validate_multiple_births(), True)
        self.assertNotEqual(repo.validate_multiple_births(), False)
        self.assertTrue(repo.validate_multiple_births())

if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)