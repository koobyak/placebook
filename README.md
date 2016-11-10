# placebook

Give me your favorite city, I'll give you Facebook pages around you.

You can check out the number of people that liked the page, the number of people who checked in there, see a little profile pic, and click the link to take you to the page.

Mark Zuckerburg, if you're reading this, please don't sue. :+1:

What I used:
 * [Pyramid](http://www.pylonsproject.org/) for back-end
 * [Deform](http://docs.pylonsproject.org/projects/deform/en/latest/) for forms and [Colander schemas](http://docs.pylonsproject.org/projects/colander/en/latest/) for their validation
 * [Leaflet.js](http://leafletjs.com/) to plot points on maps
 * [Mapbox](https://www.mapbox.com/) for map engine
 * [GoogleMaps Python client](https://github.com/googlemaps/google-maps-services-python) for getting GPS coordinates
 * [Facebook Python SDK](https://github.com/mobolic/facebook-sdk) for the obvious stuff

### Now, to get this thing to work:
Do the following.
1. Create a config.py file for reading your API keys. The common practice is to embed them as environment variables in your local system. Maybe something like: 
```python
GOOGLEMAPS_API_KEY = os.environ['GOOGLEMAPS_API_KEY']
googlemaps_api = {
    'api_key' : GOOGLEMAPS_API_KEY
}
```
2. Create a virtual env and
```unix
$ path/to/env/bin/pip install -e .
```
which will install Pyramid and all our other dependencies from setup.py.
3. After the egg is created, you should be able to 
```unix
$ path/to/env/bin/pserve development.ini --reload
```

Try typing in "Paris" or "Nice, France" or an exact address. Then select a distance and see what you get.# placebook
