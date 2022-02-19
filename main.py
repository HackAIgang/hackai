import numpy as np 
import matplotlib.pyplot as plt

flight_volumes = [900, 200, 340, 504, 700, 230, 100]

visitors = 3000
exhibitors = 500

p = 3 * exhibitors + visitors

mu = -2
sigma = 2

total_volume = 0

for i in flight_volumes:
    total_volume += i

v = total_volume / 7


def gaussian_function(x, mu, sigma):
    return 1/(sigma * np.sqrt(2 * np.pi)) * np.exp( - (x - mu)**2 / (2 * sigma**2) )

def normalise(arr):
    max = np.amax(arr)
    norm_array = []
    for i in arr:
        norm_array.append(i/max)
    return norm_array

normal_flight_volumes = normalise(flight_volumes)

print(normal_flight_volumes)

discrete_values_gd = []
for x in range(-5, 2):
    discrete_values_gd.append(gaussian_function(x, mu, sigma))

print(discrete_values_gd)

squared_deviations = []
for i in range(0, 7):
    squared_deviations.append((normal_flight_volumes[i]-discrete_values_gd[i]) ** 2)

sum = 0
for i in range(0, 7):
    sum += squared_deviations[i]

r = 7 / sum
print(r)


anomality_factor = r * p * v

print(anomality_factor)