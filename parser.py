# imports
import sys

import pandas as pd
import numpy as np
import json
import re
import greatcircle
import matplotlib.pyplot as plt
import scipy.stats as stats
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
    events_df = pd.read_csv(events_file)[['visitors', 'exhibitors', 'lat', 'lng', 'start_date', 'end_date']]
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

    print(events_df)
    # events_df.to_csv('clean_events.csv')


clean_events()
# mean = 0
# standard_deviation = 2

# x_values = np.arange(-20, 20, 0.1)
# y_values = stats.norm(mean, standard_deviation)

# plt.plot(x_values, y_values.pdf(x_values))
# plt.show()











