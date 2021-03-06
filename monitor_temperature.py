import hue_requests, temperature, domostats, database
import datetime, time
      
while True:
    if datetime.datetime.now().minute % 6 == 0: 
        hue_requests.set_endpoint()
        temp, date = temperature.get_room_info(domostats.OUTDOOR)
        database.add_temperature(domostats.OUTDOOR, temp, date)
        temp, date = temperature.get_room_info(domostats.KITCHEN)
        database.add_temperature(domostats.KITCHEN, temp, date)
        temp, date = temperature.get_room_info(domostats.HALL)
        database.add_temperature(domostats.HALL, temp, date)
        temp, date = temperature.get_room_info(domostats.MAIN_ROOM)
        database.add_temperature(domostats.MAIN_ROOM, temp, date)
    time.sleep(60)
