#!/usr/bin/env python3
"""
Example script demonstrating how to use the Weather MCP Client
"""

import asyncio
from mcp_stdio_client import WeatherMCPClient


async def example_usage():
    """Example of how to use the WeatherMCPClient"""
    client = WeatherMCPClient()
    
    try:
        print("🚀 Starting Weather MCP Client Example")
        
        # Connect to the weather server
        print("\n1. Connecting to weather server...")
        if not await client.connect_to_weather_server():
            print("❌ Failed to connect to server")
            return
        
        # List available tools
        print("\n2. Listing available tools...")
        await client.list_available_tools()
        
        # Query weather for some example locations
        locations = ["Beijing", "New York", "London", "Tokyo"]

        print("\n3. Querying weather for example locations...")
        for location in locations:
            print(f"\n--- Weather for {location} ---")
            result = await client.query_weather(location)
            print(result)

            # Small delay between requests
            await asyncio.sleep(1)

        # Test weather alerts for some US states
        print("\n4. Testing weather alerts for US states...")
        states = ["CA", "NY", "FL", "TX"]
        for state in states:
            print(f"\n--- Weather Alerts for {state} ---")
            result = await client.get_weather_alerts(state)
            print(result)

            # Small delay between requests
            await asyncio.sleep(1)

        # Test direct coordinate forecast
        print("\n5. Testing direct coordinate forecast...")
        coordinates = [
            (37.7749, -122.4194, "San Francisco"),
            (40.7128, -74.0060, "New York City"),
            (51.5074, -0.1278, "London")
        ]

        for lat, lon, name in coordinates:
            print(f"\n--- Forecast for {name} ({lat}, {lon}) ---")
            result = await client.get_weather_forecast(lat, lon)
            print(result)

            # Small delay between requests
            await asyncio.sleep(1)
        
        print("\n✅ Example completed successfully!")
        
    except Exception as e:
        print(f"❌ Error in example: {str(e)}")
    finally:
        await client.cleanup()


async def interactive_mode():
    """Run the client in interactive mode"""
    client = WeatherMCPClient()
    
    try:
        if await client.connect_to_weather_server():
            await client.interactive_chat()
    finally:
        await client.cleanup()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        print("🌟 Running in interactive mode...")
        asyncio.run(interactive_mode())
    else:
        print("🔧 Running example usage...")
        print("💡 Use --interactive flag for interactive mode")
        asyncio.run(example_usage())
