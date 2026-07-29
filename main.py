# To run and test the code you need to update 4 places:
# 1. Change MY_EMAIL/MY_PASSWORD to your own details.
# 2. Go to your email provider and make it allow less secure apps.
# 3. Update the SMTP ADDRESS to match your email provider.
# 4. Update birthdays.csv to contain today's month and day.
# See the solution video in the 100 Days of Python Course for explainations.
import os
import requests
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient


OWN_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"
api_key = os.environ.get("OWN_API_KEY")
account_sid = os.environ.get("ACCOUNT_SID")
auth_token =  os.environ.get("AUTH_TOKEN")


parameters = {
        "lat":6.451140,
        "lon":3.388400,
        "appid":api_key,
        "cnt":4
            }

response = requests.get(OWN_Endpoint,params=parameters)
response.raise_for_status()
print(response.status_code)
data = response.json()

hour_3 = data["list"][0]["weather"][0]["id"]
hour_6 = data["list"][1]["weather"][0]["id"]
hour_9 = data["list"][2]["weather"][0]["id"]
hour_12 = data["list"][3]["weather"][0]["id"]

will_rain = False

# if hour_3 < 700 or hour_6 < 700 or hour_9 < 700 or hour_12 < 700 :
#     print("bring an umbrella")

for hour in data["list"]:
    condition_code = hour["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True

if will_rain:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}
    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages.create(
        body="Its going to rain today don't forget to bring an Umbrella ☂️",
        from_="whatsapp:+14155238886",
        to="whatsapp:+2348032009394",
    )

    # noinspection string-conversion-without-dunder-method
    print(message.status)


