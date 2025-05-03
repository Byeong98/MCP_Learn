import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

city:str = "Seoul"
apiKey = os.getenv("OPENWEATHERMAP_APIKEY")
lang:str = "kr"
units:str = 'metric' #화씨 온도를 섭씨 온도로 변경
api:str = f"http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={apiKey}&lang={lang}&units={units}"


result = requests.get(api)
result = json.loads(result.text)

print(result)

"""
출력 코드 

{   
    'coord': {'lon': 126.9778, 'lat': 37.5683}, 
    'weather': [{'id': 701, 'main': 'Mist', 'description': '박무', 'icon': '50n'}], 
    'base': 'stations', 
    'main': {
        'temp': 11.76, 
        'feels_like': 11.26, 
        'temp_min': 11.76, 
        'temp_max': 11.78, 
        'pressure': 1008, 
        'humidity': 87, 
        'sea_level': 1008,
        'grnd_level': 998}, 
    'visibility': 7000, 
    'wind': {'speed': 4.12, 'deg': 270},
    'clouds': {'all': 75},
    'dt': 1746111857,
    'sys': {'type': 1, 'id': 8105, 'country': 'KR', 'sunrise': 1746131753, 'sunset': 1746181329},
    'timezone': 32400, 
    'id': 1835848,
    'name': 'Seoul', 
    'cod': 200
}
"""
# 도시 이름과 온도 출력 
print(f"{result['name']}의 온도는 : {result['main']['temp']}") 

# httpx data type 확인
import httpx 
api:str = f"http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={apiKey}&lang={lang}&units={units}"
response = httpx.Client().get(api)
data = response.json()
print(response.json())
print(type(data)) # dict