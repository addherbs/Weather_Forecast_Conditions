from bs4 import BeautifulSoup
from flask import Flask, render_template, request
import requests
import html
import json
from urllib.parse import parse_qs
app = Flask(__name__)

def run_query(longitude, latitude):
    url="https://graphical.weather.gov:443/xml/SOAP_server/ndfdXMLserver.php"
    #headers = {'content-type': 'application/soap+xml'}
    headers = {'content-type': 'text/xml'}
	lat = str(latitude)
	log = str(longitude)
    body = """<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/" SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
    <SOAP-ENV:Body>
    <ns3591:NDFDgen xmlns:ns3591="uri:DWMLgen">
    <latitude xsi:type="xsd:string">""" + lat + """</latitude>
    <longitude xsi:type="xsd:string">""" + log + """</longitude>
    <product xsi:type="xsd:string">time-series</product>
    <startTime xsi:type="xsd:string">2017-05-02T00:00:00</startTime>
    <endTime xsi:type="xsd:string">2017-05-02T23:59:59</endTime>
    <Unit xsi:type="xsd:string">e</Unit>
    <weatherParameters>
    <maxt xsi:type="xsd:boolean">1</maxt>
    <mint xsi:type="xsd:boolean">1</mint>
    <temp xsi:type="xsd:boolean">0</temp>
    <td xsi:type="xsd:boolean">0</td>
    <pop12 xsi:type="xsd:boolean">1</pop12>
    <qpf xsi:type="xsd:boolean">0</qpf>
    <sky xsi:type="xsd:boolean">1</sky>
    <snow xsi:type="xsd:boolean">0</snow>
    <wspd xsi:type="xsd:boolean">1</wspd>
    <wdir xsi:type="xsd:boolean">1</wdir>
    <wx xsi:type="xsd:boolean">0</wx>
    <waveh xsi:type="xsd:boolean">1</waveh>
    <icons xsi:type="xsd:boolean">1</icons>
    <critfireo xsi:type="xsd:boolean">0</critfireo>
    <dryfireo xsi:type="xsd:boolean">0</dryfireo>
    <rhm xsi:type="xsd:boolean">0</rhm>
    <apt xsi:type="xsd:boolean">0</apt>
    <tcwspdabv34i xsi:type="xsd:boolean">0</tcwspdabv34i>
    <tcwspdabv50i xsi:type="xsd:boolean">0</tcwspdabv50i>
    <tcwspdabv64i xsi:type="xsd:boolean">0</tcwspdabv64i>
    <tcwspdabv34c xsi:type="xsd:boolean">0</tcwspdabv34c>
    <tcwspdabv50c xsi:type="xsd:boolean">0</tcwspdabv50c>
    <tcwspdabv64c xsi:type="xsd:boolean">0</tcwspdabv64c>
    <conhazo xsi:type="xsd:boolean">0</conhazo>
    <ptornado xsi:type="xsd:boolean">0</ptornado>
    <phail xsi:type="xsd:boolean">0</phail>
    <ptstmwinds xsi:type="xsd:boolean">0</ptstmwinds>
    <pxtornado xsi:type="xsd:boolean">0</pxtornado>
    <pxhail xsi:type="xsd:boolean">0</pxhail>
    <pxtstmwinds xsi:type="xsd:boolean">0</pxtstmwinds>
    <ptotsvrtstm xsi:type="xsd:boolean">0</ptotsvrtstm>
    <ptotxsvrtstm xsi:type="xsd:boolean">0</ptotxsvrtstm>
    <tmpabv14d xsi:type="xsd:boolean">0</tmpabv14d>
    <tmpblw14d xsi:type="xsd:boolean">0</tmpblw14d>
    <tmpabv30d xsi:type="xsd:boolean">0</tmpabv30d>
    <tmpblw30d xsi:type="xsd:boolean">0</tmpblw30d>
    <tmpabv90d xsi:type="xsd:boolean">0</tmpabv90d>
    <tmpblw90d xsi:type="xsd:boolean">0</tmpblw90d>
    <prcpabv14d xsi:type="xsd:boolean">0</prcpabv14d>
    <prcpblw14d xsi:type="xsd:boolean">0</prcpblw14d>
    <prcpabv30d xsi:type="xsd:boolean">0</prcpabv30d>
    <prcpblw30d xsi:type="xsd:boolean">0</prcpblw30d>
    <prcpabv90d xsi:type="xsd:boolean">0</prcpabv90d>
    <prcpblw90d xsi:type="xsd:boolean">0</prcpblw90d>
    <precipa_r xsi:type="xsd:boolean">0</precipa_r>
    <sky_r xsi:type="xsd:boolean">0</sky_r>
    <td_r xsi:type="xsd:boolean">0</td_r>
    <temp_r xsi:type="xsd:boolean">0</temp_r>
    <wdir_r xsi:type="xsd:boolean">0</wdir_r>
    <wspd_r xsi:type="xsd:boolean">0</wspd_r>
    <wgust xsi:type="xsd:boolean">0</wgust>
    <iceaccum xsi:type="xsd:boolean">0</iceaccum>
    <maxrh xsi:type="xsd:boolean">0</maxrh>
    <minrh xsi:type="xsd:boolean">0</minrh>
    </weatherParameters>
    </ns3591:NDFDgen>
    </SOAP-ENV:Body>
    </SOAP-ENV:Envelope>"""

    response = requests.post(url,data=body,headers=headers)
    #print (response.content)
    xml_content = response.content.decode('utf-8')
    # now we need to parse xml_content
    parsed_content = html.unescape(xml_content)
    # print ('response is', parsed_content)
    soup = BeautifulSoup(parsed_content, 'html.parser')
    temp_divs = soup.findAll('temperature')
    wind_divs = soup.findAll('wind-speed')
    direction_divs = soup.findAll('direction')
    cloud_amount_divs = soup.findAll('cloud-amount')
    prob_divs = soup.findAll('probability-of-precipitation')
    condition_icon_divs = soup.findAll('conditions-icon')
    # water_state_divs = soup.findAll('water-state')
    temperature_values = []
    wind_speeds = []
    direction_values = []
    cloud_amount = []
    probability_of_precipitation = []
    condition_icons = []
    water_state_list = []
    temperature_values = {}
    for i in temp_divs:
        print ('temp div is', i)
        if 'Minimum' in i.getText():
            temperature_values['minimum_temps'] = []
            for k in i.findAll('value'):
                temperature_values['minimum_temps'].append(k.string)
        else:
            temperature_values['maximum_temps'] = []
            for k in i.findAll('value'):
                temperature_values['maximum_temps'].append(k.string)
    for j in wind_divs:
        wind_speed_value_divs = j.findAll('value')
        for k in wind_speed_value_divs:
            wind_speeds.append(k.string)
    for j in direction_divs:
        direction_value_divs = j.findAll('value')
        for k in direction_value_divs:
            direction_values.append(k.string)
    for j in cloud_amount_divs:
        cloud_amount_values = j.findAll('value')
        for k in cloud_amount_values:
            cloud_amount.append(k.string)
    for j in prob_divs:
        prob_value_divs = j.findAll('value')
        for k in prob_value_divs:
            probability_of_precipitation.append(k.string)
    for j in condition_icon_divs:
        condition_link = j.findAll('icon-link')
        for k in condition_link:
            condition_icons.append(k.string)
    print ('condition icons are', condition_icons)
    print ('temperatures are', temperature_values)
    print ('wind speeds are', wind_speeds)
    print ('direction values are', direction_values)
    print ('cloud amount is', cloud_amount)
    print ('probability is', probability_of_precipitation)
    return (condition_icons, temperature_values, wind_speeds, direction_values, cloud_amount, probability_of_precipitation)

@app.route('/', methods=['GET', 'POST'])
def show_index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        formdata = request.get_json('data')
        parsed_data = parse_qs(formdata)
        latitude, longitude = float(parsed_data['latitude'][0]), float(parsed_data['longitude'][0])
        data = run_query(longitude, latitude)
        print ('Data we got is', data)
        if data[0] == []:
            return json.dumps({'error': 'There seems to be an error'}), 400, {'contentType': 'application/json'}
        return json.dumps({'success': data}), 200, {'contentType': 'application/json'}

if __name__ == '__main__':
    app.run()
