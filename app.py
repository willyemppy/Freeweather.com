import os
import json
from urllib.request import urlopen
from flask import Flask, render_template, url_for, request

app = Flask(__name__, template_folder="templates")


def openWeatherAPI(location):
    try:
        # geolocation api to generate the longitude and latitude of the specified location
        with urlopen(
            f"http://api.openweathermap.org/geo/1.0/direct?q={location}&limit=1&appid=44bdf697b18c02331c87caa919ba8464"
        ) as source:
            data = source.read()
            data1 = json.loads(data)
        latitude = data1[0].get("lat")
        longitude = data1[0].get("lon")
    except Exception as error:
        return 0, 0, 0  # Return default values in case of an error

    try:
        # using the actual weather API to generate the weather of the specified location, using the longitude and latitude obtained above
        with urlopen(
            f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid=44bdf697b18c02331c87caa919ba8464"
        ) as source:
            data = source.read()
            new_data = json.loads(data)
        currentTemp = round(new_data["main"]["temp"] - 273.15, 1)
        feels_like = round(new_data["main"]["feels_like"] - 273.15, 1)
        windSpeed = round(new_data["wind"]["speed"])
    except Exception as error:
        return 0, 0, 0  # Return default values in case of an error

    return currentTemp, feels_like, windSpeed


# Talks to the open weather api and then asks it to return the weather in a specify city and then displays a nice summary of the city
# def displayCountry(location):
#     try:
#         openai.api_key = "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"
#         response = openai.Completion.create(
#             model="text-davinci-003",
#             prompt=f"describe {location} in 1 sentence",
#             temperature=0,
#             max_tokens=60,
#             top_p=1,
#             frequency_penalty=0,
#             presence_penalty=0,
#         )
#         reply = response["choices"][0]["text"]
#     except Exception as error:
#         return "Unable to fetch location description"
#     return reply


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/<location>", methods=["GET", "POST"])
def displayWeather(location):
    location = request.args.get("location")
    currentTemp, feels_like, windSpeed = openWeatherAPI(
        location
    )  # Unpacking the tuple returned from the openweather api function

    return render_template(
        "weather.html",
        temperature=currentTemp,
        feels_like=feels_like,
        wind_speed=windSpeed,
        location1=location,
    )


if __name__ == "__main__":
    app.run()
app.debug = True
