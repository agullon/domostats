import hue_requests, temperature

KITCHEN = 'kitchen'
OUTDOOR = 'street'
HALL = 'hall'
MAIN_ROOM = 'main room'

spanish_name = {
    KITCHEN: 'interior',
    OUTDOOR: 'exterior',
    HALL: 'hall',
    MAIN_ROOM: 'habitación'
}

sensor_id = {
    KITCHEN: '14',
    OUTDOOR: '5',
    HALL: '45',
    MAIN_ROOM: '52'
}

def get_all_info():
    temperature.get_all_info()

if __name__ == '__main__':
    hue_requests.set_endpoint()
    get_all_info()        
