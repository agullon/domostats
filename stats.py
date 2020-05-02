import temperature, domostats
import database as db
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
import datetime
import io
from PIL import Image

def save_temperature(room):
    temp, time = temperature.get_room_info(room)
    db.add_temperature(room, temp, time)

def plot_temperature():
    y_cord = []
    x_cord = []

    table = db.read_temperature(24, 'kitchen')
    for row in table:
        y_cord.append(row[1])
        x_cord.append(row[2])

    y = y_cord
    x = [datetime.datetime.strptime(d,'%Y-%m-%dT%H:%M:%S') for d in x_cord]

    matplotlib.use('Agg')

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.gca().xaxis.set_major_locator(mdates.HourLocator())

    plt.ylim(ymin=min(y)-2, ymax=max(y)+2)

    plt.plot(x,y)
    plt.gcf().autofmt_xdate()
    return plt

def get_plot_png():
    plt = plot_temperature()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return buf.getvalue()

if __name__ == '__main__':
    plt = plot_temperature()
    plt.show()