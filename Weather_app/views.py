from django.shortcuts import render
from django import forms
from dotenv import load_dotenv
import requests
import os

load_dotenv()


API_KEY = os.getenv('WEATHER_API_KEY')
API_BASE_URL = os.getenv('WEATHER_API_BASE_URL')


class Form(forms.Form):
    city_name = forms.CharField(max_length=200)


locations = []


def home_page(request):
    name = request.POST.get('title', False)

    data = []

    if name not in locations and name is not False:
        locations.append(name)

    for location in locations:

        url = API_BASE_URL + f'/current.json?key={API_KEY}&q={location}'

        response = requests.get(url)

        if response.status_code == 200:
            city_data = {
                'city': response.json()['location']['name'],
                'country': response.json()['location']['country'],
                'temperature_celsius': response.json()['current']['temp_c'],
                'temperature_fahrenheit': response.json()['current']['temp_f'],
                'condition': response.json()['current']['condition']['text'],
                'weather_image': response.json()['current']['condition']['icon'],
            }

            data.append(city_data)

    context = {
        'data_list': data
    }

    return render(request, 'main-page.html', context)
