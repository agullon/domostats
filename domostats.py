import hue_requests, temperature

KITCHEN = 'kitchen'
BEDROOM = 'bedroom'

spanish_name = {
    KITCHEN: 'cocina',
    BEDROOM: 'habitación'
}

sensor_id = {
    KITCHEN: '14',
    BEDROOM: '5'
}

def get_all_info():
    temperature.get_all_info()

if __name__ == '__main__':
    hue_requests.set_endpoint()
    get_all_info()        
