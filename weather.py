import httpx
from mcp.server.fastmcp import FastMCP

from dotenv import load_dotenv
import os

load_dotenv()

# FastMCP server
mcp = FastMCP("weather")

@mcp.tool()
async def get_weather(location:str) -> dict:
    """특정 위치의 날씨 정보를 가져온다. """
    apiKey = os.getenv("OPENWEATHERMAP_APIKEY")
    lang:str = "kr"
    units:str = 'metric' #화씨 온도를 섭씨 온도로 변경
    api:str = f"http://api.openweathermap.org/data/2.5/weather?q={location}&APPID={apiKey}&lang={lang}&units={units}"
    async with httpx.AsyncClient() as client:
        response = await client.get(api)
        return await weather_forecast_prompt(response)
    

@mcp.prompt()
async def weather_forecast_prompt(forecast:dict) -> str:
    return f"""
        {forecast['name']}의 예보:

        현재 온도: {forecast['main']['temp']} °C 
        체감 온도: {forecast["main"]["feels_like"]} °C 
        """

if __name__ == "__main__":
    mcp.run(transport='stdio')

