#!/usr/bin/env python
import unittest
from geopy import geocoders


class BaseTest(unittest.TestCase):
    
    def setUp(self):
        self.google = geocoders.Google()

class GoogleTest(BaseTest):
    
    def test_search(self):
        result = self.google.geocode("Winnetka")
        self.assertEqual(result, (u'Winnetka, IL, USA', (42.10808340000001, -87.735895)))
    
    def test_return_accuracy(self):
        result = self.google.geocode("Winnetka", return_types=True)
        self.assertEqual(result, (u'Winnetka, IL, USA', (42.10808340000001, -87.735895), [u'locality', u'political']))
    
    def test_exactly_one(self):
        self.assertRaises(ValueError, self.google.geocode, "Paris")
        results = self.google.geocode("Paris", exactly_one=False)
        self.assertEqual(len(list(results)), 6)
    
    def test_viewport_bias(self):
        result = self.google.geocode("Winnetka", bounding_box=((34.172684,-118.604794), (34.236144,-118.500938)))
        self.assertEqual(result, (u'Winnetka, Los Angeles, CA, USA', (34.2083333, -118.5752778)))

    def test_region_bias(self):
        result = self.google.geocode("Toledo", region='ES')
        self.assertEqual(result, (u'Toledo, Spain', (39.8567775, -4.0244759)))

if __name__ == '__main__':
    unittest.main()

