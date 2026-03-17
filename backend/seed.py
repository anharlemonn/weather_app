import psycopg2 
from dotenv import load_dotenv
import os
import requests


load_dotenv()

API_KEY = os.getenv("API_KEY")

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
    )
    
conn = get_db_connection()
cursor = conn.cursor()

cursor.execute("""
               CREATE TABLE IF NOT EXISTS weather (
                   id SERIAL PRIMARY KEY, 
                   name VARCHAR(100), 
                   temp_f FLOAT, 
                   temp_c FLOAT,
                   max_temp FLOAT,
                   min_temp FLOAT,
                   condition VARCHAR(100),
                   hours_c FLOAT[],
                   hours_f FLOAT[]
               )
               """)

cities = [
    "Berkeley",
    "Oakland",
    "San Francisco",
    "San Jose",
    "Fremont",
    "Santa Clara",
    "Sunnyvale",
    "Palo Alto",
    "Mountain View",
    "Redwood City",
    "Millbrae",
    "Daly City",
    "South San Francisco",
    "San Mateo",
    "Hayward",
    "Walnut Creek",
    "Concord",
    "Richmond",
    "San Rafael",
    "Sausalito"
]
cordinates = []

# fetch the lat, lon cordinates of cities that I want 
for city in cities:
    url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={city}&days=1&aqi=no&alerts=no"
    results = requests.get(url)
    data = results.json()
    
    lat = data["location"]["lat"] 
    lon = data["location"]["lon"]
    
    cordinates.append([lat,lon])
    
# grab data for each
for lat, lon in cordinates:
    url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={lat} ,{lon}&days=1&aqi=no&alerts=no"
    results = requests.get(url) 
    data = results.json()
    # print(dataJson)
    # data = dataJson["data"]
    
    # extract from the data 
    name = data["location"]["name"]
    
    current = data["current"]
    temp_c = current["temp_c"]
    temp_f = current["temp_f"]
    condition = current["condition"]["text"]
    
    day = data["forecast"]["forecastday"][0]["day"]
    hours = data["forecast"]["forecastday"][0]["hour"]
    
    hours_f = []
    hours_c = []
    for i in range(len(hours)):
        hours_f.append(hours[i]['temp_f'])
        hours_c.append(hours[i]['temp_c'])
    
    
    # insert row into db 
    cursor.execute("""
        INSERT INTO weather (name, temp_c, temp_f, condition, hours_f, hours_c)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (name, temp_c, temp_f, condition, hours_c, hours_f))
    

conn.commit()
cursor.close()
conn.close()

# a simple database for now 
# weather 
# name: string
# current temp: int
# max temp: int
# min tem: int 
# chance_rain
# condition


# add this later on 
#24HourTemperatures_f: List[60,60,50,70,]
# 24HourTemperatures_c: List[30,40,10,2,12, ..]

    
