# Floodfill
# writing code to find templates based on number of objects before and after removing a center pixel
# if equal then the pixel can be deleted and structuring element is a valid deletable template
# using python
# need python > 3 to compile
# uses scipy, numpy and itertools packages
# 2D sanity check 
# number of deleting templates is 32
# number of deleting templates from the algorithm 
# implemented so far is 124
# definitely not correct :( 
# did not work by using inbuilt instruction scipy.ndimage.measurements.label 
# number of objects in a 3 by 3 array of all 1s and 3 by 3 array of 1s with 
# zero in the center is same which means it suggests the a 3 by 3 array of all 1s
# as a deletable template which it is not
# flood filling in actuality must be implemented 
# count the number of times floodfill is called 
# count number of unfilled pixels
# 
