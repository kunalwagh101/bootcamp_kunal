
"""
Consume OpenWeatherMap API

Objective: Fetch weather data for a specified location.
Task: Create a Python CLI tool that uses the OpenWeatherMap API 
(https://api.openweathermap.org/data/2.5/weather?q={city name}&appid={API key}) 
to fetch and display weather information. You'll need to sign up for a free API key.
Expected Output: Weather details for the specified city.

"""
import requests
import typer

def cli(city:str,country_code:str) -> str:
    url = "https://api.openweathermap.org/data/2.5/weather?q="+city+","+country_code+"&appid=da29940ff36f3a8e9495765d22c01cfc"
    api_call = requests.get(url).json()
    name =  api_call["name"]
    temp =  round(api_call["main"]["temp"] - 273.15,3)
    humidity =  api_call["main"]["humidity"]
    pressure =  api_call["main"]["pressure"]

    print(f" city = {name} , tempreture = {temp}°C ,humidity = {humidity}g/m³, pressure = {pressure}psi")
    
app  = typer.Typer()

@app.command()
def main(city:str = typer.Argument("Mumbai") ,  country_code: str = typer.Argument("IN")) :
    country_code = country_code.upper()
    try :
        return cli(city ,country_code )
    except ValueError :
        typer.echo(f"city name {city} or country_code {country_code} is wrong")
        


if __name__ == "__main__" :
    app()