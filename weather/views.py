import requests
import os

from decouple import config
from django.shortcuts import render

from .forms import CityForm
from .models import StarredCity 
from .utils import formatTime, getStateName, add_city_coordinates, make_home
# import .models import CityWeatherData


#View for main page to render, add cities
def index(request, city_id = False):
    API_KEY = config("API_KEY")
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=' + API_KEY
   
   #If city_id passed in, update that city as home
    if city_id:
        make_home(city_id)

    if request.method == 'POST':
        #TODO When user adds first city, should coordinates.geojson file be created then? Or set up project with empty features collection template
        form = CityForm(request.POST)
        
        if form.is_valid():
            new_city, sep, state = form.cleaned_data['city_name'].partition(',')
        
            #Openweathermaps api doesn't take in state abbreviations
            #So if user provides input in that format, update state to full state name
            #TODO figure out why this conditional works in an interpreter but not in here
            if len(state) and len(state) < 3:
                state = getStateName(state)

            r = requests.get(url.format(new_city)).json()
            #TODO handle error if city does not exist to let the user know

            city_obj = StarredCity(city_name=r['name'], city_id=r['id'])
            city_obj.save()

            add_city_coordinates([r['coord']['lon'], r['coord']['lat']], r['name'])

    form = CityForm()

    starred_cities_list = StarredCity.objects.order_by('-is_home')
    cities_weather_data = []

    for city in starred_cities_list:
        #Get city data from api
        r = requests.get(url.format(city.city_name)).json()

        #TODO add mapbox access code to env and pass it in from view
        city_weather = {
            'city': city.city_name.capitalize(),
            'city_id': city.city_id,
            'is_home': city.is_home,
            'temperature': round(r['main']['temp'], 1),
            'icon': r['weather'][0]['icon'],
            'map-api-key': config("GOOGLE_API_KEY"),
            'coordinates': {
                'lat': r['coord']['lat'],
                'lon': r['coord']['lon']
            }
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
        'description': r['weather'][0]['description'].capitalize(),
        'temperature': round(r['main']['temp'], 1),
        'temperature_min': round(r['main']['temp_min'], 1),
        'temperature_max': round(r['main']['temp_max'], 1),
        'temperature_feels_like': round(r['main']['feels_like'], 1),
        'clouds': r['clouds']['all'],
        'pressure': r['main']['pressure'],
        'humidity': r['main']['humidity'],
        'icon': r['weather'][0]['icon'],
        'sunrise': formatTime(r['sys']['sunrise'])['time'],
        'sunset': formatTime(r['sys']['sunset'])['time'],
        'date': formatTime(r['sys']['sunset'])['date'],
        'hireability': 'High',
    }

    return render(request, 'weather/citydata.html', { 'city_data': city_data})
