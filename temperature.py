import hue_requests, domostats, utils
import requests, json, time, datetime

TEMP_OFFSET = {
    domostats.KITCHEN: +1.0,
    domostats.BEDROOM: -1.5
}

def get_room_info(room):
    resp = hue_requests.get('sensors/' + domostats.sensor_id[room])
    temp = round(resp['state']['temperature']/100 + TEMP_OFFSET[room],2)
    time = resp['state']['lastupdated']# + str(datetime.timedelta(hours=2))
    return temp, time

def print_room_status(room):
    temp, time = get_room_info(room)
    return print(domostats.spanish_name[room] + ' {:.2f}ºC '.format(temp) + utils.format_date(time))

def print_all_info():
    print_room_status(domostats.KITCHEN)
    print_room_status(domostats.BEDROOM)

if __name__ == '__main__':
    hue_requests.set_endpoint()
    print_all_info()