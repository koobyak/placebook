import colander
import deform.widget

from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

import api_resources

class SearchQuery(colander.MappingSchema):
    """
    For user to enter an address and select a distance from the homepage.
    """
    address = colander.SchemaNode(
        colander.String(),
        title = 'Address',
        description = 'Enter a city name or an exact address.'
    )

    distance_values = [
        # (value in meters, display_name)
        (1000, '1 km'),
        (2000, '2 km'),
        (3000, '3 km'),
        (5000, '5 km'),
        (10000, '10 km')
    ]
    distance = colander.SchemaNode(
        colander.Int(),
        # TODO: which range is best?
        validator = colander.Range(0, 99999),
        title = 'Distance',
        description = 'Select a max distance from your address in kilometers.',
        widget = deform.widget.SelectWidget(values = distance_values)
    )

class PlacebookViews(object):
    def __init__(self, request):
        self.request = request

    @property
    def placebook_form(self):
        schema = SearchQuery()
        return deform.Form(schema, buttons=('submit',))

    # this is called by chameleon in our template to pull appropriate CSS, JS resources for Deform
    @property
    def reqts(self):
        return self.placebook_form.get_widget_resources()

    @view_config(route_name='homepage', renderer='static/homepage.pt')
    def homepage(self):
        form = self.placebook_form.render()
        # check if form was submitted with POST action
        if 'submit' in self.request.params:
            form_values = self.request.POST.items()
            try:
                # with Deform we get validation according to Colander schema for free
                validated = self.placebook_form.validate(form_values)
            except deform.ValidationFailure as e:
                return dict(form = e.render())

            # Form is valid, get our values and build query string
            address = validated['address']
            distance = validated['distance']

            # redirect to map with parameters in query string ('GET')
            url = self.request.route_url(
                'map',
                _query=(
                    ('address', address),
                    ('distance', distance)
                )
            )
            return HTTPFound(location = url)

        return dict(form=form)

    @view_config(route_name='map', renderer='static/map.pt')
    def map_view(self):
        address = self.request.params['address']
        distance = self.request.params['distance']
        gmaps = api_resources.GoogleMapsGeocoding(address)
        coords = gmaps.get_coordinates()
        latitude = coords['lat']
        longitude = coords['lng']
        facebook = api_resources.FacebookPlaces(coords, distance)
        geojson = facebook.get_nearby_places_as_geojson()
        return dict(address = address, 
            distance = distance,
            latitude = latitude,
            longitude = longitude,
            geojson = geojson
        )
