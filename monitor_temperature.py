import hue_requests, temperature, domostats, database
import datetime, time
      
while True:
    if datetime.datetime.now().minute % 6 == 0: 
        hue_requests.set_endpoint()
        temp, date = temperature.get_room_info(domostats.OUTDOOR)
        database.add_temperature(domostats.OUTDOOR, temp, date)
        temp, date = temperature.get_room_info(domostats.INDOOR)
        database.add_temperature(domostats.INDOOR, temp, date)
    time.sleep(60)
