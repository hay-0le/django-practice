# import requests
import os
import json

from django.shortcuts import get_object_or_404
# from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from datetime import datetime
from django.conf import settings

from .models import StarredCity 

#Convert date/time from unix to YYYY:MM:DD HH:MM:SS format
def formatTime(unix_time):
    date_time = datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d %H:%M:%S')

    date, sep, time = date_time.partition(' ')

    return {
        "date": date,
        "time": time
    }
    

#get full state name
def getStateName(state_initials):
    state = state_initials.upper()

    states = {
        "AL": "Alabama",
        "AK": "Alaska",
        "AZ": "Arizona",
        "AR": "Arkansas",
        "CA": "California",
        "CO": "Colorado",
        "CT": "Connecticut",
        "DE": "Delaware",
        "FL": "Florida",
        "GA": "Georgia",
        "HI": "Hawaii",
        "ID": "Idaho",
        "IL": "Illinois",
        "IN": "Indiana",
        "IA": "Iowa",
        "KS": "Kansas",
        "KY": "Kentucky",
        "LA": "Louisiana",
        "ME": "Maine",
        "MD": "Maryland",
        "MA": "Massachusetts",
        "MI": "Michigan",
        "MN": "Minnesota",
        "MS": "Mississippi",
        "MO": "Missouri",
        "MT": "Montana",
        "NE": "Nebraska",
        "NV": "Nevada",
        "NH": "New Hampshire",
        "NJ": "New Jersey",
        "NM": "New Mexico",
        "NY": "New York",
        "NC": "North Carolina",
        "ND": "North Dakota",
        "OH": "Ohio",
        "OK": "Oklahoma",
        "OR": "Oregon",
        "PA": "Pennsylvania",
        "RI": "Rhode Island",
        "SC": "South Carolina",
        "SD": "South Dakota",
        "TN": "Tennessee",
        "TX": "Texas",
        "UT": "Utah",
        "VT": "Vermont",
        "VA": "Virginia",
        "WA": "Washington",
        "WV": "West Virginia",
        "WI": "Wisconsin",
        "WY": "Wyoming",
    }

    return states.get(state, "error")


def add_city_coordinates(coordinates, city_name):

    path_to_coordinates = os.path.join( settings.BASE_DIR, 'static/data/coordinates.geojson' )

    with open(path_to_coordinates) as f:
        data = json.load(f)
    
    #TODO Use geojson package to format instead (this does the job correctly for now)
    feature = {
        'type': 'Feature',
        'geometry': {
            'type': 'Point',
            'coordinates': coordinates,
        },
        'properties': {
            'message': city_name,
            'is_home': False,
            "iconSize": [40, 40]
        }
    }

    data['features'].append(feature)

    with open(path_to_coordinates, 'w') as f:
        f.write(json.dumps(data))


#Update home city
def make_home(city_id):
    
    #Reset old home city is_home to false
    if StarredCity.objects.filter(is_home=True).exists():
        StarredCity.objects.filter(is_home=True).update(is_home=False)
  
    #update city at city_id to home
    new_home = get_object_or_404(StarredCity, pk=city_id)
    new_home.is_home=True
    new_home.save()

