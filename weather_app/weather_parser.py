from datetime import datetime
from typing import Dict, Any

class WeatherParser:
    """Parses raw JSON data into clean formatting"""
    
    @staticmethod
    def celsius_to_fahrenheit(celsius: float) -> float:
        return (celsius * 9/5) + 32

    @classmethod
    def parse_current(cls, data: Dict[str, Any], use_fahrenheit: bool = False) -> Dict[str, Any]:
        main = data.get("main", {})
        wind = data.get("wind", {})
        sys = data.get("sys", {})
        weather = data.get("weather", [{}])[0]
        
        temp_c = main.get("temp", 0.0)
        feels_c = main.get("feels_like", 0.0)
        
        updated_at = datetime.fromtimestamp(data.get("dt", 0)).strftime("%Y-%m-%d %H:%M:%S")
        sunrise = datetime.fromtimestamp(sys.get("sunrise", 0)).strftime("%H:%M")
        sunset = datetime.fromtimestamp(sys.get("sunset", 0)).strftime("%H:%M")
        
        return {
            "city": data.get("name"),
            "country": sys.get("country"),
            "temp": cls.celsius_to_fahrenheit(temp_c) if use_fahrenheit else temp_c,
            "feels_like": cls.celsius_to_fahrenheit(feels_c) if use_fahrenheit else feels_c,
            "condition": weather.get("description", "Unknown").capitalize(),
            "main_condition": weather.get("main", "Clear"),
            "humidity": main.get("humidity", 0),
            "wind_speed": wind.get("speed", 0.0),
            "pressure": main.get("pressure", 0),
            "visibility": data.get("visibility", 0) / 1000,
            "updated_at": updated_at,
            "sunrise": sunrise,
            "sunset": sunset,
            "unit": "°F" if use_fahrenheit else "°C"
        }

    @classmethod
    def parse_forecast(cls, data: Dict[str, Any], use_fahrenheit: bool = False) -> list:
        """Parses 5-day forecast data into daily summaries"""
        forecast_list = data.get("list", [])
        daily_data = {}
        
        for item in forecast_list:
            dt_txt = item.get("dt_txt", "")
            date_str = dt_txt.split(" ")[0]
            
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            formatted_date = date_obj.strftime("%a %d %b")
            
            main = item.get("main", {})
            temp = main.get("temp", 0.0)
            weather = item.get("weather", [{}])[0]
            condition = weather.get("main", "Clear")
            
            if formatted_date not in daily_data:
                daily_data[formatted_date] = {
                    "temps": [temp],
                    "conditions": [condition]
                }
            else:
                daily_data[formatted_date]["temps"].append(temp)
                daily_data[formatted_date]["conditions"].append(condition)
                
        final_forecast = []
        for day, info in list(daily_data.items())[:5]:
            min_c = min(info["temps"])
            max_c = max(info["temps"])
            most_common_condition = max(set(info["conditions"]), key=info["conditions"].count)
            
            if use_fahrenheit:
                min_temp = cls.celsius_to_fahrenheit(min_c)
                max_temp = cls.celsius_to_fahrenheit(max_c)
            else:
                min_temp = min_c
                max_temp = max_c
                
            final_forecast.append({
                "day": day,
                "min_temp": min_temp,
                "max_temp": max_temp,
                "condition": most_common_condition
            })
            
        return final_forecast