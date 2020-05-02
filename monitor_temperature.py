import hue_requests, temperature, domostats, database
import datetime, time
      
while True:
    if datetime.datetime.now().minute % 6 == 0: 
        hue_requests.set_endpoint()
        temp, date = temperature.get_room_info(domostats.BEDROOM)
        database.add_temperature(domostats.BEDROOM, temp, date)
        temp, date = temperature.get_room_info(domostats.KITCHEN)
        database.add_temperature(domostats.KITCHEN, temp, date)
    time.sleep(60)