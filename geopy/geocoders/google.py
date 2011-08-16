from urllib import urlencode
from urllib2 import urlopen
try:
    import json as simplejson
except ImportError:
    import simplejson

import xml
from xml.parsers.expat import ExpatError

from geopy.geocoders.base import Geocoder,GeocoderError,GeocoderResultError
from geopy import Point, Location, util


class Google(Geocoder):
    """Geocoder using the Google Maps API."""
    
    def __init__(self, domain='maps.googleapis.com', resource='maps/api/geocode',
        format_string='%s', output_format='json', sensor='false'):
        """Initialize a customized Google geocoder with location-specific
        address information and your Google Maps API key.

        ``api_key`` should be a valid Google Maps API key. It is required for
        the 'maps/geo' resource to work.

        ``domain`` should be a the Google Maps domain to connect to. The default
        is 'maps.google.com', but if you're geocoding address in the UK (for
        example), you may want to set it to 'maps.google.co.uk'.

        ``resource`` is the HTTP resource to give the query parameter.
        'maps/geo' is the HTTP geocoder and is a documented API resource.
        'maps' is the actual Google Maps interface and its use for just
        geocoding is undocumented. Anything else probably won't work.

        ``format_string`` is a string containing '%s' where the string to
        geocode should be interpolated before querying the geocoder.
        For example: '%s, Mountain View, CA'. The default is just '%s'.
        
        ``output_format`` can be 'json', 'xml', 'kml', 'csv', or 'js' and will
        control the output format of Google's response. The default is 'kml'
        since it is supported by both the 'maps' and 'maps/geo' resources. The
        'js' format is the most likely to break since it parses Google's
        JavaScript, which could change. However, it currently returns the best
        results for restricted geocoder areas such as the UK.
        """
        self.domain = domain
        self.resource = resource
        self.format_string = format_string
        self.output_format = output_format
        self.sensor = sensor
    
    @property
    def url(self):
        domain = self.domain.strip('/')
        resource = "%s/%s" % (
            self.resource.strip('/'),
            self.output_format.lower(),
        )
        return "http://%(domain)s/%(resource)s?%%s" % locals()
    
    def geocode(self, string, exactly_one=True, return_types=False,
        bounding_box=None, region=None):
        """
        Hit the API and get the response from Google.

        ``exactly_one`` will limit the search results to only one result.

        ``return_accuracy`` will add Google's accuracy score to the result,
        so you can tell at what level of precision in each match.

        http://code.google.com/apis/maps/documentation/javascript/v2/reference.html#GGeoAddressAccuracy

        ``bounding box`` should be a pairs of tuples that contains, each
        containing a longitude and latitude pair or use in the Google Maps API V3 version of
        viewport biasing. The first tuple should be the southwest corner and
        the second should be the northeast corner.
        
        Google's example, creating a box around the San Fernando Valley, would be
        submitted as follows:
        
            bounding_box=((34.172684,-118.604794), (34.236144,-118.500938))
        
        More information about viewport biasing is here:
        
            http://code.google.com/apis/maps/documentation/geocoding/#Viewports
        """
        # Add parameters to URL
        params = {
            'address': self.format_string % string,
            'sensor': self.sensor,
        }
        url = self.url % urlencode(params)
        
        # If the user has submitted a bounding box for viewport biasing...
        if bounding_box:
            # .. make sure it's decent...
            if len(bounding_box) != 2:
                raise ValueError("You have submitted a bad bounding box.")
            # ... then tack it on the end.
            url += "&bounds=%s,%s" % (bounding_box[0][0], bounding_box[0][1])
            url += "|%s,%s" % (bounding_box[1][0], bounding_box[1][1])
        if region:
            url += "&region=%s" % region.lower()
        # Pass out the finished url
        return self.geocode_url(url, exactly_one, return_types)

    def geocode_url(self, url, exactly_one=True, return_types=False):
        util.logger.debug("Fetching %s..." % url)
        page = urlopen(url)
        dispatch = getattr(self, 'parse_' + self.output_format)
        return dispatch(page, exactly_one, return_types)

    def parse_xml(self, page, exactly_one=True, return_types=False):
        raise NotImplementedError

    def parse_csv(self, page, exactly_one=True):
        raise NotImplementedError

    def parse_kml(self, page, exactly_one=True, return_accuracy=False):
        raise NotImplementedError

    def parse_json(self, page, exactly_one=True, return_types=False):
        if not isinstance(page, basestring):
            page = util.decode_page(page)
        json = simplejson.loads(page)
        places = json.get('results', [])

        if len(places) == 0:
            # Got empty result. Parse out the status code and raise an error if necessary.
            status = json.get("status", None)
            self.check_status_code(status_code)

        if exactly_one and len(places) != 1:
            raise ValueError("Didn't find exactly one placemark! " \
                             "(Found %d.)" % len(places))

        def parse_place(place):
            location = place.get('formatted_address')
            longitude, latitude = place['geometry']['location']['lng'], place['geometry']['location']['lat']
            if return_types:
                accuracy = place['types']
                return (location, (latitude, longitude), accuracy)
            else:
                return (location, (latitude, longitude))

        
        if exactly_one:
            return parse_place(places[0])
        else:
            return (parse_place(place) for place in places)

    def parse_js(self, page, exactly_one=True):
        raise NotImplementedError

    def check_status_code(self, status_code):
        if status_code == "ZERO_RESULTS":
            raise GQueryError("No corresponding geographic location could be found for the specified location, possibly because the address is relatively new, or because it may be incorrect.")
        elif status_code == "REQUEST_DENIED":
            raise GQueryError("Your request was denied, generally because of lack of a sensor parameter.")
        elif status_code == "INVALID_REQUEST":
            raise GQueryError("You request did not include an address or latlng.")
        elif status_code == "OVER_QUERY_LIMIT":
            raise GTooManyQueriesError("The given key has gone over the requests limit in the 24 hour period or has submitted too many requests in too short a period of time.")


class GQueryError(GeocoderResultError):
    pass


class GTooManyQueriesError(GeocoderResultError):
    pass
