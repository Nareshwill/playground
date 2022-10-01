import unittest
import csv


class TestMain(unittest.TestCase):

    def test_similarity_longitudinal_acceleration(self):
        org_file = list(csv.DictReader(open('l1_longitudinal_acceleration.csv')))
        ccn_file = list(csv.DictReader(open('l1_longitudinal_acceleration_ccn.csv')))

        self.assertListEqual(org_file, ccn_file)

    def test_similarity_longitudinal_deceleration(self):
        org_file = list(csv.DictReader(open('l1_longitudinal_deceleration.csv')))
        ccn_file = list(csv.DictReader(open('l1_longitudinal_deceleration_ccn.csv')))

        self.assertListEqual(org_file, ccn_file)

    def test_similarity_longitudinal_jerk(self):
        org_file = list(csv.DictReader(open('l1_longitudinal_jerk.csv')))
        ccn_file = list(csv.DictReader(open('l1_longitudinal_jerk_ccn.csv')))

        self.assertListEqual(org_file, ccn_file)

    def test_similarity_false_indicator_check(self):
        org_file = list(csv.DictReader(open('l0_false_indicator_check.csv')))
        ccn_file = list(csv.DictReader(open('l0_false_indicator_check_ccn.csv')))

        self.assertListEqual(org_file, ccn_file)
