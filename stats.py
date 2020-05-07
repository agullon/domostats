import temperature, domostats
import database as db
import numpy as np
import matplotlib
matplotlib.use('Agg')
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

    x1, y1 = get_graph_cords(domostats.BEDROOM)
    graph_b = plt.plot(x1, y1, label=domostats.spanish_name[domostats.BEDROOM])
    x2, y2= get_graph_cords(domostats.KITCHEN)
    graph_k = plt.plot(x2, y2, label=domostats.spanish_name[domostats.KITCHEN])

    graphs = graph_k + graph_b
    labels = [g.get_label() for g in graphs]
    ax.legend(graphs, labels, loc=0)
    plt.legend(loc="upper left")

    plt.ylim(ymin=min(y1+y2)-2, ymax=max(y1+y2)+2)

    plt.gcf().autofmt_xdate()
    return plt

def get_plot_png():
    plt = plot_temperature()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return buf.getvalue()

if __name__ == '__main__':
    plt = plot_temperature('kitchen')
    plt.show()
