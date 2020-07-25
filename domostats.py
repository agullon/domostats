import hue_requests, temperature

INDOOR = 'indoor'
OUTDOOR = 'outdoor'

spanish_name = {
    INDOOR: 'dentro',
    OUTDOOR: 'fuera'
}

sensor_id = {
    INDOOR: '14',
    OUTDOOR: '5'
}

def get_all_info():
    temperature.get_all_info()

if __name__ == '__main__':
    hue_requests.set_endpoint()
    get_all_info()        
