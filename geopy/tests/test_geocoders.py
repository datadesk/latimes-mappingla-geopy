#!/usr/bin/env python
import unittest
from geopy import geocoders


class BaseTest(unittest.TestCase):
    
    def setUp(self):
        self.GOOGLE_API_KEY = 'ABQIAAAAGhi-W_UrhAbJd_oyDNEvcxTi5SvYvSQHL9wSA8Ar43CRRnpzhBQ_yTB7UeJHK00rUynRE4eLdUJp0Q'
        self.google = geocoders.Google(self.GOOGLE_API_KEY)


class GoogleTest(BaseTest):
    
    def test_search(self):
        result = self.google.geocode("Winnetka")
        self.assertEqual(result, (u'Winnetka, IL, USA', (42.1080834, -87.735895)))
    
    def test_return_accuracy(self):
        result = self.google.geocode("Winnetka", return_accuracy=True)
        self.assertEqual(result, (u'Winnetka, IL, USA', (42.1080834, -87.735895), u'4'))
    
    def test_exactly_one(self):
        self.assertRaises(ValueError, self.google.geocode, "Paris")
        results = self.google.geocode("Paris", exactly_one=False)
        self.assertEqual(len(list(results)), 6)
    
    def test_viewport_bias(self):
        result = self.google.geocode("Winnetka", bounding_box=((34.172684,-118.604794), (34.236144,-118.500938)))
        print result

if __name__ == '__main__':
    unittest.main()

