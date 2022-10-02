# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import datetime
import json

import requests
import spacy
import string
from geopy.geocoders import Nominatim
import geocoder

nlp = spacy.load("en_core_web_md")
api_key = "f829e0c6a641f3f32551028815f5e57a"


def get_weather(city_name):
    api_url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid={}".format(city_name, api_key)

    response = requests.get(api_url)
    response_dict = response.json()

    weather = response_dict["weather"][0]["description"]

    if response.status_code == 200:
        return weather
    else:
        print('[!] HTTP {0} calling [{1}]'.format(response.status_code, api_url))
        return None

def get_weather_geolocation(latitude,longitude):
    api_url = "http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}".format(latitude, longitude, api_key)

    response = requests.get(api_url)
    response_dict = response.json()

    weather = response_dict["weather"][0]["description"]

    if response.status_code == 200:
        return weather
    else:
        print('[!] HTTP {0} calling [{1}]'.format(response.status_code, api_url))
        return None
def get_forecast(city_name):
    geolocator = Nominatim(user_agent="Niamh Murphy")
    location = geolocator.geocode(city_name)
    print(location.address)
    print((location.latitude, location.longitude))
    api_url = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude={}&appid={}".format(location.latitude, location.longitude,"", api_key)

    response = requests.get(api_url)
    response_dict = response.json()

    forecast = response_dict["daily"][0]

    if response.status_code == 200:
        output = "\n"
        output = output + "At " + datetime.datetime.fromtimestamp(forecast["dt"]).strftime("%m/%d/%Y, %H:%M:%S") + "\n"
        output = output + "Outlook: " + str((forecast['weather'][0])['description']) + "\n"
        output = output + "Sunrise: " + datetime.datetime.fromtimestamp(forecast["sunrise"]).strftime("%H:%M:%S") + "\n"
        output = output + "Sunset: " + datetime.datetime.fromtimestamp(forecast["sunset"]).strftime("%H:%M:%S") + "\n"
        output = output + "Moonrise: " + datetime.datetime.fromtimestamp(forecast["moonrise"]).strftime("%H:%M:%S") + "\n"
        output = output + "Moonset: " + datetime.datetime.fromtimestamp(forecast["moonset"]).strftime("%H:%M:%S") + "\n"
        output = output + "Temperatures:" + "\n"
        output = output + "\tHigh is " + str(round(((((forecast['temp'])['max'] - 273) * 1.8) + 32), 0)) + " F" + "\n"
        output = output + "\tLow is " + str(round(((((forecast['temp'])['min'] - 273) * 1.8) + 32), 0)) + " F" + "\n"
        output = output + "Humidity: " + str(forecast["humidity"]) + "%" + "\n"
        output = output + "Chance of Precipitation: " + str(round(forecast['pop'] * 100, 0)) + "%" + "\n"
        return output
    else:
        print('[!] HTTP {0} calling [{1}]'.format(response.status_code, api_url))
        return None

def get_forecast_geolocation(latitude, longitude):
    api_url = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude={}&appid={}".format(latitude, longitude,"", api_key)

    response = requests.get(api_url)
    response_dict = response.json()

    forecast = response_dict["daily"][0]

    if response.status_code == 200:
        output = "\n"
        output = output + "At " + datetime.datetime.fromtimestamp(forecast["dt"]).strftime("%m/%d/%Y, %H:%M:%S") +"\n"
        output = output + "Outlook: " + str((forecast['weather'][0])['description']) +"\n"
        output = output + "Sunrise: " + datetime.datetime.fromtimestamp(forecast["sunrise"]).strftime("%H:%M:%S") +"\n"
        output = output + "Sunset: " + datetime.datetime.fromtimestamp(forecast["sunset"]).strftime("%H:%M:%S") + "\n"
        output = output + "Moonrise: " + datetime.datetime.fromtimestamp(forecast["moonrise"]).strftime("%H:%M:%S") + "\n"
        output = output + "Moonset: " + datetime.datetime.fromtimestamp(forecast["moonset"]).strftime("%H:%M:%S") + "\n"
        output = output + "Temperatures:" + "\n"
        output = output + "\tHigh is " + str(round(((((forecast['temp'])['max']-273)*1.8)+32),0)) + " F" + "\n"
        output = output + "\tLow is " + str(round(((((forecast['temp'])['min'] - 273) * 1.8) + 32),0)) + " F" + "\n"
        output = output + "Humidity: " + str(forecast["humidity"]) + "%" + "\n"
        output = output + "Chance of Precipitation: " + str(round(forecast['pop']*100,0)) + "%" + "\n"
        return output

    else:
        print('[!] HTTP {0} calling [{1}]'.format(response.status_code, api_url))
        return None

def chatbot(statement):
    weather = nlp("What is the weather in a city")
    forecast = nlp("What is the forecast for a city")
    rain = nlp("Is it raining in the city")
    snow = nlp("Is it snowing in the city")
    sunshine = nlp("Is it sunny in the city")
    wind = nlp("Is it windy in the city")
    cloud = nlp("Is it cloudy in the city")
    statement = nlp(statement)
    min_similarity = 0.75
    weather_similarity = weather.similarity(statement)
    forecast_similarity = forecast.similarity(statement)
    rain_similarity = rain.similarity(statement)
    snow_similarity = snow.similarity(statement)
    sunshine_similarity = sunshine.similarity(statement)
    wind_similarity = wind.similarity(statement)
    cloud_similarity = cloud.similarity(statement)
    similarity_list = [weather_similarity, forecast_similarity, rain_similarity, snow_similarity, sunshine_similarity, wind_similarity, cloud_similarity]
    maximum_similarity = max(similarity_list)
    maximum_similarity_index = similarity_list.index(maximum_similarity)
    if (maximum_similarity >= min_similarity):
        if (len(statement.ents)> 0):
            expanded_location = city = ""
            for ent in statement.ents:
                if ent.label_ == "GPE":  # GeoPolitical Entity
                    if (len(expanded_location) == 0):
                        expanded_location = city = ent.text
                    else:
                        expanded_location = expanded_location + ", " + ent.text


            if (len(city) == 0):
              return "I did not recognize the city. Try adding state or country code"
            else:
                location = geocoder.arcgis(expanded_location)
                latlng = location.latlng
        else:
            location = geocoder.ip('me')
            city = location.city
            latlng = location.latlng
        # add code to get current location
        if(maximum_similarity_index == 1):
            #looking for the weather or forecast since they are very similar
            for tokenS in statement:
                if (tokenS.text == "forecast"):
                    city_forecast = get_forecast_geolocation(latlng[0],latlng[1])
                    if city_forecast is not None:
                        return "For " + city + ", the current forecast is: " + city_forecast
                    else:
                        return "Something went wrong."
            city_weather = get_weather_geolocation(latlng[0], latlng[1])
            if city_weather is not None:
                return "In " + city + ", the current weather is: " + city_weather
            else:
                return "Something went wrong."
        else:
            city_weather = get_weather_geolocation(latlng[0],latlng[1])
            if city_weather is not None:
                if (maximum_similarity_index == 0):
                    return "In " + city + ", the current weather is: " + city_weather
                elif (maximum_similarity_index == 2):
                    #check if raining or Snowing they are very similar
                    output = "No it is " + city_weather + " in " + city
                    raining = nlp("rain")
                    snowing = nlp("snow")
                    weather = nlp(city_weather)
                    for tokenR in raining:
                        for tokenW in weather:
                           raining_similarity = tokenR.similarity(tokenW)
                           if (raining_similarity >= 0.65):
                                output = "Yes it is " + city_weather + " in " + city
                    for tokenS in snowing:
                        for tokenW in weather:
                            snowing_similarity = tokenS.similarity(tokenW)
                            if (snowing_similarity >= 0.65):
                                output = "Yes it is " + city_weather + " in " + city
                    return output
                elif (maximum_similarity_index == 3):
                    #check if snowing
                    output = "No it is " + city_weather + " in " + city
                    snowing = nlp("snow")
                    weather = nlp(city_weather)
                    for tokenS in snowing:
                        for tokenW in weather:
                            snowing_similarity = tokenS.similarity(tokenW)
                            if (snowing_similarity  >= 0.65):
                                output = "Yes it is " + city_weather + " in " + city
                    return output

                elif (maximum_similarity_index == 4):
                    #check if sunny
                    output = "No it is " + city_weather + " in " + city
                    sunny = nlp("sun")
                    weather = nlp(city_weather)
                    for tokenSu in sunny:
                        for tokenW in weather:
                            sunny_similarity = tokenSu.similarity(tokenW)
                            if (sunny_similarity >= 0.65):
                                output = "Yes it is " + city_weather + " in " + city
                    return output
                elif (maximum_similarity_index == 5):
                    #check if windy
                    output = "No it is " + city_weather + " in " + city
                    windy = nlp("wind")
                    weather = nlp(city_weather)
                    for tokenWi in windy:
                        for tokenW in weather:
                            windy_similarity = tokenWi.similarity(tokenW)
                            if (windy_similarity >= 0.65):
                                output = "Yes it is " + city_weather + " in " + city
                    return output
                elif (maximum_similarity_index == 6):
                    #check if cloudy
                    output = "No it is " + city_weather + " in " + city
                    cloudy = nlp("cloud")
                    weather = nlp(city_weather)
                    for tokenC in cloudy:
                        for tokenW in weather:
                            cloudy_similarity = tokenC.similarity(tokenW)
                            if (cloudy_similarity >= 0.65):
                                output = "Yes it is " + city_weather + " in " + city
                    return output
                return "Something went wrong."
    else:
        return "Sorry I don't understand that. Please rephrase your statement."




if __name__ == '__main__':
    print('Hi I am Niamh and I am the weather chatbot.')
    print('Enter quit when finished')
    weatherquestion = ""
    while weatherquestion.lower() != "quit":
        weatherquestion = input(">> ")
        if weatherquestion.lower() != "quit":
            print("<< " + chatbot(weatherquestion))
        else:
            print("Thank you")
