import temperature
import requests, json, configparser

endpoint = None

def set_endpoint():
    global endpoint

    resp_obj = requests.get('https://discovery.meethue.com/')
    resp_json = json.loads(resp_obj.text[1:-2])
    hue_bridge_ip = resp_json['internalipaddress']

    config = configparser.RawConfigParser()
    config.read('../keys/connection_tokens.ini')
    hue_conn_hash = config.get('hue', 'local.hash')

    endpoint = 'http://' + hue_bridge_ip + '/api/' + hue_conn_hash + '/'

def get(element=''):
    response = requests.get(endpoint + element)
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return 'Request for ' + element + ' failed!'