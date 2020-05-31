import hue_requests, domostats, utils
import requests, json, time, datetime

TEMP_OFFSET = {
    domostats.HALL: +1.0,
    domostats.KITCHEN: -1.5
}

def get_room_info(room):
    resp = hue_requests.get('sensors/' + domostats.sensor_id[room])
    temperature = round(resp['state']['temperature']/100 + TEMP_OFFSET[room],1)
    time_hue = resp['state']['lastupdated'] 
    time_str = utils.date_format(utils.date_diff_hours(time_hue), '%Y-%m-%dT%H:%M:%S')
    return temperature, time_str

def all_rooms():
    text = 'Ahora mismo:\n'
    text += room_status(domostats.KITCHEN) + '\n'
    text += room_status(domostats.HALL) + '\n'
    return text

def room_status(room):
    temperature, time = get_room_info(room)
    return 'En la ' + domostats.spanish_name[room] + ' hay ' + '{:.1f}ºC'.format(temperature)

if __name__ == '__main__':
    hue_requests.set_endpoint()
    print(all_rooms())