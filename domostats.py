import hue_requests, temperature

KITCHEN = 'kitchen'
HALL = 'hall'

spanish_name = {
    KITCHEN: 'cocina',
    HALL: 'entrada'
}

sensor_id = {
    KITCHEN: '14',
    HALL: '5'
}

def get_all_info():
    temperature.get_all_info()

if __name__ == '__main__':
    hue_requests.set_endpoint()
    get_all_info()        
