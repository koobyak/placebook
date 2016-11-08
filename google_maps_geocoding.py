#!/usr/bin/env python
import config
import googlemaps

class GoogleMapsGeocoding(object):
    def __init__(self, address):
        self.api_key = config.googlemaps_api['api_key']
        self.address = address

    def get_coordinates(self):
        gmaps = googlemaps.Client(key = self.api_key)
        geocoded = gmaps.geocode(self.address)
        first_result = geocoded[0]
        # returns dict with 'lat' and 'lng' keys
        geolocation = first_result['geometry']['location']
        return geolocation
