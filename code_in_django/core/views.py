from django.http import HttpResponse
from django.shortcuts import render
import requests
from bs4 import BeautifulSoup

# Create your views here.
def get_html_content(city):
    USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    LANGUAGE = 'en_US,en;q=0.5'
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    city = city.replace(' ', '+')
    html_content = session.get(f'https://www.google.com/search?q=weather+in+{city}').text
    return html_content

def home(request):
    weather_data = None
    if 'city' in request.GET:
        city = request.GET.get('city')
        html_content = get_html_content(city)
        soup = BeautifulSoup(html_content, 'html.parser')
        data_region = soup.find(class_='VQF4g')

        weather_data = dict()
        weather_data['region'] = data_region.find('div', attrs={'id': 'wob_loc'}).text
        weather_data['daytime'] = data_region.find('div', attrs={'id': 'wob_dts'}).text
        weather_data['status'] = data_region.find('div', attrs={'id': 'wob_dcp'}).text
        data_temp = soup.find(class_='vk_bk TylWce')
        weather_data['temp'] = data_temp.find(attrs={'id': 'wob_tm'}).text
        pass
    return render(request, 'core/home.html', {'weather': weather_data})

