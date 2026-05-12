import time

from config import CACHE_TTL_SECONDS
from logging_config import logger
import requests
def get_current_weather(arguments: dict):
    """Get the current weather in a given city."""
    url = "http://api.weatherapi.com/v1/current.json"
    API_KEY = "312f5712e6b047058f2200626252611"
    city = arguments.get("city")
    if not city:
        return "City argument is missing."
    resp = requests.get(url, {"key":API_KEY, "q":city})
    res = f"{city} is wrong city"
    if not resp.status_code == 400:
        resp.raise_for_status()
        data = resp.json()
        res = f"Weather in {data["location"]["name"]}: temperature is {data["current"]["temp_c"]}\u00B0C , {data["current"]["condition"]["text"]},\n\
        speed of wind: {data["current"]["wind_kph"]} kph, Humidity is {data["current"]["humidity"]}%"
    return res


_rates_cache = None
def get_exchange_rate(arguments: dict)->str:
    global _rates_cache
    url = "https://data.fixer.io/api/latest"
    access_key = "b2d71961ebe71a300a02e73d03b6ebc8"
   
    from_currency = arguments.get("from_currency")
    to_currency = arguments.get("to_currency")
    result = ""
    if not from_currency:
        result += "from_currency argument is missing. "
    if not to_currency:
        result += "to_currency argument is missing. "
    if not result:
        use_cache = False
        if _rates_cache is not None:
            rates_timestamp = _rates_cache["timestamp"]
            rates_age = time.time() - rates_timestamp

            if rates_age < CACHE_TTL_SECONDS:
                use_cache = True
        if use_cache:
            data = _rates_cache
            logger.debug("Using cached exchange rates.")
        else: 
             logger.debug("Fetching new exchange rates.")
             resp = requests.get(url, params={"access_key":access_key})
             resp.raise_for_status()
             data = resp.json()
             _rates_cache =data
        rates = data["rates"]    
        rateFrom = rates[from_currency]
        rateTo = rates[to_currency]
        rateFromTo = round(rateTo / rateFrom, 2)
        result = f"The current exchange rate from {from_currency} to {to_currency} is {rateFromTo}."
    return result   

TOOLS = {
    "get_current_weather": get_current_weather,
    "get_exchange_rate": get_exchange_rate  
}