from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__)

def get_data(timeseries, target_time):
    entry = next((ts for ts in timeseries if ts['time'] == target_time), None)
    if entry:
        details = entry['data']['instant']['details']
        return {
            'temperature': details.get('air_temperature'),
            'wind_speed': details.get('wind_speed'),
            'precipitation': entry['data']['next_1_hours']['details'].get('precipitation_amount')
        }
    return None
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/options', methods=['POST'])
def options():
    data = request.json
    lat = data['lat']
    lng = data['lng']
    date = data['date']
    minTemp = int(data['minTemp'])
    maxTemp = int(data['maxTemp'])
    minPrecipitation = float(data['minPrecipitation'])
    maxPrecipitation = float(data['maxPrecipitation'])
    minWind = int(data['minWind'])
    maxWind = int(data['maxWind'])

    print(minWind, maxWind)
    if minTemp > maxTemp:
        print(minTemp, maxTemp)
        return jsonify({"error0": "Invalid options!"})
    elif minPrecipitation > maxPrecipitation:
        print(minPrecipitation, maxPrecipitation)
        return jsonify({"error0": "Invalid options!"})
    elif minWind > maxWind:
        print(minWind, maxWind)
        return jsonify({"error0": "Invalid options!"})
    else:

        url = f"https://api.met.no/weatherapi/locationforecast/2.0/mini.json?lat={lat}&lon={lng}"

        headers = {
            'User-Agent': 'CheckOUT!/1.0 (bedirhan_kurt_@outlook.com)'
        }

        data = requests.get(url, headers=headers).json()
        print(data)

        time = request.args.get('time', '2024-09-09T10:00:00Z')
        timeseries = data['properties']['timeseries']
        weather_data = get_data(timeseries, time)

        if weather_data:
            print(f"Temperature: {weather_data['temperature']}°C")
            print(f"Wind Speed: {weather_data['wind_speed']} km/h")
            print(f"Rain: {weather_data['precipitation']} mm")
        else:
            print("No data found for the specified date and time.")


if __name__ == '__main__':
    app.run(debug=True, port=5002)