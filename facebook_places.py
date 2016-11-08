#!/usr/bin/env python
import config
import facebook

class FacebookPlaces(object):
    def __init__(self, coordinates, distance):
        self.api_key = config.facebook_api['api_key']
        self.coordinates = coordinates
        self.distance = distance

    def get_nearby_places(self):
    	# version 2.8 is the newest, but not fully supported yet
        graph = facebook.GraphAPI(access_token = self.api_key, version = '2.7')
        # we will pass lat and long into query as strings
        coordinates = '%s, %s' % (str(self.coordinates['lat']), str(self.coordinates['lng']))
        # the metadata of the page we're interested in
        fields = 'id, location, name, checkins, fan_count, category'
        results = graph.get_object(
        	'search',
            q = '',
            type = 'place', 
            center = coordinates,
            distance = str(self.distance),
            fields = fields
        )
        return results
