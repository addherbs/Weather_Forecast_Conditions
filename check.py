import html
import requests
from bs4 import BeautifulSoup

url = 'https://api.weather.gov/points/38.9588,-94.624/forecast'
headers = {'Accept': 'application/vnd.noaa.dwml+xml'}

r = requests.get(url, headers=headers)
xml = r.content.decode('utf-8')
parsed_content = html.unescape(xml)

soup = BeautifulSoup(parsed_content, 'html.parser')
temp_divs = soup.findAll ('temperature')
wind_divs = soup.findAll ('wind-speed')
direction_divs = soup.findAll ('direction')
prob_divs = soup.findAll ('probability-of-precipitation')
condition_icon_divs = soup.findAll ('conditions-icon')

temperature_values = []
wind_speeds = []
direction_values = []
probability_of_precipitation = []
condition_icons = []
water_state_list = []

min_temp = []
max_temp = []

for i in temp_divs:
    if 'Minimum' in i.getText():
        for k in i.findAll('value'):
            min_temp.append(k.string)
    else:
        for k in i.findAll('value'):
            max_temp.append(k.string)
for j in wind_divs:
    wind_speed_value_divs = j.findAll('value')
    for k in wind_speed_value_divs:
        wind_speeds.append(k.string)
for j in direction_divs:
    direction_value_divs = j.findAll('value')
    for k in direction_value_divs:
        direction_values.append(k.string)
for j in prob_divs:
    prob_value_divs = j.findAll('value')
    for k in prob_value_divs:
        probability_of_precipitation.append(k.string)
for j in condition_icon_divs:
    condition_link = j.findAll('icon-link')
    for k in condition_link:
        condition_icons.append(k.string)


print("The Minimum Value is: ", min_temp[0])
print("The Minimum Value is: " , min_temp[0])
print ('wind speed is: ', wind_speeds[0])
print ('direction value is: ', direction_values[0])
print ('probability is', probability_of_precipitation[0])
