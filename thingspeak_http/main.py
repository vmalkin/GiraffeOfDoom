import requests

# https://api.thingspeak.com/update?api_key=HSUZINZPK1KCPHU7&field1=2&field2=3

api_key = "api_key=HSUZINZPK1KCPHU7"
update_url = "https://api.thingspeak.com/update?"
payload = {'field1': '2', 'field2' : '3'}

url = update_url + api_key

r = requests.get(url, params=payload)
# return the url that was sent
print(r.url)

# return the response from THingSpeak.
print(r.text)