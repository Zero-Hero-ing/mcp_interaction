import asyncio
from typing import Optional
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class WeatherMCPClient:
    """MCP Client specifically designed to communicate with the weather query server"""

    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()

    async def connect_to_weather_server(self):
        """Connect to the weather MCP server using uvx command"""
        try:
            # Use uvx to run the weather server
            server_params = StdioServerParameters(
                command="uvx",
                args=[
                    "--from",
                    "git+https://github.com/Zero-Hero-ing/Zero-Hero-ing.git",
                    "query_weather"
                ],
                env=None
            )

            print("Connecting to weather MCP server...")
            stdio_transport = await self.exit_stack.enter_async_context(
                stdio_client(server_params)
            )
            self.stdio, self.write = stdio_transport
            self.session = await self.exit_stack.enter_async_context(
                ClientSession(self.stdio, self.write)
            )

            # Initialize the session
            await self.session.initialize()

            # List available tools
            response = await self.session.list_tools()
            tools = response.tools
            print(f"✅ Connected successfully! Available tools: {[tool.name for tool in tools]}")

            # Print tool details
            for tool in tools:
                print(f"\n🔧 Tool: {tool.name}")
                print(f"   Description: {tool.description}")
                if hasattr(tool, 'inputSchema') and tool.inputSchema:
                    print(f"   Input Schema: {tool.inputSchema}")

            return True

        except Exception as e:
            print(f"❌ Failed to connect to weather server: {str(e)}")
            return False

    async def query_weather(self, location: str) -> str:
        """Query weather for a specific location"""
        if not self.session:
            raise RuntimeError("Not connected to server. Call connect_to_weather_server() first.")

        try:
            # Get available tools first
            tools_response = await self.session.list_tools()
            available_tools = [tool.name for tool in tools_response.tools]

            if not available_tools:
                return "No tools available on the server."

            print(f"🌤️  Querying weather for '{location}'...")

            # Check if location is a US state code for alerts
            if len(location) == 2 and location.upper().isalpha():
                if 'get_alerts' in available_tools:
                    print(f"   Using get_alerts for state: {location.upper()}")
                    result = await self.session.call_tool('get_alerts', {"state": location.upper()})
                    if hasattr(result, 'content'):
                        if isinstance(result.content, list):
                            return "\n".join([str(item) for item in result.content])
                        else:
                            return str(result.content)
                    else:
                        return str(result)

            # For other locations, we need coordinates for get_forecast
            # This is a simplified mapping - in a real app you'd use a geocoding service
            location_coords = {
                'beijing': (39.9042, 116.4074),
                'new york': (40.7128, -74.0060),
                'london': (51.5074, -0.1278),
                'tokyo': (35.6762, 139.6503),
                'san francisco': (37.7749, -122.4194),
                'paris': (48.8566, 2.3522),
                'sydney': (-33.8688, 151.2093),
                'los angeles': (34.0522, -118.2437),
                'chicago': (41.8781, -87.6298),
                'miami': (25.7617, -80.1918)
            }

            location_lower = location.lower()
            if location_lower in location_coords and 'get_forecast' in available_tools:
                lat, lon = location_coords[location_lower]
                print(f"   Using get_forecast for coordinates: {lat}, {lon}")
                result = await self.session.call_tool('get_forecast', {"latitude": lat, "longitude": lon})
                if hasattr(result, 'content'):
                    if isinstance(result.content, list):
                        return "\n".join([str(item) for item in result.content])
                    else:
                        return str(result.content)
                else:
                    return str(result)

            # If we can't handle the location, provide helpful information
            return f"""❓ Unable to query weather for '{location}'.

Available options:
1. For US weather alerts, use a 2-letter state code (e.g., 'CA', 'NY', 'TX')
2. For weather forecasts, use one of these supported cities:
   {', '.join(location_coords.keys())}

Available tools on server: {', '.join(available_tools)}"""

        except Exception as e:
            return f"❌ Error querying weather: {str(e)}"

    async def get_weather_forecast(self, latitude: float, longitude: float) -> str:
        """Get weather forecast for specific coordinates"""
        if not self.session:
            raise RuntimeError("Not connected to server. Call connect_to_weather_server() first.")

        try:
            print(f"🌤️  Getting forecast for coordinates: {latitude}, {longitude}")
            result = await self.session.call_tool('get_forecast', {
                "latitude": latitude,
                "longitude": longitude
            })

            if hasattr(result, 'content'):
                if isinstance(result.content, list):
                    return "\n".join([str(item) for item in result.content])
                else:
                    return str(result.content)
            else:
                return str(result)

        except Exception as e:
            return f"❌ Error getting forecast: {str(e)}"

    async def get_weather_alerts(self, state_code: str) -> str:
        """Get weather alerts for a US state"""
        if not self.session:
            raise RuntimeError("Not connected to server. Call connect_to_weather_server() first.")

        try:
            state_code = state_code.upper()
            print(f"🚨 Getting weather alerts for state: {state_code}")
            result = await self.session.call_tool('get_alerts', {"state": state_code})

            if hasattr(result, 'content'):
                if isinstance(result.content, list):
                    return "\n".join([str(item) for item in result.content])
                else:
                    return str(result.content)
            else:
                return str(result)

        except Exception as e:
            return f"❌ Error getting alerts: {str(e)}"

    async def list_available_tools(self):
        """List all available tools on the server"""
        if not self.session:
            raise RuntimeError("Not connected to server. Call connect_to_weather_server() first.")

        try:
            response = await self.session.list_tools()
            tools = response.tools

            print("\n📋 Available Tools:")
            for i, tool in enumerate(tools, 1):
                print(f"{i}. {tool.name}")
                print(f"   Description: {tool.description}")
                if hasattr(tool, 'inputSchema') and tool.inputSchema:
                    print(f"   Input Schema: {tool.inputSchema}")
                print()

            return tools

        except Exception as e:
            print(f"❌ Error listing tools: {str(e)}")
            return []

    async def interactive_chat(self):
        """Run an interactive chat session"""
        print("\n🌟 Weather MCP Client Interactive Mode")
        print("Commands:")
        print("  - Type a location to get weather (e.g., 'Beijing', 'New York')")
        print("  - 'forecast <lat> <lon>' to get forecast for coordinates")
        print("  - 'alerts <state>' to get alerts for US state (e.g., 'alerts CA')")
        print("  - 'tools' to list available tools")
        print("  - 'help' to show this help message")
        print("  - 'quit' to exit")
        print("-" * 60)

        while True:
            try:
                user_input = input("\n🌍 Enter location or command: ").strip()

                if user_input.lower() == 'quit':
                    print("👋 Goodbye!")
                    break
                elif user_input.lower() == 'tools':
                    await self.list_available_tools()
                elif user_input.lower() == 'help':
                    print("\n📖 Available Commands:")
                    print("  • Location names: Beijing, New York, London, Tokyo, etc.")
                    print("  • US state codes: CA, NY, TX, FL, etc. (for alerts)")
                    print("  • forecast <lat> <lon>: Get forecast for coordinates")
                    print("  • alerts <state>: Get weather alerts for US state")
                    print("  • tools: List available server tools")
                    print("  • help: Show this help message")
                    print("  • quit: Exit the client")
                elif user_input.lower().startswith('forecast '):
                    parts = user_input.split()
                    if len(parts) == 3:
                        try:
                            lat = float(parts[1])
                            lon = float(parts[2])
                            result = await self.get_weather_forecast(lat, lon)
                            print(f"\n📊 Weather Forecast:\n{result}")
                        except ValueError:
                            print("❌ Invalid coordinates. Use: forecast <latitude> <longitude>")
                    else:
                        print("❌ Usage: forecast <latitude> <longitude>")
                elif user_input.lower().startswith('alerts '):
                    parts = user_input.split()
                    if len(parts) == 2:
                        state = parts[1]
                        result = await self.get_weather_alerts(state)
                        print(f"\n🚨 Weather Alerts:\n{result}")
                    else:
                        print("❌ Usage: alerts <state_code> (e.g., alerts CA)")
                elif user_input:
                    result = await self.query_weather(user_input)
                    print(f"\n📊 Weather Result:\n{result}")
                else:
                    print("Please enter a location or command. Type 'help' for available commands.")

            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {str(e)}")

    async def cleanup(self):
        """Clean up resources"""
        await self.exit_stack.aclose()


async def main():
    """Main function to run the weather MCP client"""
    client = WeatherMCPClient()

    try:
        # Connect to the weather server
        if await client.connect_to_weather_server():
            # Start interactive chat
            await client.interactive_chat()
        else:
            print("Failed to connect to the weather server. Please check:")
            print("1. uvx is installed")
            print("2. The repository URL is accessible")
            print("3. Your internet connection")

    except KeyboardInterrupt:
        print("\n👋 Interrupted by user")
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
    finally:
        await client.cleanup()


if __name__ == "__main__":
    asyncio.run(main())