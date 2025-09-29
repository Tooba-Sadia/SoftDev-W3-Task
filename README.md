# Python Weather Reporter: Multi-City Data Fetcher

## Task Overview
This Python script is designed to fetch current weather data for one or more cities provided by the user and display the results in a user-friendly format, while also saving the detailed information into a separate JSON file for each city. It utilizes the OpenWeatherMap API for reliable data retrieval.

## Problem Approach
The core challenge was fetching comprehensive and accurate weather data given only a city name, and handling this process for multiple inputs.

The solution was structured as a robust two-step API process:

1. **Geocoding:** Use the city name entered by the user to call the OpenWeatherMap Geocoding API. This step translates the human-readable city name (e.g., "Paris") into precise geographic coordinates (latitude and longitude).  
2. **Weather Fetching:** Use the retrieved latitude and longitude to call the main OpenWeatherMap Current Weather API. This ensures the weather data is specific to the requested location.  
3. **Data Processing & Output:** The raw data (in Kelvin, Alpha-2 country codes, Unix timestamps) is converted to user-friendly formats (Celsius, full country names, local date/time) and then printed to the console and saved as a structured JSON file.

## Key Challenges and Solutions

| Challenge                | Solution Implemented                                                                                                                                       | Takeaway                                                                 |
|---------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------|
| Handling Multiple Cities  | The script now accepts a comma-separated string of cities, which is split into a list. The entire fetching and processing logic is wrapped in a for loop that iterates over each city. | Use list comprehensions and loops for efficient handling of variable user inputs. |
| API Key/Bad Request Errors | Added explicit checks for `response.status_code == 401` (API Key Invalid) and used `response.raise_for_status()` to catch general network/HTTP errors.     | Robust error handling prevents the script from crashing and provides specific feedback to the user. |
| Invalid City Input        | Added a check (`if not data:`) after the Geocoding request. If the city is not found, the script prints an error and uses `continue` to proceed to the next city in the list. | Graceful error recovery is essential for multi-item processing tasks.     |
| Country Code Conversion   | The raw data provides a 2-letter country code (e.g., "US"). The `pycountry` library was integrated to convert this code into the full, readable country name (e.g., "United States"). | Leverage specialized external libraries (`pycountry`) to handle complex data conversions and standardize output. |
| Timestamp and Timezone    | The API provides UTC timestamp and a separate timezone offset. The `datetime` and `pytz` libraries were used to correctly combine these values to display the local time and date for the reported location. | Timezone arithmetic is complex; using `pytz` for robust handling is critical for accuracy. |

## Key Takeaways
- **Modular Functionality:** Breaking down the task into small, reusable functions (like `kelvin_to_celsius`) makes the main logic cleaner and easier to read.  
- **External Libraries:** Libraries like `pycountry`, `pytz`, and `requests` are indispensable for real-world data processing, providing standardized solutions for common problems like timezone conversion and HTTP communication.  
- **Data Serialization:** Using the `json` library to save the output is an effective way to store structured data that can be easily consumed by other programs or archived.  
- **Input Robustness:** Cleaning user input (`.strip()`) and handling unexpected edge cases (empty results, missing JSON keys) ensures the script remains stable and user-friendly.  
