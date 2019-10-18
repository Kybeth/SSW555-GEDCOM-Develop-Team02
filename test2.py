import unittest
import main2
from main2 import Repo

class UserStoryTest(unittest.TestCase):
    
    """US03"""
    def test_US03(self):
        """US03 - Birth before Death of Individual"""
        path = 'Das.ged'
        repo = Repo()
        repo.read_file(path)
        self.assertEqual(repo.US03(), True)
        self.assertNotEqual(repo.US03(), False)
        self.assertTrue(repo.US03())

    """US04"""

    def test_US04(self):
        """US04	Marriage before divorce"""
        path = 'Das.ged'
        repo = Repo()
        repo.read_file(path)
        self.assertEqual(repo.US04(), True)
        self.assertNotEqual(repo.US04(), False)
        self.assertTrue(repo.US04())

    """US13"""

    def test_validate_sibling_spacing(self):
        """US13 - Birth Dates of Sibilings should be more than 8 months apart or less than 2 days apart"""
        path = 'Das.ged'
        repo = Repo()
        repo.read_file(path)
        self.assertEqual(repo.US13(), True)
        self.assertNotEqual(repo.US13(), False)
        self.assertTrue(repo.US13())

    """US14"""

    def test_US14(self):
        """US14 - Multiple births <= 5"""
        path = 'Das.ged'
        repo = Repo()
        repo.read_file(path)
        self.assertEqual(repo.US14(), True)
        self.assertNotEqual(repo.US14(), False)
        self.assertTrue(repo.US14())

if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)