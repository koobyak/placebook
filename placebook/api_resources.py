#!/usr/bin/env python
import config
import facebook
import googlemaps
import json, requests

class GoogleMapsGeocoding(object):
    """
    Query GoogleMaps API with key in config.py to get geo coordinates of address.
    """
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

class FacebookPlaces(object):
    """
    Query Facebook API with key in config.py to return places a certain distance from geo center.
    """
    def __init__(self, coordinates, distance):
        self.api_key = config.facebook_api['api_key']
        self.coordinates = coordinates
        self.distance = distance

    def get_nearby_places_as_geojson(self):
    	# version 2.8 is the newest, but not fully supported yet
        graph = facebook.GraphAPI(access_token = self.api_key, version = '2.7')
        # we will pass lat and long into query as strings
        coordinates = '%s, %s' % (str(self.coordinates['lat']), str(self.coordinates['lng']))
        # the metadata of the page we're interested in
        fields = 'id, location, name, checkins, fan_count, category, picture'
        all_results = graph.get_object(
        	'search',
            q = '',
            type = 'place', 
            center = coordinates,
            distance = str(self.distance),
            fields = fields,
            # READ: Facebook Search API seems to cap out results around ~800 .. however it's not consistent
            # and no proper documentation found to confirm this. Capping at hard-coded 1000 search results.
            limit = 1000
        )
        results = all_results['data']
        geojson = facebook_places_results_to_geojson(results)
        return geojson

def facebook_places_results_to_geojson(results):
	# build according to geojson schema
	# see http://geojson.org/
    geojson = {}
    geojson['type'] = 'FeatureCollection'
    geojson['features'] = []
    features = geojson['features']
    for result in results:
        new_feature = create_geojson_feature(result) # returns dict like below
        features.append(new_feature)
    return json.dumps(geojson)

def create_geojson_feature(result):
    coordinates = []
    coordinates.extend((result['location']['longitude'], result['location']['latitude']))
    geometry = dict(
        type = 'Point', 
        coordinates = coordinates
    )
    properties = dict(
    	name = result['name'],
    	fbid = result['id'],
        popupContent = result['name'],
        likes = result['fan_count'],
        checkins = result['checkins'],
        picture = result['picture'],
        category = result['category']
    )
    # add everything above to feature
    feature = dict(
        type = 'Feature',
        geometry = geometry,
        properties = properties
    )
    return feature
