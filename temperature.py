import hue_requests, domostats, utils
import requests, json, time, datetime

TEMP_OFFSET = {
    domostats.INDOOR: -1.5,
    domostats.OUTDOOR: +1.0
}

def get_room_info(room):
    resp = hue_requests.get('sensors/' + domostats.sensor_id[room])
    temperature = round(resp['state']['temperature']/100 + TEMP_OFFSET[room],1)
    time_hue = resp['state']['lastupdated'] 
    time_str = utils.date_format(utils.date_diff_hours(time_hue), '%Y-%m-%dT%H:%M:%S')
    return temperature, time_str

def all_rooms():
    text = 'Current temperature:\n'
    text += room_status(domostats.INDOOR) + '\n'
    text += room_status(domostats.OUTDOOR)
    return text

def room_status(room):
    temperature, time = get_room_info(room)
    return room + ' is ' + '{:.1f}ºC'.format(temperature) + ' at ' + utils.date_format(utils.date_diff_hours(time), '%H:%M:%S  %B %d, %Y')

if __name__ == '__main__':
    hue_requests.set_endpoint()
    print(all_rooms())