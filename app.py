import json
from urllib.request import urlopen
from flask import Flask, render_template, url_for, request, flash, redirect

app = Flask(__name__, template_folder="templates")


def openWeatherAPI(location):
    try:
        # geolocation api to generate the longitude and latitude of the specified location
        with urlopen(
                f"http://api.openweathermap.org/geo/1.0/direct?q={location}&limit=1&appid=storage"
        ) as source:
            data = source.read()
            data1 = json.loads(data)
        latitude = data1[0].get("lat")
        longitude = data1[0].get("lon")
    except Exception as error:
        return 0, 0, 0  # Return default values in case of an error

    try:
        # using the actual weather API to generate the weather of the specified location,
        # using the longitude and latitude obtained above
        with urlopen(
                f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid=storage"
        ) as source:
            data = source.read()
            new_data = json.loads(data)
        currentTemp = round(new_data["main"]["temp"] - 273.15, 1)
        feels_like = round(new_data["main"]["feels_like"] - 273.15, 1)
        windSpeed = round(new_data["wind"]["speed"])
    except Exception as error:
        return 0, 0, 0  # Return default values in case of an error

    return currentTemp, feels_like, windSpeed


# root URL
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        # Using request.form.get to get a form field in a POST request
        location = request.form.get("location")
        if location:
            # Check if 'location' contains only letters
            if location.isalpha():
                return redirect(url_for('displayWeather', location=location))
            else:
                flash("Enter only letters", "error")
        else:
            flash("Location is required", "error")

    return render_template("index.html")


@app.route("/<location>", methods=["GET", "POST"])
def displayWeather(location):
    # location = request.args.get("location")
    currentTemp, feels_like, windSpeed = openWeatherAPI(
        location
    )  # Unpacking the tuple returned from the openweather api function

    return render_template(
        "weather.html",
        temperature=currentTemp,
        feels_like=feels_like,
        wind_speed=windSpeed,
        location=location,
    )


if __name__ == "__main__":
    app.run()
    app.debug = True
