from fastapi import FastAPI
import requests
from fastapi.middleware.cors import CORSMiddleware

# db stuff 
import psycopg2 
import psycopg2.extras
from dotenv import load_dotenv
import os 

load_dotenv()

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        cursor_factory=psycopg2.extras.RealDictCursor  # return dicts
    )
app = FastAPI()

# my frontend is allowed to recieve the data
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = os.getenv("API_KEY")

# fakeDb = {
#     1: {
#         "name": "berkeley",
#         "lat": 37.8717,
#         "lon": -122.2727
#     },
#     2: {
#         "name": "los angeles",
#         "lat": 34.0522,
#         "lon": -118.2437
#     },
#     3: {
#         "name": "millbrae",
#         "lat": 37.5985,
#         "lon": -122.3869
#     },
#     4: {
#         "name": "oakland",
#         "lat": 37.8044,
#         "lon": -122.2712
#     },
#     5: {
#         "name": "san francisco",
#         "lat": 37.7749,
#         "lon": -122.4194
#     }
# }


# helper function
# def getCityData(id):
#     city = fakeDb[id]
#     name, lat, lon = city["name"], city["lat"], city["lon"]
    
#     url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={lat},{lon}&days=3&aqi=no&alerts=no"
    
#     data = requests.get(url).json()
    
#     dayData = data["forecast"]["forecastday"][0]["day"]
    
#     result = {
#         "name": name,
#         "temp_c": data["current"]["temp_c"],
#         "temp_f": data["current"]["temp_f"],
#         "day": dayData,
#         "hours":  data["forecast"]["forecastday"][0]["hour"]
#     }
#     return result

@app.get("/")
def root():
    return {"status": "ok"} 

@app.get("/weather")
def weather():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
                   SELECT * from weather
                   
                   """) 
    
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return {
        "count": len(results),
        "data": results
    }

@app.get("/weather/{id}")
def cityInfo(id: int):
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
                            
                            SELECT * FROM weather WHERE id=%s
                            
                            """, (id,))
    result = cursor.fetchall()
    print('backend', result)

    cursor.close()
    conn.close()
    
    return { "data": result}

# 0.0.0.0 : accept connections from anywhere
# machine,                                                                                              local network, everywhere

# 127.0.0.1 : only accept connections from your own machine

# reload=True : every time save main.py, uvicorn automatically restarts the server so your changes take effect immediately
# so you dont need to restart the server everytime you change a line of code, don't use this in production thought lol
if __name__ == "__main__":
    import uvicorn 
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
