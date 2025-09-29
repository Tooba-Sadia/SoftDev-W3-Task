import requests
import datetime
import pytz # Recommended for robust timezone handling
import json # Required to save data to a JSON file
import pycountry #Required to convert country code to name


api_key = "1c24be15da95f34d89e54227688e881a"

# using direct geocoding
#for city
'''http://api.openweathermap.org/geo/1.0/direct?q={city name}
,{state code},{country code}&limit={limit}&appid={API key}'''

#current weather data
#https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API key}

city_input = input("Enter the City or Comma separated Cities you want the weather for>> ")
cities = [c.strip() for c in city_input.split(',')]

def kelvin_to_celsius(kelvin):
    """Converts Kelvin to Celsius and rounds to 1 decimal place."""
    return round(kelvin - 273.15, 1)

for city in cities:
    try:
        geocode_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&appid={api_key}"

        # --- GEOCoding Request ---
        response = requests.get(geocode_url)

        if response.status_code == 401:
            print("ERROR: API Key Issue. Please check if the API key is correct or expired.")
            # Exit the program since the key is invalid
            exit() 
        
        # Raise an exception for other bad status codes (4xx or 5xx)
        response.raise_for_status()
        
        #using Json to access lat lon as keys
        data = response.json() 

        # Handle INVALID CITY NAME: The geocoding API returns an empty list [] for an unknown city
        if not data:
            print(f"ERROR: City not found. No location data returned for '{city}'.")
            # Exit the program since we can't get coordinates
            exit()

        #(type(data)) = list so accessing 0th element which is a list
        loc_info = data[0]

        lat = loc_info["lat"]
        lon = loc_info["lon"]

        # --- WEATHER Data Request ---
        weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
        response2 = requests.get(weather_url) 

        response2.raise_for_status()

        json_data = response2.json()

        # --- Data Extraction and Formatting ---

        city_name = json_data['name']
        
        # --- Convert Alpha-2 (2-letter) code to Country Name ---
        country_code = json_data['sys']['country'] # <-- Corrected typo from 'jsom_data'
        country_obj = pycountry.countries.get(alpha_2=country_code)

        # Safely get the country name or default to the code if not found
        country_name = country_obj.name if country_obj else country_code

        # Temperature conversion
        current_temp_k = json_data['main']['temp']
        current_temp_c = kelvin_to_celsius(current_temp_k)
        feels_like_c = kelvin_to_celsius(json_data['main']['feels_like'])

        # Weather description
        description = json_data['weather'][0]['description'].title()

        # Wind formatting
        wind_speed = json_data['wind']['speed'] # Assumes m/s (OpenWeatherMap default)

        # Other metrics
        humidity = json_data['main']['humidity']
        pressure = json_data['main']['pressure']
        cloud_cover = json_data['clouds']['all']

        # --- TIME and DATE Extraction ---
        timestamp_utc = json_data['dt']
        timezone_offset = json_data['timezone']

        # 1. Convert the Unix timestamp (dt) to a UTC datetime object
        utc_time = datetime.datetime.fromtimestamp(timestamp_utc, tz=pytz.utc)

        # 2. Apply the timezone offset to get the local time
        local_offset = datetime.timedelta(seconds=timezone_offset)
        local_time = utc_time + local_offset

        date = local_time.strftime('%A, %B %d, %Y')
        time = local_time.strftime('%I:%M %p')


        # --- User-Friendly Presentation ---

        print("="*50)
        print(f"CURRENT WEATHER REPORT for {city_name}, {country_name}")
        print("="*50)
        # Display the Date and Time in a clear, local format
        print(f"🗓️ Data Date: {date}")
        print(f"⏱️ Local Time: {time}")
        print("-" * 50)
        print(f"🌤️ Condition: {description}")
        print(f"🌡️ Temperature: {current_temp_c}°C (Feels like {feels_like_c}°C)")
        print("-" * 50)
        print(f"💨 Wind: {wind_speed}")
        print(f"💧 Humidity: {humidity}%")
        print(f"☁️ Cloud Cover: {cloud_cover}%")
        print(f"⏱️ Pressure: {pressure} hPa")
        print("="*50)

        # --- Saving fetched weather details into a JSON file ---
        json_data_to_save = {
            'City' : city_name,
            'Country_Code': country_code,
            'Country_Name': country_name, # <-- Added full name
            'Date' : date,
            'Time' : time,
            'Weather Condition' : description,
            'Temperature (°C)' : current_temp_c,
            'Feels like (°C)' : feels_like_c,
            'Wind Speed (m/s)': wind_speed, 
            'Humidity (%)': humidity,
            'Cloud Cover (%)': cloud_cover,
            'Pressure (hPa)': pressure
        }

        # Define the filename based on the city name
        # Using .replace to make sure the filename is valid #e.g dera ghazi khan
        filename = f"{city_name.replace(' ', '_')}_weather_report.json"

        with open(filename, 'w') as f:
            json.dump(json_data_to_save, f, indent=4)
        
        print("-" * 50)
        print(f"Successfully saved weather data to {filename}")


    except requests.exceptions.RequestException as e:
        # This block handles network issues or other general request failures
        print(f"ERROR during API request (Network/Connection/Other HTTP Error): {e}")

    except KeyError as e:
        # This block handles issues where a key is missing in the JSON data
        print(f"ERROR: Failed to parse weather data. Missing key: {e}")

    except Exception as e:
        # Catch all other unexpected errors (like pycountry not being installed)
        print(f"An unexpected error occurred: {e}")