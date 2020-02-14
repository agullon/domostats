import requests, json, time, configparser

HALL = 'entrada'
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
        currentTemp = str(sensorsResponse['14']['state']['temperature']/100) + 'ºC'
        return "Dormitorio: " + currentTemp
    elif(room == HALL):
        currentTemp = str(sensorsResponse['5']['state']['temperature']/100) + 'ºC'
        return "Entrada: " + currentTemp

def start():
    set_endpoint()

def main():
    start()
    print(temperature_status(HALL))
    print(temperature_status(MAIN_ROOM))

if __name__ == '__main__':
    main()        