import temperature, domostats
import database as db
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
import datetime
import io
from PIL import Image

def save_temp(room):
    temp, time = temperature.get_room_info(room)
    db.add_temperature(room, temp, time)

def plot_temp():
    y_cord = []
    x_cord = []

    table = db.read_temperature(24, 'kitchen')
    for row in table:
        y_cord.append(row[1])
        x_cord.append(row[2])

    y = y_cord
    x = [datetime.datetime.strptime(d,'%Y-%m-%dT%H:%M:%S') for d in x_cord]

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.gca().xaxis.set_major_locator(mdates.HourLocator())

    plt.plot(x,y)
    plt.gcf().autofmt_xdate()
    #plt.show()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return buf.getvalue()