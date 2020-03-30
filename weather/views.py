import requests
from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import HttpResponseRedirect
from .models import StarredCity, CityWeatherData
from .forms import CityForm

# Create your views here.

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
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=bc8fdc1c8cf8248eadf944a93af0b431'

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
            'temperature': round(r['main']['temp'], 1),
            'icon': r['weather'][0]['icon'],
            # 'isHome': city.isHome,
        }

        cities_weather_data.append(city_weather)

    context = {'cities_weather_data': cities_weather_data, 'form': form}
    return render(request, 'weather/index.html', context)

#Show detailed weather data for chosen city
def detail(request, city_id):
    try:
        city = StarredCity.objects.get(pk=city_id)
    except StarredCity.DoesNotExist:
        raise Http404("City does not exist")
    return render(request, 'weather/citydata.html', { 'city': city})
