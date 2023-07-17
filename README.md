# NPLD-trough-profiles
These two python codes are used to create NPLD trough profile figures and calculate the trough profile metrics for "Investigating the Linkage Between Spiral Trough Morphology and Cloud Coverage on the Martian North Polar Layered Deposits". This was done for all the ~3000 trough profiles created perpendiculatar to the thalwag of NPLD troughs mapped in ArcPro. The raw data for each profile are contained in the compressed data folder, separated based on if the profile is predominantly east or west of the pole in order to properly note which side of the profile is pole-facing vs equator-facing.

## Plotting Profiles
The script Poly_Profiles.py was used to plot figures of indivudal trough profiles. One profile is read and has a polynomial fit to it. The minimum points are identified by calculating the first derivative of the curve. The most accurate minimum point is then visually identified and entered this into the code where it states (x_poly[b][1]) immediately following the minimum calculation, replacing the 1 with the number of whichever minimum point is the profile's actual minimum, where the first minimum point identified is 0. 

Then the second derivative of the polynomial is calculated to find the shoulder points of the trough profile, which are also visually identified based on which values best fit the original polynomial. These vaules are also input into the code where it states (x_poly[b][1]), immediately following the second derivative calculation. Multiple ways of ploting the polyonimal follow, focusing on reducing vertical exageration to various amounts in different ways.

## Automating Trough Metric Calculation
The script Poly_Profiles_Auto.py was used to automate the calculation of trough metrics for the ~3000 trough profiles. 

NOTE: Before running this code, update the x_min, x_left, and x_right values to match those of the first profile to be read. To do this, run the Poly_Profile.py script for the first profile and record these values.

This code reads in a large batch of profile data, fits a polynomial to the first profile it finds, uses the input minimum trough point and shoulder points (identified using Poly_Profiles), then calculates the trough metrics defined in the paper. The next trough profile is then loaded and its minimum point and shoulder points are found by finding the calculated value closest to the previous x_min, x_left, and x_right values. Break points exist in the code to stop the loop if the values of the two troughs are too different, as this indicates that the code will most likely identify an incorrect minimum point and/or shoulder point. 
