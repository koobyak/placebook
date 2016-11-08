import colander
import deform.widget

from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from google_maps_geocoding import GoogleMapsGeocoding

class SearchQuery(colander.MappingSchema):
    """
    For user to enter an address and select a distance from the homepage.
    """
    address = colander.SchemaNode(
        colander.String(),
        title = 'Address',
        description = 'Enter an exact address or a city name.'
    )

    distance_values = [
        # (value_passed, display_name)
        (25, '25'),
        (50, '50'),
        (100, '100')
    ]
    distance = colander.SchemaNode(
        colander.Int(),
        # TODO: which range is best?
        validator = colander.Range(0, 9999),
        title = 'Distance',
        description = 'Select a max distance from your address.',
        widget = deform.widget.SelectWidget(values = distance_values)
    )
        # TODO: in kilometers or miles?


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
        gmaps = GoogleMapsGeocoding(address)
        coords = gmaps.get_coordinates()
        latitude = coords['lat']
        longitude = coords['lng']
        return dict(address = address, 
            distance = distance,
            latitude = latitude,
            longitude = longitude,
        )
