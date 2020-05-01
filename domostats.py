import hue_requests, temperature

KITCHEN = 'kitchen'
BEDROOM = 'bedroom'

spanish_name = {
    KITCHEN: 'cocina',
    BEDROOM: 'dormitorio'
}

sensor_id = {
    KITCHEN: '5',
    BEDROOM: '14'
}

def get_all_info():
    temperature.get_all_info()

if __name__ == '__main__':
    hue_requests.set_endpoint()
    get_all_info()        