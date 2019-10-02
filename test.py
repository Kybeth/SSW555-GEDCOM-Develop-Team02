import unittest
from main import parse_file


class UserStoryTest(unittest.TestCase):

    def test_test(self):
        self.assertEqual('foo'.upper(), 'FOO')


unittest.main(exit=False, verbosity=2)
