import requests
import os
from decouple import config
from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import HttpResponseRedirect
from .models import StarredCity, CityWeatherData
from .forms import CityForm

# API_KEY = config("API_KEY")

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

#Search Cities
def index(request):
    API_KEY = config("API_KEY")
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=' + API_KEY
   
    if request.method == 'POST':
        form = CityForm(request.POST)
        
        if form.is_valid():
            new_city, sep, state = form.cleaned_data['city_name'].partition(',')
        
            #openweathermaps api doesn't take in state abbreviations, so if user provides input that way, find full state name
            #TODO why you no work?
            if len(state) and len(state) < 3:
                state = getStateName(state)

            city_obj = StarredCity(city_name=new_city)

            city_obj.save()
            # return HttpResponseRedirect('/weather')

        #TODO form reset, but still sending duplicates to db
    form = CityForm()
    print("resetting form", form)

    starred_cities_list = StarredCity.objects.order_by('-city_name')
    cities_weather_data = []

    for city in starred_cities_list:
        r = requests.get(url.format(city.city_name)).json()

        city_weather = {
            'city': city.city_name.capitalize(),
            'city_id': r['id'],
            'temperature': round(r['main']['temp'], 1),
            'icon': r['weather'][0]['icon'],
            # 'isHome': city.isHome,
        }

        cities_weather_data.append(city_weather)

    context = {'cities_weather_data': cities_weather_data, 'form': form}
    return render(request, 'weather/index.html', context)

#Show detailed weather data for chosen city
def city_weather_details(request, city_id):
    API_KEY = config("API_KEY")

    url = 'http://api.openweathermap.org/data/2.5/weather?id={}&units=imperial&appid=' + API_KEY
    

    r = requests.get(url.format(city_id)).json()

    coordinates = {
        'lat': r['coord']['lat'],
        'lon': r['coord']['lon']
    }

    city_data = {
        'city_id': city_id,
        'city_name': r['name'],
        'country': r['sys']['country'],
        'description': r['weather'][0]['description'],
        'temperature': round(r['main']['temp'], 1),
        'temperature_min': round(r['main']['temp_min'], 1),
        'temperature_max': round(r['main']['temp_max'], 1),
        'temperature_feels_like': round(r['main']['feels_like'], 1),
        'clouds': r['clouds']['all'],
        # 'rainfall_3h': r['rain']['3h'],
        # 'snowfall_3h': r['snow']['3h'],
        'pressure': round(r['main']['pressure'], 1),
        'humidity': round(r['main']['humidity'], 1),
        'icon': r['weather'][0]['icon'],
        'sunrise': r['sys']['sunrise'],
        'sunset': r['sys']['sunset'],

    }

    return render(request, 'weather/citydata.html', { 'city_data': city_data})
