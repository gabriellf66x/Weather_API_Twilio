import os
import requests
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

OMW_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"
api = os.environ.get("OWM_API_KEY")
account_sid = "YOUR ACCOUNT SID"
auth_token = os.environ.get("AUTH_TOKEN")

weather_param = {
    "lat": 100.9999,  # YOUR LATITUDE
    "lon": -100.9999,  # YOUR LONGITUDE
    "appid": api,
    "cnt": 3,
}


def umbrella():
    response = requests.get(OMW_Endpoint, weather_param)
    response.raise_for_status()
    data = response.json()

    will_rain = False
    for hour_data in data["list"]:
        cond_code = hour_data['weather'][0]["id"]
        if int(cond_code) < 700:
            will_rain = True

    if will_rain:
        proxy_client = TwilioHttpClient()
        proxy_client.session.proxies = {'https': os.environ['https_proxy']}

        client = Client(account_sid, auth_token, http_client=proxy_client)

        message = client.messages \
            .create(
            body="It's going to rain today!",
            from_='YOUR PHONE NUMBER',
            to='OTHER PHONE NUMBER'
        )
        print(message.status)


umbrella()
