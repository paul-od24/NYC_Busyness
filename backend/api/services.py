import requests
import json
import time
from datetime import date, timedelta, datetime
import datetime 
from django.http import JsonResponse
from django.utils import timezone
import pickle
import pandas as pd

import re
from shapely.geometry import MultiPolygon, Point, Polygon

# OpenWeather API

WEATHER_API = "http://api.openweathermap.org/data/2.5/weather?appid=d5de0b0a9c3cc6473da7d0005b3798ac&q=Manhattan"

def get_weather():
    try:
        response = requests.get(WEATHER_API)
        response.raise_for_status()
        weather = response.json()
        
        main_weather = weather["weather"][0]["main"]
        description = weather["weather"][0]["description"]
        temperature = weather["main"]["temp"]
        visibility = weather["visibility"]
        wind_speed = weather["wind"]["speed"]
        wind_deg = weather["wind"]["deg"]
        clouds = weather["clouds"]["all"]
        timestamp = timezone.now().timestamp()

        weather_data = {
            "main_weather": main_weather,
            "description": description,
            "temperature": temperature,
            "visibility": visibility,
            "wind_speed": wind_speed,
            "wind_deg": wind_deg,
            "clouds": clouds,
            "timestamp": timestamp
        }
        
        return weather_data
    except requests.exceptions.RequestException as e:
        print("Error in get_weather:", e)
        return None

# Foursquare API

def get_foursquare_hotels():
    url = "https://api.foursquare.com/v3/places/search"

    headers = {
        "Accept": "application/json",
        "Authorization": "fsq3YJj6mpB8MvstI7T9B/Z74vyD/AuUXD48pI8OJbs7U70="
    }

    params = {
        "query": "hotels",
        "ll": "40.7831,-73.9712",  # Manhattan coordinates
        "open_now": "true",
        "categoryId": "4bf58dd8d48988d1fa931735",  # Category ID for Food (Restaurants)
        "limit": 50,  # Number of results to retrieve per request
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        results = data.get("results", [])

        extracted_data = []

        for result in results:
            fsq_id = result.get("fsq_id")
            name = result.get("name")
            categories = [category.get("name") for category in result.get("categories", [])]
            location = result.get("location", {})
            geocodes = result.get("geocodes", {}).get("main", {})

            url = f"https://api.foursquare.com/v3/places/{fsq_id}"

            r_headers = {
                "accept": "application/json",
                "Authorization": "fsq3YJj6mpB8MvstI7T9B/Z74vyD/AuUXD48pI8OJbs7U70="
            }

            params = {
                "fields": "rating",
                "fields": "hours",
                "fields": "photos",
            }

            r_response = requests.get(url, params=params, headers=r_headers)
            r_response.raise_for_status()
            r_data = r_response.json()
            rating = r_data.get("rating")
            hours = r_data.get("hours")
            phtots = r_data.get("photos")

            extracted_data.append({
                "fsq_id": fsq_id,
                "name": name,
                "categories": categories,
                "location": location,
                "geocodes": geocodes,
                "rating": rating,
                "hours": hours,
                "photos": phtots,
            })
        return extracted_data

    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None


def get_foursquare_restaurants():
    url = "https://api.foursquare.com/v3/places/search"
    headers = {
        "Accept": "application/json",
        "Authorization": "fsq3YJj6mpB8MvstI7T9B/Z74vyD/AuUXD48pI8OJbs7U70="
    }
    params = {
        "query": "restaurants",
        "ll": "40.7831,-73.9712",  # Manhattan coordinates
        "open_now": "true",
        "categoryId": "4d4b7105d754a06374d81259",  # Category ID for Food (Restaurants)
        "limit": 50,  # Number of results to retrieve per request
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        results = data.get("results", [])

        extracted_data = []

        for result in results:
            fsq_id = result.get("fsq_id")
            name = result.get("name")
            categories = [category.get("name") for category in result.get("categories", [])]
            location = result.get("location", {})
            geocodes = result.get("geocodes", {}).get("main", {})

            # Additional API call to get rating, hours, and photos for each restaurant
            r_url = f"https://api.foursquare.com/v3/places/{fsq_id}"
            r_headers = {
                "accept": "application/json",
                "Authorization": "fsq3YJj6mpB8MvstI7T9B/Z74vyD/AuUXD48pI8OJbs7U70="
            }
            r_params = {
                "fields": "rating,hours,photos",
            }
            r_response = requests.get(r_url, params=r_params, headers=r_headers)
            r_response.raise_for_status()
            r_data = r_response.json()
            rating = r_data.get("rating")
            hours = r_data.get("hours")
            photos = r_data.get("photos")

            extracted_data.append({
                "fsq_id": fsq_id,
                "name": name,
                "categories": categories,
                "location": location,
                "geocodes": geocodes,
                "rating": rating,
                "hours": hours,
                "photos": photos,
            })

        return extracted_data

    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None


# Google Places API

def get_google_restaurants():
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    details_url = "https://maps.googleapis.com/maps/api/place/details/json"
    # api_key = "AIzaSyDgYC8VXvS4UG9ApSUhS2v-ByddtHljFls"
    params = {
        "query": "restaurants in Manhattan, New York",
        "key": api_key,
        "fields": "place_id,name,formatted_address,geometry/location,rating,photos"
    }
    restaurant_data = []

    try:
        while True:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            results = data["results"]

            for result in results:
                place_id = result["place_id"]  # Add place ID
                name = result["name"]
                address = result["formatted_address"]
                location = result["geometry"]["location"]
                lat = location["lat"]
                lng = location["lng"]
                rating = result.get("rating")
                photos = result.get("photos", [])

                # Make a separate API call to get details
                details_params = {
                    "place_id": place_id,
                    "fields": "opening_hours",
                    "key": api_key
                }
                details_response = requests.get(details_url, params=details_params)
                details_response.raise_for_status()
                details_data = details_response.json()
                
                # Get the opening hours if available, or an empty list if not present
                opening_hours = details_data["result"]
                
                photo_urls = []
                for photo in photos:
                    photo_reference = photo.get("photo_reference")
                    photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={api_key}"
                    photo_urls.append(photo_url)

                restaurant_data.append({
                    "place_id": place_id,
                    "name": name,
                    "address": address,
                    "latitude": lat,
                    "longitude": lng,
                    "rating": rating,
                    "photos": photo_urls,
                    "opening_hours": opening_hours
                })

            if "next_page_token" not in data:
                break

            params["pagetoken"] = data["next_page_token"]
            time.sleep(2)  # Delay between API calls as per Google's guidelines

    except requests.exceptions.RequestException as e:
        print("Error in get_google_restaurants:", e)

    return restaurant_data

def get_google_attractions():
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    details_url = "https://maps.googleapis.com/maps/api/place/details/json"
    # api_key = "AIzaSyDgYC8VXvS4UG9ApSUhS2v-ByddtHljFls"
    params = {
        "query": "tourist attractions in Manhattan, New York",
        "key": api_key,
        "fields": "place_id,name,formatted_address,geometry/location,rating,photos,opening_hours"
    }
    attraction_data = []

    try:
        while True:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            results = data["results"]

            for result in results:
                place_id = result["place_id"]  # Add place ID
                name = result["name"]
                address = result["formatted_address"]
                location = result["geometry"]["location"]
                lat = location["lat"]
                lng = location["lng"]
                rating = result.get("rating")
                photos = result.get("photos")

                # Make a separate API call to get details
                details_params = {
                    "place_id": place_id,
                    "fields": "opening_hours",
                    "key": api_key
                }
                details_response = requests.get(details_url, params=details_params)
                details_response.raise_for_status()
                details_data = details_response.json()

                # Get the opening hours if available, or an empty list if not present
                opening_hours = details_data["result"]

                photo_urls = []
                if photos:
                    for photo in photos:
                        photo_reference = photo.get("photo_reference")
                        photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={api_key}"
                        photo_urls.append(photo_url)

                attraction_data.append({
                    "place_id": place_id,
                    "name": name,
                    "address": address,
                    "latitude": lat,
                    "longitude": lng,
                    "rating": rating,
                    "photos": photo_urls,
                    "opening_hours": opening_hours
                })

            if "next_page_token" not in data:
                break

            params["pagetoken"] = data["next_page_token"]
            time.sleep(2)  # Delay between API calls as per Google's guidelines

    except requests.exceptions.RequestException as e:
        print("Error in get_google_attractions:", e)
    
    return attraction_data




def get_google_hotels():
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    # api_key = "AIzaSyDgYC8VXvS4UG9ApSUhS2v-ByddtHljFls"
    params = {
        "query": "Hotels in Manhattan, New York",
        "key": api_key,
        "fields": "place_id,name,formatted_address,geometry/location,rating,photos"
    }
    hotel_data = []

    try:
        while True:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            results = data["results"]

            for result in results:
                place_id = result["place_id"]  # Add place ID
                name = result["name"]
                address = result["formatted_address"]
                location = result["geometry"]["location"]
                lat = location["lat"]
                lng = location["lng"]
                rating = result.get("rating")
                photos = result.get("photos")

                photo_urls = []
                if photos:
                    for photo in photos:
                        photo_reference = photo.get("photo_reference")
                        photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={api_key}"
                        photo_urls.append(photo_url)

                hotel_data.append({
                    "place_id": place_id,
                    "name": name,
                    "address": address,
                    "latitude": lat,
                    "longitude": lng,
                    "rating": rating,
                    "photos": photo_urls
                })

            if "next_page_token" not in data:
                break

            params["pagetoken"] = data["next_page_token"]
            time.sleep(2)  # Delay between API calls as per Google's guidelines

    except requests.exceptions.RequestException as e:
        print("Error in get_google_hotels:", e)
        
    return hotel_data


# Ticketmaster API

def get_events():
    API_KEY = "q62LGBfQCP3kg9gVyUlveTeq2BayJuLL"
    url = "https://app.ticketmaster.com/discovery/v2/events.json"
    today = datetime.date.today()  # Remove the "datetime" before ".date()"
    end_date = today + datetime.timedelta(days=30)
    event_data = []

    params = {
        "apikey": API_KEY,
        "latlong": "40.7831,-73.9712",  # Manhattan coordinates (latitude, longitude)
        "radius": "5",  # Radius in miles around the specified coordinates
        "size": 200,  # Number of events per API response (maximum allowed)
        "page": 0,  # Start with the first page
    }

    while True:
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            events = data["_embedded"]["events"]

            for event in events:
                event_date = event["dates"]["start"]["localDate"]
                event_date_obj = datetime.datetime.fromisoformat(event_date).date()

                if today <= event_date_obj <= end_date:
                    event_name = event["name"]
                    event_time = event["dates"]["start"].get("localTime", "Time not available")
                    event_image = event["images"][0]["url"] if event["images"] else None
                    event_url = event["url"]
                    event_latitude = event["_embedded"]["venues"][0]["location"]["latitude"]
                    event_longitude = event["_embedded"]["venues"][0]["location"]["longitude"]

                    if event.get("classifications"):
                        classification = event["classifications"][0]
                        genre = classification.get("genre", {})
                        event_genres = genre.get("name")
                    else:
                        event_genres = None

                    event_data.append({
                        "name": event_name,
                        "date": event_date,
                        "time": event_time,
                        "image": event_image,
                        "url": event_url,
                        "genres": event_genres,
                        "latitude": event_latitude,
                        "longitude": event_longitude
                    })

            params["page"] += 1

            if len(event_data) >= 1000:
                break

        except requests.exceptions.RequestException as e:
            print("Error in get_events:", e)
            break

    return event_data


# ML Model 

def is_point_inside_polygon(point, polygon_coords):
        """Checks if point is inside a polygon"""
        polygon = Polygon(polygon_coords)
        point = Point(point)
        return polygon.contains(point)

def get_predictions(hour: float, day: float, month: float, latitude: float, longitude: float) -> float:
    """Returns prediction of busyness in Area."""

    def get_location_id(latitude, longitude):
        """Returns location ID given coordinates"""
        with open('taxi_zones.json', 'r') as file:
            data = json.load(file)
        for i in range(1, len(data) + 1):
             try:
                if is_point_inside_polygon((latitude, longitude), data[str(i)]):
                    zone = i
             except:
                  continue
        return zone
    
    if day < 5:
        is_weekday, is_weekend = 1, 0
    else:
        is_weekday, is_weekend = 0, 1
    
    try:
        WEATHERAPI = f"http://api.openweathermap.org/data/2.5/forecast?lat=40.6958lon=74.184&appid=d5de0b0a9c3cc6473da7d0005b3798ac"
        # Need to get Temperature, Wind Speed, Wind direction, Clouds 
        text = requests.get(WEATHERAPI).text
        forecast = json.loads(text)['list']
        for i in forecast:
            temp = i['main']['temp']
            humidity = i['main']['humidity']
            wind_speed = i['wind']['speed']
            pressure = i['main']['pressure']
            # Don't think this is in forecast
            # Will double check then remove if necessary 
            precipitation = 0 
    
    # Bill will need you to help with correct error handling
    except Exception as e:
        temp, humidity, wind_speed, pressure, precipitation = 60, 49, 8, 2988, 0
    
    zone = get_location_id(latitude, longitude)    
    with open('xgb_model.pkl', 'rb') as file:
        model = pickle.load(file)

    prediction_data = pd.DataFrame({
        'Hour': [hour],
        'is_weekday': [is_weekday],
        'is_weekend': [is_weekend],
        'PULocationID': [0],
        'Temperature': [temp],
        'Precip.': [precipitation],
        'Pressure': [pressure],
        'Wind Speed': [wind_speed],
        'Humidity': [humidity],
        'Month': [month]
    })

    prediction_data = model.predict(prediction_data)
    return prediction_data[0]

def get_heat_map(hour: float, day: float, month:float = 8):
    """ Function that returns coordinates with weight for heat map"""
    with open(f'api/pickles/xgb_model.pkl', 'rb') as file:
        model = pickle.load(file)

    if day < 5:
        is_weekday, is_weekend = 1, 0
    else:
        is_weekday, is_weekend = 0, 1

    try:
        WEATHERAPI = f"http://api.openweathermap.org/data/2.5/forecast?lat=40.6958&lon=74.184&appid=d5de0b0a9c3cc6473da7d0005b3798ac"
        # Need to get Temperature, Wind Speed, Wind direction, Clouds 
        text = requests.get(WEATHERAPI).text
        forecast = json.loads(text)['list']
        for i in forecast:
            temp = i['main']['temp']
            humidity = i['main']['humidity']
            wind_speed = i['wind']['speed']
            pressure = i['main']['pressure']
            precipitation = 0 
    except Exception as e:
        weather = [283.5, 43, 2.28, 1012, 0]
        return weather
    
    prediction_data = pd.DataFrame({
        'Hour': [hour],
        'is_weekday': [is_weekday],
        'is_weekend': [is_weekend],
        'PULocationID': [0],
        'Temperature': [temp],
        'Precip.': [precipitation],
        'Pressure': [pressure],
        'Wind Speed': [wind_speed],
        'Humidity': [humidity],
        'Month': [month]
    })

    value_list = [4,12,13,24,41,42,43,45,48,50,68,74,75,79,87,88,90,100,107,113,114,116,120,125,127,128,137,140,141,142,143,
                144,148,151,152,158,161,162,163,164,166,170,186,202,209,211,224,229,230,231,232,233,234,236,237,238,239,243,
                244,246,249,261,262,263]
    
    heat_map_data = {}

    for i in value_list:
        prediction_data['PULocationID'] = i
        heat_map_data[i] = model.predict(prediction_data)[0]
    
    return heat_map_data
