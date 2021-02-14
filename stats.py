import temperature, domostats
import database as db
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
from scipy.ndimage.filters import gaussian_filter1d
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

    x1, y1 = get_graph_cords(domostats.OUTDOOR)
    y1_smoth = gaussian_filter1d(y1, sigma=2)
    graph_1 = plt.plot(x1, y1_smoth, label='outdoor')

    x2, y2= get_graph_cords(domostats.KITCHEN)
    y2_smoth = gaussian_filter1d(y2, sigma=2)
    #graph_2 = plt.plot(x2, y2_smoth, label=domostats.KITCHEN)

    x3, y3= get_graph_cords(domostats.HALL)
    y3_smoth = gaussian_filter1d(y3, sigma=2)
    #graph_3 = plt.plot(x3, y3_smoth, label=domostats.HALL)

    x4, y4= get_graph_cords(domostats.MAIN_ROOM)
    y4_smoth = gaussian_filter1d(y4, sigma=2)
    #graph_4 = plt.plot(x4, y4_smoth, label=domostats.MAIN_ROOM)

    x5 = x1
    y5_smoth = (y2_smoth + y3_smoth + y4_smoth)/3
    graph_5 = plt.plot(x5, y5_smoth, label='indoor avg')

    graphs = graph_1 + graph_5
    labels = [g.get_label() for g in graphs]
    ax.legend(graphs, labels, loc=0)
    plt.legend(loc='lower center', bbox_to_anchor=(0,1,1,0), ncol=2)

    y_all = y1+y2+y3+y4
    plt.ylim(bottom = min(y_all)-2)
    plt.ylim(top = max(y_all)+2)

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
