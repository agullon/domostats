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

def get_graph_cords(room):
    y_cord = []
    x_cord = []

    table = db.read_temperature(24, room)
    for row in table:
        y_cord.append(row[1])
        x_cord.append(row[2])

    y = y_cord
    x = [datetime.datetime.strptime(d,'%Y-%m-%dT%H:%M:%S') for d in x_cord]
    return x, y

def plot_temperature():
    fig = plt.figure()
    ax = fig.add_subplot(111)

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.gca().xaxis.set_major_locator(mdates.HourLocator())

    x, y = get_graph_cords('kitchen')
    graph_k = plt.plot(x, y, label=domostats.spanish_name['kitchen'])
    x, y = get_graph_cords('bedroom')
    graph_b = plt.plot(x, y, label=domostats.spanish_name['bedroom'])

    graphs = graph_k + graph_b
    labels = [g.get_label() for g in graphs]
    ax.legend(graphs, labels, loc=0)
    plt.legend(loc="upper left")

    plt.ylim(ymin=min(y)-2, ymax=max(y)+2)

    plt.gcf().autofmt_xdate()
    return plt

def get_plot_png():
    matplotlib.use('Agg')
    plt = plot_temperature()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return buf.getvalue()

if __name__ == '__main__':
    plt = plot_temperature('kitchen')
    plt.show()
