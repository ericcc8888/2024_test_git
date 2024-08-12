import requests
import json
import os

from pprint import pprint

#Request URL
#'https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=CWA-643AE88F-AD63-4667-966E-ED19C35D1CD4&format=JSON&locationName=%E8%87%BA%E5%8C%97%E5%B8%82,%E8%87%BA%E4%B8%AD%E5%B8%82'

header = {
    'Accept' : 'application/json'
}

parameters = {
    'Authorization' : os.getenv("CWA_API_KEY" , None),
    'locationName' : ['臺中市']
}

url = 'https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001'
response = requests.get(url, headers = header , params = parameters)

if response.status_code == 200:
    weather_data = response.json()

else:
    print('Requests Error')

#pprint(weather_data['records']['location'])

weather_element_name = {
    'Wx' : '天氣現象',
    'PoP' : '降雨機率',
    'CI' : '舒適度',
    'MinT' : '時段最低溫度',
    'MaxT' : '時段最高溫度' 
}

cities_weather = dict()
for location in weather_data['records']['location']:
    city_name = location['locationName']

    city_weather = dict()
    for element in location['weatherElement']:
        print(element['elementName'], end=':')
        print(element['time'][0]['parameter']['parameterName'])
        
        element_name = element['elementName']
        element_value = element['time'][0]['parameter']['parameterName']

        if element_name in ['MinT' , 'MaxT']:
            element_unit = 'C'
        elif element_name in ['PoP']:
            element_unit = '%'
        else:
            element_unit = ''
        
        element_name = weather_element_name[element['elementName']]

        city_weather[element_name] = element_value

cities_weather[city_name] = city_weather

pprint(cities_weather)