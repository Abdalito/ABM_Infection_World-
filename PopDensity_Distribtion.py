# -*- coding: utf-8 -*-
"""
Created on Sat Feb 12 17:31:30 2022

@author: ABM
"""
import math
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import time


T_1 = time.time() # Measurement of time before allocation of tasks commence


lat_col = 'Lat' # Latitude Column
lon_col = 'Lon' # Longitude Column
pop_col = 'Population' # Population Column 

population = pd.read_csv('Italy.csv') # Creating a dataset to store data from the country csv
population.sort_values(by = [lat_col, lon_col]) # Sorting the columns in the dataset by latitude and then longitude 

# print(population) # Printing the dataset to check the data is coherent 

# Extract the data we're interested in: 
lat = population[lat_col].values # Extracting the latitude column 
lon = population[lon_col].values # Extracting the longitude column 
pop_count = population[pop_col].values # Extracting the population column 

pop_total = sum(pop_count) # Checking the population total 

print("Total Population: ",pop_total) # Printing the total population 

T_2 = time.time() # Taking the second time measurement 

T_delta = T_2-T_1 # Finding the time taken for the creation, sorting and summing operations 
print("__________________________________________________________")
print("Time taken for read, sort and sum operation: ",T_delta)
print("__________________________________________________________")

core_count = 1000000 # Hard-coded value of what the number of cores used would be 
n = int(pop_total/core_count) # Number of people per core 
core_number = int(pop_total/core_count)
print("Total Number of Cores: ", core_number)
a = round(math.sqrt(n))

#print(n)

while n%a > 0:
    a -= 1

#print(a)

lat_min = min(lat)
lat_max = max(lat)

lon_min = min(lon)
lon_max = max(lon)

lat_diff = lat_max - lat_min
lon_diff = lon_max - lon_min

if lat_diff > lon_diff:
    lat_n = int(n/a)
    lon_n = a
else:
    lon_n = int(n/a)
    lat_n = a
    
print("Number of Lat Divisions: ",lat_n)
print("Number of Lon Divisions: ",lon_n)

#fig, ax = plt.subplots()

x_lin_width = lon_diff/lon_n
y_lin_width = lat_diff/lat_n

alpha_lat = 1
delta_lat = alpha_lat*y_lin_width 
delta_lat_1 = (alpha_lat-1)*y_lin_width


alpha_lon = 1
delta_lon = alpha_lon*x_lin_width
delta_lon_1 = (alpha_lon-1)*x_lin_width


box_list = []

print("Latitude Grid Width: ",y_lin_width)
print("Longitude Grid Width: ",x_lin_width)

#plt.grid(axis = 'x', color = 'green', linestyle = '--' )
#plt.grid(axis = 'y', color = 'green', linestyle = '--' )

print("Latitude: Min - ",lat_min, "; Max - ", lat_max, "; Delta: ", delta_lat)

print("Longitude: Min - ",lon_min, "; Max - ", lon_max, "; Delta: ", delta_lon)

T_3 = time.time()

T_delta = T_3-T_2
print("__________________________________________________________")
print("Time taken for intital calculations: ",T_delta)
print("__________________________________________________________")
#plt.show()

box_count = 0
lat_list = []
lon_list = []



index_val = np.where(lat<=lat_max)    

for a in range(1,core_number+1):
    index_val_x = np.where(np.logical_and(lon>=(lon_min+delta_lon_1),lon<=(lon_min+delta_lon)))
    index_val_y = np.where(np.logical_and(lat>=(lat_min+delta_lat_1),lat<=(lat_min+delta_lat)))
    core_index = np.intersect1d(index_val_x,index_val_y)
    for b in core_index:
        box_count+=pop_count[b]
   # print(box_count)
    box_list.append(int(box_count))
    box_count = 0
    
    alpha_lon += 1
    delta_lon = alpha_lon*x_lin_width
    delta_lon_1 = (alpha_lon-1)*x_lin_width
    
    if a%lon_n == 0:
        alpha_lat += 1
        delta_lat = alpha_lat*y_lin_width 
        delta_lat_1 = (alpha_lat-1)*y_lin_width
        alpha_lon = 1
        delta_lon = alpha_lon*x_lin_width
        delta_lon_1 = (alpha_lon-1)*x_lin_width
        


print("Total Number of cores: " + str(len(box_list)))
print("Total Population: " + str(sum(box_list)))
print("Array of Population distribution:" + str(box_list))

#ax.scatter(lon, lat)

T_4 = time.time()

T_delta = T_4-T_3
print("__________________________________________________________")
print("Time taken for core distribution: ",T_delta)
print("__________________________________________________________")

print("Core with the maximum number of people: " + str(max(box_list)))

print(box_count)    


