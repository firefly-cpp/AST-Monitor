import os
from unittest import TestCase

from sport_activities_features.tcx_manipulation import TCXFile


class TestTCXFile(TestCase):
    def setUp(self):
        filename = os.path.join(
            os.path.dirname(__file__),
            'test_data',
            '15.tcx'
        )
        self.tcx_file = TCXFile()
        self.tcx_exercise = self.tcx_file.read_one_file(filename)
        self.data = self.tcx_file.extract_activity_data(self.tcx_exercise)
    def test_total_distance(self):
        self.assertAlmostEqual(self.data['total_distance'], 116366.98, 2)

    def test_number_of_positions(self):
        self.assertEqual(len(self.data['positions']), 7799)

    def test_heartrates(self):
        if 'heartrates' in self.data:
            self.assertEqual(self.data['heartrates'][0], 94)
            self.assertEqual(self.data['heartrates'][1], 95)
