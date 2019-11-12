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

    '''
    def test_US11(self):
        repo = Repo()
        repo.read_file('ged/My-Family-29-Oct-2019-620.ged')
        self.assertEqual(repo.US11(), ['@F9@'])
    '''

    def test_US21(self):
        repo = Repo()
        repo.read_file("ged/das.ged")
        self.assertNotEqual(repo.US21(), list())

    def test_US22(self):
        repo = Repo()
        repo.read_file('ged/My-Family.ged')
        self.assertNotEqual(repo.US22(), True)

    '''
    def test_US31(self):
        repo = Repo()
        repo.read_file('ged/My-Family.ged')
        result = repo.US31()
        
        expect = {'Surinder /Kapoor/', 'Nirmal /Kapoor/', 'Boney /Kapoor/', 'Sridevi /Kapoor/', 'Anil /Kapoor/', 'Sunita /Kapoor/', 
        'Sanjay /Kapoor/', 'Maheep /Sandhu/', 'Sonam /Kapoor/', 'Rhea /Kapoor/', 'Harshvardhan /Kapoor/', 'Shanaya /Kapoor/', 
        'Jahaan /Kapoor/', 'Mona /Shourie/', 'Arjun /Kapoor/', 'Anshula /Kapoor/', 'Khushi /Kapoor/', 'Janhvi /Kapoor/', 
        'John /Kapoor/', 'Allen /Kapoor/', 'Lily /Kapoor/', 'Vu /Kapoor/', 'Sue /Kapoor/', 'Shilpy /Kapoor/', 'Das /Kapoor/', 
        'Deepa /Kapoor/', 'Shreya /Kapoor/', 'SImmi /Kapoor/'}
        self.assertEqual(result, expect)
        
        self.assertEqual(repo.US31(), [['ERROR US31', '@F13@'], ['ERROR US31', '@F13@'], ['ERROR US31', '@F13@'], ['ERROR US31', '@F13@'], ['ERROR US31', '@F13@'], ['ERROR US31', '@F13@'], ['ERROR US31', '@F13@'], ['ERROR US31', '@F13@'], ['ERROR US31', '@F13@'], ['ERROR US31', '@F13@'], ['ERROR US31', '@F13@'], ['ERROR US31', '@F13@'], ['ERROR US31', '@F13@'], ['ERROR US31', '@F13@'], ['ERROR US31', '@F13@'], ['ERROR US31', '@F13@'], ['ERROR US31', '@F13@'], ['ERROR US31', '@F13@'], ['ERROR US31', '@F13@'], ['ERROR US31', '@F13@'], ['ERROR US31', '@F13@'], ['ERROR US31', '@F13@'], ['ERROR US31', '@F13@'], ['ERROR US31', '@F13@'], ['ERROR US31', '@F13@'], ['ERROR US31', '@F13@'], ['ERROR US31', '@F13@'], ['ERROR US31', '@F13@'], ['ERROR US31', '@F13@'], ['ERROR US31', '@F13@'], ['ERROR US31', '@F13@'], ['ERROR US31', '@F13@'], ['ERROR US31', '@F13@'], ['ERROR US31', '@F13@'], ['ERROR US31', '@F13@'], ['ERROR US31', '@F13@'], ['ERROR US31', '@F13@'], ['ERROR US31', '@F13@'], ['ERROR US31', '@F13@'], ['ERROR US31', '@F13@'], ['ERROR US31', '@F13@'], ['ERROR US31', '@F13@'], ['ERROR US31', '@F13@'], ['ERROR US31', '@F13@'], ['ERROR US31', '@F13@'], ['ERROR US31', '@F13@'], ['ERROR US31', '@F13@'], ['ERROR US31', '@F13@'], ['ERROR US31', '@F13@'], ['ERROR US31', '@F13@'], ['ERROR US31', '@F13@'], ['ERROR US31', '@F13@'], ['ERROR US31', '@F13@'], ['ERROR US31', '@F13@'], ['ERROR US31', '@F13@'], ['ERROR US31', '@F13@']])
    '''

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

    '''
    def test_US33(self):  # orphans
        repo = Repo()
        repo.read_file("ged/My-Family.ged")
        result = repo.US33()
        expect = {'@I8@',
                  '@I19@'
                  '@I16@'
                  '@I20@'
                  '@I26@'
                  '@I10@'
                  '@I15@'
                  '@I21@'
                  '@I18@'
                  '@I27@'
                  '@I12@'
                  '@I9@'
                  '@I25@'
                  '@I28@'
                  '@I17@'
                  '@I24@'
                  '@I11@'
                  '@I23@'
                  '@I13@'
                  '@I3@'
                  '@I5@'
                  '@I6@'}
        self.assertEqual(result, expect)

    def test_US34(self):

        repo = Repo()
        repo.read_file("ged/das.ged")
        self.assertEqual(repo.US34(), True)
    '''

    """Lifu Xiao"""

    def test_US07(self):
        repo = Repo()
        repo.read_file("ged/My-Family.ged")
        self.assertEqual(repo.US07(), ['@I22@', '@I24@', '@I25@'])
    '''
    def test_US08(self):
        repo = Repo()
        repo.read_file("ged/My-Family.ged")
        self.assertEqual(repo.US08(), ['@I1@', '@I24@', '@I28@', '@I301@'])

    
    def test_US17(self):
        repo = Repo()
        repo.read_file("ged/My-Family.ged")
        self.assertEqual(repo.US17(), ['@I101@', '@I301@'])
    '''

    def test_US18(self):
        repo = Repo()
        repo.read_file("ged/My-Family.ged")
        self.assertEqual(repo.US18(), ['@I12@', '@I13@', '@I15@', '@I16@'])

    '''
    def test_US27(self):
        repo = Repo()
        repo.read_file("ged/My-Family.ged")
        a = repo.US27()
        self.assertEqual(repo.US27(),  ['@I101@'])
    '''

    def test_US28(self):
        repo = Repo()
        repo.read_file("ged/My-Family.ged")
        self.assertEqual(repo.US28()[0], [(26, '@I16@'), (34, '@I15@')])
        self.assertEqual(repo.US28()[1], [
                         (-2982, '@I5@'), (7, '@I21@'), (36, '@I3@'), (54, '@I7@')])

    def test_US37(self):
        repo = Repo()
        repo.read_file("ged/My-Family.ged")
        self.assertEqual(repo.US37(), ['@I7@'])

    def test_US38(self):
        repo = Repo()
        repo.read_file("ged/My-Family.ged")
        self.assertEqual(repo.US38(), ['@I13@'])

    """Yuan Zhang"""

    def test_US09(self):  # Birth before death of parents
        repo = Repo()
        repo.read_file("ged/My-Family.ged")
        result = repo.US09()
        expect = {'@I21@', '@I20@', '@I5@'}
        self.assertEqual(result, expect)

    def test_US10(self):  # Marriage after 14
        repo = Repo()
        repo.read_file("ged/My-Family.ged")
        result = repo.US10()
        expect = {'@I5@', '@I20@', '@I15@', '@I21@', '@I26@', '@I2@',
                  '@I1@', '@I19@', '@I18@', '@I23@', '@I14@', '@I3@'}
        self.assertEqual(result, expect)

    def test_US19(self):  # First cousins should not marry
        repo = Repo()
        repo.read_file("ged/My-Family.ged")
        result = repo.US19()
        expect = {'@F8@', '@F13@', '@F11@', '@F9@'}
        self.assertEqual(result, expect)

    def test_US20(self):  # Aunts and uncles
        repo = Repo()
        repo.read_file("ged/My-Family.ged")
        result = repo.US20()
        expect = {'@F13@'}
        self.assertEqual(result, expect)

    def test_US29(self):  # List deceased
        repo = Repo()
        repo.read_file("ged/My-Family.ged")
        result = repo.US29()
        expect = {'@I14@', '@I28@', '@I1@', '@I2@', '@I7@', '@I4@', '@I22@'}
        self.assertEqual(result, expect)

    def test_US30(self):  # List living married
        repo = Repo()
        repo.read_file("ged/My-Family.ged")
        result = repo.US30()
        expect = {'@I12@', '@I6@', '@I5@', '@I25@', '@I15@', '@I24@', '@I18@',
                  '@I16@', '@I21@', '@I29@', '@I26@', '@I19@', '@I20@', '@I13@'}
        self.assertEqual(result, expect)

    def test_US39(self):  # List living married
        repo = Repo()
        repo.read_file("ged/My-Family.ged")
        result = repo.US39()
        expect = {'@F11@', '@F13@'}
        self.assertEqual(result, expect)

    def test_US40(self):  # List living married
        repo = Repo()
        repo.read_file("ged/My-Family.ged")
        result = repo.US40()
        expect = 393
        self.assertEqual(result, expect)

    """By Tanvi"""

    def test_US05(self):
        repo = Repo()
        repo.read_file('ged/My-Family.ged')
        self.assertEqual(repo.US05(), [['ANOMALY US05', '@I1@'], ['ANOMALY US05', '@I1@'], ['ANOMALY US05', '@I1@'], ['ANOMALY US05', '@I1@'], ['ANOMALY US05', '@I1@'], ['ANOMALY US05', '@I1@'], ['ANOMALY US05', '@I1@'], ['ANOMALY US05', '@I1@'], ['ANOMALY US05', '@I1@'], ['ANOMALY US05', '@I2@'], ['ANOMALY US05', '@I2@'], ['ANOMALY US05', '@I2@'], ['ANOMALY US05', '@I2@'], ['ANOMALY US05', '@I2@'], ['ANOMALY US05',
                                                                                                                                                                                                                                                                                                                                                                                                                    '@I2@'], ['ANOMALY US05', '@I2@'], ['ANOMALY US05', '@I2@'], ['ANOMALY US05', '@I2@'], ['ANOMALY US05', '@I4@'], ['ANOMALY US05', '@I4@'], ['ANOMALY US05', '@I4@'], ['ANOMALY US05', '@I4@'],
                                       ['ANOMALY US05', '@I4@'], ['ANOMALY US05', '@I4@'], ['ANOMALY US05', '@I4@'], ['ANOMALY US05', '@I4@'], ['ANOMALY US05', '@I4@'], ['ANOMALY US05', '@I7@'], ['ANOMALY US05', '@I7@'], ['ANOMALY US05', '@I7@'], ['ANOMALY US05', '@I7@'], ['ANOMALY US05', '@I7@'], ['ANOMALY US05', '@I7@'], ['ANOMALY US05', '@I7@'], ['ANOMALY US05', '@I7@'], ['ANOMALY US05', '@I7@'], ['ANOMALY US05', '@I14@'], ['ANOMALY US05', '@I14@'], ['ANOMALY US05', '@I14@'], ['ANOMALY US05', '@I14@'], ['ANOMALY US05', '@I14@'], ['ANOMALY US05', '@I14@'], ['ANOMALY US05', '@I14@'], ['ANOMALY US05', '@I14@'], ['ANOMALY US05', '@I14@'], ['ANOMALY US05', '@I22@'], ['ANOMALY US05', '@I22@'], ['ANOMALY US05', '@I22@'], ['ANOMALY US05', '@I22@'], ['ANOMALY US05', '@I22@'], ['ANOMALY US05', '@I22@'], ['ANOMALY US05', '@I22@'], ['ANOMALY US05', '@I22@'], ['ANOMALY US05', '@I22@'], ['ANOMALY US05', '@I28@'], ['ANOMALY US05', '@I28@'], ['ANOMALY US05', '@I28@'], ['ANOMALY US05', '@I28@'], ['ANOMALY US05', '@I28@'], ['ANOMALY US05', '@I28@'], ['ANOMALY US05', '@I28@'], ['ANOMALY US05', '@I28@'], ['ANOMALY US05', '@I28@']])

    def test_US06(self):
        repo = Repo()
        repo.read_file('ged/My-Family.ged')
        self.assertEqual(repo.US06(), [['ANOMALY US06', '@I1@'], ['ANOMALY US06', '@I2@'], ['ANOMALY US06', '@I4@'], [
                         'ANOMALY US06', '@I7@'], ['ANOMALY US06', '@I14@'], ['ANOMALY US06', '@I22@'], ['ANOMALY US06', '@I28@']])

    def test_US15(self):
        repo = Repo()
        repo.read_file('ged/My-Family.ged')
        self.assertEqual(repo.US15(), True)

    def test_US16(self):
        repo = Repo()
        repo.read_file('ged/My-Family.ged')
        self.assertEqual(repo.US16(), [['ANOMALY US16', '@I3@'], ['ANOMALY US16', '@I5@'], ['ANOMALY US16', '@I7@'], ['ANOMALY US16', '@I11@'], ['ANOMALY US16', '@I13@'], [
                         'ANOMALY US16', '@I15@'], ['ANOMALY US16', '@I19@'], ['ANOMALY US16', '@I20@'], ['ANOMALY US16', '@I22@'], ['ANOMALY US16', '@I24@'], ['ANOMALY US16', '@I25@']])

    def test_US25(self):
        repo = Repo()
        repo.read_file('ged/My-Family.ged')
        self.assertEqual(repo.US25(), [['Surinder '], ['Nirmal '], ['Boney '], ['Sridevi '], ['Anil '], ['Sunita '], ['Sanjay '], ['Maheep '], ['Sonam '], ['Rhea '], ['Harshvardhan '], ['Shanaya '], [
                         'Jahaan '], ['Mona '], ['Arjun '], ['Anshula '], ['Khushi '], ['Janhvi '], ['John '], ['Allen '], ['Lily '], ['Vu '], ['Sue '], ['Shilpy '], ['Das '], ['Deepa '], ['Shreya '], ['SImmi ']])
    # def test_US26(self):
    #     repo = Repo()
    #     repo.read_file("ged/My-Family-29-Oct-2019-793.ged")
    #     self.assertEqual(repo.US26(), )

    def test_US35(self):
        repo = Repo()
        repo.read_file('ged/My-Family.ged')
        self.assertEqual(repo.US35(), ['@I27@'])

    def test_US36(self):
        repo = Repo()
        repo.read_file('ged/My-Family.ged')
        self.assertEqual(repo.US36(), ['@I7@', '@I28@'])


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
