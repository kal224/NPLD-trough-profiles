#!/usr/bin/env python
# coding: utf-8


# LOAD BASIC MODULES
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


#read in one profile
data = pd.read_csv('2023_Profiles/East_Profiles/Read_Txt_Files/Profile_0020.txt',sep='\s+',header=None, skiprows=1)
data = pd.DataFrame(data)
x = data[0]
y = data[1]

#fit a polynomial to the data
x_poly = np.unique(x)
y_poly = np.poly1d(np.polyfit(x, y, 15))(np.unique(x))

plt.plot(x, y, marker='.', label='signal')
plt.plot(x_poly, y_poly, label='polyfit')
plt.legend()
plt.savefig('2023_Profiles/East_Profiles/Images/Profile_0020.png')
plt.close()



# detection of local minimums and maximums of polyfit

a = np.diff(np.sign(np.diff(y_poly))).nonzero()[0] + 1               # local min & max
b = (np.diff(np.sign(np.diff(y_poly))) > 0).nonzero()[0] + 1         # local min

# plot
plt.figure(figsize=(12, 5))
plt.plot(x_poly, y_poly, color='grey')
plt.plot(x_poly[b], y_poly[b], "o", label="min", color='r')
plt.legend()
plt.savefig('2023_Profiles/East_Profiles/Images/Profile_0020_min.png')
plt.close()

#stop code in order to identify x_min
#exit()

#find which min value in the list corresponds to the minimum point visually in the last graph
x_min = x_poly[b][1]
y_min = np.interp(x_min,x_poly,y_poly)



# Computing y 1st derivative of polyfit with a step of 0.01
y_1prime = np.gradient(y_poly, 0.01)
#plt.plot(x_poly, y_1prime, label="y'(x)")

# Computing y 2nd derivative of polyfit with a step of 0.01
y_2prime = np.gradient(y_1prime, 0.01)

# detection of local minimums and maximums of y" polyfit to find shoulder points

a = np.diff(np.sign(np.diff(y_2prime))).nonzero()[0] + 1               # local min & max
b = (np.diff(np.sign(np.diff(y_2prime))) > 0).nonzero()[0] + 1         # local min
c = (np.diff(np.sign(np.diff(y_2prime))) < 0).nonzero()[0] + 1         # local max
# +1 due to the fact that diff reduces the original index number

# plot
plt.figure(figsize=(12, 5))
plt.plot(x_poly, y_2prime, color='grey')
plt.plot(x_poly[b], y_2prime[b], "o", label="min", color='r')
plt.plot(x_poly[c], y_2prime[c], "o", label="max", color='b')
plt.legend()
plt.savefig('2023_Profiles/East_Profiles/Images/Profile_0020_y2.png')
plt.close()

#stop code in order to identify x_left and x_right
#exit()


#find shoulder points, based on where they should be from origianl graph
x_left = x_poly[b][1]
x_right = x_poly[b][4]

y_left = np.interp(x_left,x_poly,y_poly)
y_right = np.interp(x_right,x_poly,y_poly)


#plot points and profile data (check if min/left/right match)
plt.plot(x, y, label='trough profile')
plt.plot(x_poly, y_poly, label='polynomial fit')
plt.plot(x_min, y_min, "o", label='min')
plt.plot(x_left, y_left, "o", label='left')
plt.plot(x_right, y_right, "o", label='right')
#plt.legend()
plt.title('R7a Trough Profile')
plt.xlabel('Distance Across Trough (m)')
plt.ylabel('Elevation (m)')
plt.savefig('2023_Profiles/East_Profiles/Images/Profile_0020_allpoints.png')
plt.close()


#plot points and profile data with reduced vertical exageration
plt.plot(x, y, label='trough profile')
plt.plot(x_poly, y_poly, label='polynomial fit')
plt.plot(x_min, y_min, "o", label='min')
plt.plot(x_left, y_left, "o", label='left')
plt.plot(x_right, y_right, "o", label='right')
plt.legend()
plt.title('R7a Trough Profile - Reduced Vertical Exaggeration')
plt.xlabel('Distance Across Trough (m)')
plt.ylabel('Elevation (m)')
plt.ylim(-4000, -2000)
plt.savefig('2023_Profiles/East_Profiles/Images/Profile_0020_allpoints_vert1.png')
plt.close()


#condensed plot with reduced vertical exageration, used for figure creation (note both figures are the same, simply cropped as needed)
import matplotlib.gridspec as gridspec

gs = gridspec.GridSpec(2,1)
fig = plt.figure()

#first plot
ax = fig.add_subplot(gs[0])
plt.plot(x, y, label='trough profile')
plt.plot(x_poly, y_poly, label='polynomial fit')
plt.plot(x_min, y_min, "o", label='min')
plt.plot(x_left, y_left, "o", label='left')
plt.plot(x_right, y_right, "o", label='right')
ax.set_ylabel(r'Elevation(m)', size =10)
plt.tick_params(
    axis='x',          # changes apply to the x-axis
    labelbottom='off') # labels along the x-axis are off

#second plot
ax = fig.add_subplot(gs[1])
plt.plot(x, y, label='trough profile')
plt.plot(x_poly, y_poly, label='polynomial fit')
plt.plot(x_min, y_min, "o", label='min')
plt.plot(x_left, y_left, "o", label='left')
plt.plot(x_right, y_right, "o", label='right')
ax.set_ylabel(r'Elevation (m)', size =10)
ax.set_xlabel(r'Distance Across Trough (m)')

plt.savefig('2023_Profiles/East_Profiles/Images/Profile_0020_allpoints_vert2.png')
plt.close()
