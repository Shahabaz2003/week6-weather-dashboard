import sys
from weather_app.config import API_KEY
from weather_app.weather_api import WeatherAPI
from weather_app.weather_parser import WeatherParser
from weather_app.weather_display import WeatherDisplay

def main():
    api_client = WeatherAPI(api_key=API_KEY)
    use_fahrenheit = False

    print("====================================")
    print("  Welcome to the Weather Dashboard  ")
    print("====================================")
    
    while True:
        print("\nCommands: [city_name] | toggle | quit")
        user_input = input("Search city or command: ").strip()
        
        if not user_input:
            continue
            
        if user_input.lower() == 'quit':
            print("Exiting application. Goodbye!")
            sys.exit(0)
            
        if user_input.lower() == 'toggle':
            use_fahrenheit = not use_fahrenheit
            unit_str = "Fahrenheit" if use_fahrenheit else "Celsius"
            print(f"Units switched to {unit_str}.")
            continue
            
        print(f"Fetching weather data for '{user_input}'...")
        
        # Cache checking for console display status
        cache_key = f"current_{user_input.lower().replace(' ', '_')}"
        is_cached = api_client.cache_dir.joinpath(f"{cache_key}.json").exists()
        
        # 1. Fetch data from API/Cache
        raw_current = api_client.get_current_weather(user_input)
        raw_forecast = api_client.get_forecast(user_input)
        
        if raw_current and raw_forecast:
            # 2. Parse data
            clean_current = WeatherParser.parse_current(raw_current, use_fahrenheit=use_fahrenheit)
            clean_forecast = WeatherParser.parse_forecast(raw_forecast, use_fahrenheit=use_fahrenheit)
            
            # 3. Display data
            WeatherDisplay.display_current(clean_current, from_cache=is_cached)
            WeatherDisplay.display_forecast(clean_forecast, unit=clean_current["unit"])
        else:
            print("Could not retrieve weather data. Try again or check the city name.")

if __name__ == "__main__":
    main()