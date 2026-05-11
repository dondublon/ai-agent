def get_current_weather(city: str):
    """Get the current weather in a given city."""
    # For the sake of this example, we'll return a hardcoded weather report.
    return f"The current weather in {city} is sunny with a temperature of 25°C."

TOOLS = {
    "get_current_weather": get_current_weather  
}