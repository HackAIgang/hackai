# imports
import sys

import pandas as pd
import numpy as np
import json
import re
import greatcircle
import time
import datetime
import matplotlib.pyplot as plt
import scipy.stats as stats
import matplotlib.dates
from datetime import datetime
import tensorflow as tf
from tensorflow.python.keras import layers

# modules setup
pd.set_option('display.max_columns', None)
np.set_printoptions(precision=3, suppress=True)
gc = greatcircle.GreatCircle()

# Constants, setup values
flights_file = 'data/flights_searches.csv'
events_file = 'data/events.csv'
airports_file = 'data/airports.json'


def to_unix_time(string_time):
    return time.mktime(datetime.strptime(string_time, "%Y-%m-%d").timetuple())


def get_closest_airport(lat, lng):
    with open(airports_file, 'r') as file:
        airports_obj = json.load(file)

    closest_iata = ''
    closest_distance = sys.maxsize
    for airport in airports_obj:

        coordinates = airport['geolocation']['coordinates']

        gc.latitude1_degrees = lat
        gc.longitude1_degrees = lng
        gc.latitude2_degrees = coordinates[1]
        gc.longitude2_degrees = coordinates[0]

        gc.calculate()
        distance = gc.distance_kilometres

        if distance < closest_distance:
            closest_distance = distance
            closest_iata = airport['iata']

    return {
        'iata': closest_iata,
        'distance': closest_distance
    }


def clean_events():
    events_df = pd.read_csv(events_file)[['visitors', 'exhibitors', 'lat', 'lng', 'name']]
    for i, row in events_df.iterrows():

        closest_airport = get_closest_airport(row['lat'], row['lng'])
        events_df.at[i, 'iata'] = closest_airport['iata']
        events_df.at[i, 'distance'] = closest_airport['distance']

        # columns to normalize
        average_columns = ['visitors', 'exhibitors']
        for column in average_columns:

            no_commas = str(row[column]).replace(',', '')
            split = re.split('\D+', no_commas)

            try:
                num_range = list(map(float, split))
                events_df.at[i, column] = np.mean(num_range)
            except:
                events_df.at[i, column] = 0

    # print(events_df.head())
    # events_df.to_csv('clean_events.csv')
    return events_df


# mean = 0
# standard_deviation = 2
#
# x_values = np.arange(-20, 20, 0.1)
# y_values = stats.norm(mean, standard_deviation)
#
# plt.plot(x_values, y_values.pdf(x_values))
# plt.show()

arrivals_returns_df = pd.read_csv(flights_file)
flights_obj = []

for i, arrival_return in arrivals_returns_df.iterrows():
    arrival_set = False
    return_set = False

    arrival_obj = {
        'origin': arrival_return['origin'],
        'destination': arrival_return['destination'],
        'unix_time': to_unix_time(arrival_return['arrival_date'])
    }

    return_obj = {
        'origin': arrival_return['destination'],
        'destination': arrival_return['origin'],
        'unix_time': to_unix_time(arrival_return['return_date'])
    }

    for j, flight in flights_obj:
        unix_time = flight['unix_time']

        if not arrival_set and arrival_obj['unix_time'] > unix_time:
            flights_obj.insert(i + 1, arrival_obj)
            arrival_set = True

        if not return_set and return_obj['unix_time'] > unix_time:
            flights_obj.insert(i + 1, arrival_obj)
            return_set = True

        if arrival_set and return_set:
            break


flights_df = pd.DataFrame(flights_obj)
print(flights_df)


# flights_df.plot(x='index', y='Stock_Index_Price', kind='scatter')
# plt.show()











