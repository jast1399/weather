import click
import datetime
import matplotlib.dates as mdates
import numpy as np

from matplotlib.collections import LineCollection
from matplotlib.colors import Normalize
from matplotlib.figure import Figure

from weather.db import get_db


def get_forecast_data():
    db = get_db()
    forecast = db.execute(
        """SELECT time, temp FROM forecast"""
    ).fetchall()
    return zip(*forecast)

def get_history_data():
    db = get_db()
    history = db.execute(
        """SELECT time, temp FROM history"""
    ).fetchall()
    return zip(*history)

def get_diff():
    db = get_db()
    diff = db.execute(
        """SELECT f.time, f.temp - h.temp
           FROM forecast f INNER JOIN history h 
           ON f.time = h.time
           AND h.temp IS NOT NULL;"""
    )
    return zip(*diff)

def generate_plot():
    fig = Figure()
    axs = fig.subplots(nrows=2, sharex=True)
    
    generate_temperature_plot(axs[0])
    generate_difference_plot(axs[1])
    
    plot_url = 'weather/static/plot.png'
    fig.savefig(plot_url, format="png")

def generate_temperature_plot(ax):
    ftimes, ftemps = get_forecast_data()
    ftimes = [mdates.datestr2num(t) for t in ftimes]
    htimes, htemps = get_history_data()
    htimes = [mdates.datestr2num(t) for t in htimes]

    ax.plot(ftimes, ftemps, label='forecast')
    ax.plot(htimes, htemps, label='history')
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(ax.xaxis.get_major_locator()))
    ax.legend()
    ax.set_title('Temperature Data')
    ax.set_ylabel('Temperature')

def generate_difference_plot(ax):
    time, diff = get_diff()
    time = [mdates.datestr2num(t) for t in time]

    # Create a set of line segments so that we can color them individually
    # This creates the points as an N x 1 x 2 array so that we can stack points
    # together easily to get the segments. The segments array for line collection
    # needs to be (numlines) x (points per line) x 2 (for x and y)
    points = np.array([time, diff]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    # Create a continuous norm to map from data points to colors
    bound = max(max(diff), -min(diff))
    norm = Normalize(-bound, bound)
    lc = LineCollection(segments, cmap='coolwarm', norm=norm)
    # Set the values used for colormapping
    lc.set_array(diff)
    ax.set_ylim(-bound*1.1, bound*1.1)
    ax.add_collection(lc)
    ax.set_title('Forecast Error')
    ax.set_ylabel('Temperature Difference')
    ax.set_xlabel('Date')

    
@click.command('plot-data')
def plot_command():
    """Plot the stored data."""
    generate_plot()
    click.echo('Plot saved.')

def init_app(app):
    app.cli.add_command(plot_command)    
