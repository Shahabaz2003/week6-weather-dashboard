from typing import Dict, Any

class WeatherDisplay:
    """Renders formatted weather information to the command line"""
    
    ICONS = {
        "Clear": "☀️",
        "Clouds": "☁️",
        "Rain": "🌧️",
        "Drizzle": "🌦️",
        "Thunderstorm": "⛈️",
        "Snow": "❄️",
        "Mist": "🌫️"
    }

    @classmethod
    def display_current(cls, parsed_data: Dict[str, Any], from_cache: bool = False):
        icon = cls.ICONS.get(parsed_data["main_condition"], "🌍")
        unit = parsed_data["unit"]
        
        print("\n🌤️  WEATHER DASHBOARD")
        print("=======================")
        print(f"📍 Current Location: {parsed_data['city']}, {parsed_data['country']}")
        print(f"🕐 Last Updated:    {parsed_data['updated_at']}")
        print(f"📡 API Status:       {'Using cached data' if from_cache else 'Live response fetched'}")
        print("\nCurrent Weather:")
        print("────────────────")
        print(f"Temperature:   {parsed_data['temp']:.1f}{unit} (Feels like: {parsed_data['feels_like']:.1f}{unit})")
        print(f"Conditions:    {parsed_data['condition']} {icon}")
        print(f"Humidity:      {parsed_data['humidity']}%")
        print(f"Wind:          {parsed_data['wind_speed']} m/s")
        print(f"Pressure:      {parsed_data['pressure']} hPa")
        print(f"Visibility:    {parsed_data['visibility']:.1f} km")
        print(f"Sunrise:       {parsed_data['sunrise']}")
        print(f"Sunset:        {parsed_data['sunset']}")
        print("────────────────")

    @classmethod
    def display_forecast(cls, forecast_data: list, unit: str):
        print("\n5-Day Forecast:")
        print("───────────────")
        for day in forecast_data:
            icon = cls.ICONS.get(day["condition"], "🌍")
            print(f"{day['day']}:  {icon}   {day['max_temp']:.1f}{unit} / {day['min_temp']:.1f}{unit}  ({day['condition']})")
        print("=======================")