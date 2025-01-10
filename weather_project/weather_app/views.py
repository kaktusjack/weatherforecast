from django.shortcuts import render
from dotenv import load_dotenv
import os
import requests
import datetime
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
@csrf_exempt
def index(request):

  
    API_KEy=os.environ.get('APIKEY')
    current_weather_url="https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
    forecast_url="https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid={}&cnt=5&exclude=current,minutely,hourly,alerts"

    if request.method=="POST":
        city1= (request.POST['city1']).upper()
        city2= (request.POST.get('city2',None)).upper()

        weather_data1,daily_forecast1=fetch_weather_and_forecast(city1,API_KEy,current_weather_url,forecast_url)

        if city2:
            weather_data2,daily_forecast2=fetch_weather_and_forecast(city2,API_KEy,current_weather_url,forecast_url)
        else:
            weather_data2,daily_forecast2=None,None
            

        context={
            "weather_data1":weather_data1,
            "daily_forecast1":daily_forecast1,
            "weather_data2":weather_data2,
            "daily_forecast2":daily_forecast2,
            
        }
        return render (request,"index.html",context)
        
    else:
        return render(request,"index.html")

@csrf_exempt
def fetch_weather_and_forecast(city,api_key,current_weather_url,forecast_url):
    response=requests.get(current_weather_url.format(city,api_key)).json()
    # print(response)
    print("hi")
    lat, lon= response ['coord']['lat'], response ['coord']['lon']
    forecast_response= requests.get(forecast_url.format(lat,lon,api_key)).json()
    # print(forecast_response)

    weather_data={
        "city":city,
        "temperature":round(response['main']['temp']-273.15,2),
        "description":response['weather'][0]['description'],
        "icon":response['weather'][0]['icon'],
    }
    daily_forecast= []
  
    for daily_data in forecast_response['list'][:5]:
        
        day_and_time = datetime.datetime.strptime(daily_data['dt_txt'], "%Y-%m-%d %H:%M:%S").strftime("%A %H:%M:%S")

        daily_forecast.append({
           
            "date":day_and_time,
            "min_temp":round(daily_data['main']['temp_min']-273.15,2),
            "max_temp":round(daily_data['main']['temp_max']-273.15,2),
            "description":daily_data['weather'][0]['description'],
            "icon":daily_data['weather'][0]['icon'],
  
            
        })
    print(daily_forecast)


    
    return weather_data, daily_forecast
