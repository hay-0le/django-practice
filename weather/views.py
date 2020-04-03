import requests
import os

from decouple import config
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from datetime import datetime

from .forms import CityForm
from .models import StarredCity 
# import .models import CityWeatherData

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

#Update home city
def make_home(city_id):
    
    #Reset old home city is_home to false
    if StarredCity.objects.filter(is_home=True).exists():
        StarredCity.objects.filter(is_home=True).update(is_home=False)
  
    #update city at city_id to home
    new_home = get_object_or_404(StarredCity, pk=city_id)
    new_home.is_home=True
    new_home.save()

#Search Cities
def index(request, city_id = False):
    API_KEY = config("API_KEY")
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=' + API_KEY
   
   #If city_id passed in, update that city as home
    if city_id:
        make_home(city_id)

    if request.method == 'POST':
        form = CityForm(request.POST)
        
        if form.is_valid():
            new_city, sep, state = form.cleaned_data['city_name'].partition(',')
        
            #Openweathermaps api doesn't take in state abbreviations
            #So if user provides input in that format, update state to full state name
            #TODO figure out why this conditional works in an interpreter but not in here
            if len(state) and len(state) < 3:
                state = getStateName(state)

            r = requests.get(url.format(new_city)).json()
            #TODO handle error if city does not exist

            city_obj = StarredCity(city_name=r['name'], city_id=r['id'])
            city_obj.save()

    #TODO print shows that form resets, but is still sending duplicates to db on occasion
    form = CityForm()
    # print("resetting form", form)

    starred_cities_list = StarredCity.objects.order_by('-is_home')
    cities_weather_data = []

    for city in starred_cities_list:
        #Get city data from api
        r = requests.get(url.format(city.city_name)).json()

        city_weather = {
            'city': city.city_name.capitalize(),
            'city_id': city.city_id,
            'is_home': city.is_home,
            'temperature': round(r['main']['temp'], 1),
            'icon': r['weather'][0]['icon'],
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
        # 'rainfall_3h': r['rain']['3h'],
        # 'snowfall_3h': r['snow']['3h'],
    }

    return render(request, 'weather/citydata.html', { 'city_data': city_data})
