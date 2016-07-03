from flask import Flask
from flask import render_template
from flask import request
from flask import make_response
import datetime
import os
import json
import time
import urllib2

app = Flask(__name__)
api_key = 'dfb9bb4473a71b63a4f782bd0b744627'


def get_weather(city):
    url = "http://api.openweathermap.org/data/2.5/forecast/daily?q={}&cnt=10&mode=json&units=metric&APPID={}".format(city, api_key)
    response = urllib2.urlopen(url).read()
    return response


@app.route('/')
def index():
    searchcity = request.args.get('searchcity')
    if not searchcity:
        searchcity = request.cookies.get('last_city')
    if not searchcity:
        searchcity = 'Belgrade'

    data = json.loads(get_weather(searchcity))

    try:
        city = data['city']['name']
    except KeyError:
        return render_template('invalid_city.html', user_input=searchcity)

    country = data['city']['country']
    forecast_list = []
    for d in data.get('list'):
        day = time.strftime('%d %B', time.localtime(d.get('dt')))
        mini = d.get('temp').get('min')
        maxi = d.get('temp').get('max')
        description = d.get('weather')[0].get('description')
        forecast_list.append((day, mini, maxi, description))
    response = make_response(render_template('index.html', forecast_list=forecast_list, city=city, country=country))
    if request.args.get('remember'):
        response.set_cookie('last_city', "{},{}".format(city, country), expires=datetime.datetime.today() + datetime.timedelta(days=3))
    return response

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
