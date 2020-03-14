import requests, json, time, configparser

KITCHEN = 'cocina'
MAIN_ROOM = 'dormitorio'

def set_endpoint():
    global endpoint
    responseObj = requests.get('https://discovery.meethue.com/')
    responseJson = json.loads(responseObj.text[1:-2])
    hue_bridge_ip = responseJson['internalipaddress']

    config = configparser.RawConfigParser()
    config.read('../keys/connection_tokens.ini')
    hue_conn_hash = config.get('hue', 'local.hash')

    endpoint = 'http://' + hue_bridge_ip + '/api/' + hue_conn_hash + '/'

def getElement(element=''):
    response = requests.get(endpoint + element)
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return 'Request for ' + element + ' failed!'

def temperature_status(room):
    sensorsResponse = getElement("sensors")
    if (room == MAIN_ROOM):
        currentTemp = round(sensorsResponse['14']['state']['temperature']/100 - 1.5,2)
        return "Dormitorio: " + str(currentTemp) + 'ºC'
    elif(room == KITCHEN):
        currentTemp = round(sensorsResponse['5']['state']['temperature']/100 + 1.0,2)
        return "Cocina:     " + str(currentTemp) + 'ºC'

def start():
    set_endpoint()

def main():
    start()
    print(temperature_status(KITCHEN))
    print(temperature_status(MAIN_ROOM))

if __name__ == '__main__':
    main()        