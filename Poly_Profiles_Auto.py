#!/usr/bin/env python
# coding: utf-8


# LOAD BASIC MODULES
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
from math import hypot


#Slope calc
def slope(x1, y1, x2, y2):
    m = (y2-y1)/(x2-x1)
    return m

#find nearest value calc
def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]



#Profile data path and other required set-up information
path_dir = '2023_Profiles/West_Profiles/Text_Files/'

ext = ('.txt')
ymin_list = []
leftslope_list = []
rightslope_list = []
leftrelief_list = []
rightrelief_list = []
width_list = []
depth_list = []
reliefdiff_list = []

#NOTE: UPDATE BEFORE RUNNING LOOP EVERYTIME!!!!!!
x_min = 16108.89901
x_left = 9350.570569
x_right = 28458.47502


for files in sorted(os.listdir(path_dir)):
    if files.endswith(ext):
        #read data and create polynomial fit
        data = pd.read_csv('2023_Profiles/West_Profiles/Text_Files/' + str(files), sep='\s+',header=None, skiprows = 1)
        data = pd.DataFrame(data)
        x = data[0]
        y = data[1]
        x_poly = np.unique(x)
        y_poly = np.poly1d(np.polyfit(x, y, 15))(np.unique(x))

        # detection of local min of y' polyfit
        b_min = (np.diff(np.sign(np.diff(y_poly))) > 0).nonzero()[0] + 1
        x_min2 = find_nearest(x_poly[b_min], x_min)

        #break point to catch incorrect local min detection, change value as needed
        #if x_min2-x_min > 5000: #2000:
        #    break

        x_min = x_min2
        y_min = np.interp(x_min,x_poly,y_poly)
        #wait to append minimum point data until all break tests complete

        # Computing 1st derivative of your curve with a step of 0.01 and plotting it
        y_1prime = np.gradient(y_poly, 0.01)
        # Computing 2nd derivative of your curve with a step of 0.01 and plotting it
        y_2prime = np.gradient(y_1prime, 0.01)
        # detection of local min of y" polyfit
        b_min2 = (np.diff(np.sign(np.diff(y_2prime))) > 0).nonzero()[0] + 1

        #find boundary points, based on where they should be from graph
        ####find closest x_poly[b_min2] value to previous x_left and x_right
        x_left2 = find_nearest(x_poly[b_min2], x_left)

        #break point to catch incorrect shoulder point detection, change value as needed
        #if x_left2-x_left > 5000: #1500:
        #    break

        x_left = x_left2
        ##########

        x_right2 = find_nearest(x_poly[b_min2], x_right)

        #break point to catch incorrect shoulder point detection, change value as needed
        #if x_right2-x_right > 5000: #1000:
        #    break

        x_right = x_right2

        if x_left > x_right:
            break

        if x_left > x_min:
            break

        #Save y-min information
        ymin_list.append(y_min) #Min trough value, y-axis

        #find closest x_poly[b_min2] value to previous x_left and x_right

        y_left = np.interp(x_left,x_poly,y_poly)
        y_right = np.interp(x_right,x_poly,y_poly)

        #slope calc
        left_slope = slope(x_left, y_left, x_min, y_min)
        right_slope = slope(x_min, y_min, x_right, y_right)
        leftslope_list.append(left_slope)
        rightslope_list.append(right_slope)

        #relief calc
        left_relief = y_left-y_min
        right_relief = y_right-y_min
        leftrelief_list.append(left_relief)
        rightrelief_list.append(right_relief)

        #width calc -> distance hump to hump
        base_1 = hypot(x_left - x_left, y_left - y_min)
        base_2 = hypot(x_right - x_right, y_right - y_min)
        width = base_1 + base_2
        width_list.append(width)

        #dept calc -> avg reflief value
        avg_relief = (right_relief+left_relief)/2
        depth_list.append(avg_relief)

        #relief difference calc
        relief_diff = abs(right_relief-left_relief)
        reliefdiff_list.append(relief_diff)

        #create trough profile plot image and save
        plt.plot(x, y, marker='.', label='trough profile')
        plt.plot(x_poly, y_poly, label='polyfit')
        plt.plot(x_min, y_min, "o", label='min')
        plt.plot(x_left, y_left, "o", label='left')
        plt.plot(x_right, y_right, "o", label='right')
        plt.legend()
        plt.xlabel('Extent (m)')
        plt.ylabel('Elevation (m)')
        plt.title('Trough Profile: ' + str(files))
        plt.savefig('2023_Profiles/West_Profiles/Png_Files/' + str(files) + '.png')
        plt.close()

    else:
        continue


#combine individual lists into one list
profile_data = list(zip(leftslope_list, rightslope_list, leftrelief_list, rightrelief_list, reliefdiff_list, width_list, depth_list))

#save list as .csv file
dataframe = pd.DataFrame(profile_data)
dataframe.columns = ['Left Slope', 'Right Slope', 'Left Relief', 'Right Relief', 'Relief Diff', 'Width', 'Depth']
dataframe.to_csv('2023Analysis_West1.csv')
