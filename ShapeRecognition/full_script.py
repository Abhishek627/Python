import cv2
import numpy as np
import math
import matplotlib
from matplotlib import pyplot as plt

# This Project Was Created By Ethan Bonnardeaux 
# It takes an Image with either a white or black background and indentifies the shapes inside 


# Function Definitions

#defining the masking function for photos with a white background
def WhiteBack(img):
    lower = np.array([235,235,235], dtype=np.uint8) # lower bound for colour white
    upper = np.array([255,255,255], dtype=np.uint8) #upper bound for white
    mask = cv2.inRange(img, lower, upper)
    return mask
		
#this function get the contours of the image using the cv2 package
def getContours(mask):
    (contours, hierarchy) = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE) 
		# no chain approximation method is used because all contour points are required for later functions
    return contours
#this function is not used but is created for masking images with black backgrounds
#def BlackBack(img2):
    #lower = np.array([0,0,0], dtype=np.uint8) #lower bound for black
    #upper = np.array([15,15,15], dtype=np.uint8) #upper bound for black
    #mask = cv2.inRange(img2, lower, upper)
    #return mask

#this function determines the number of shapes in the image
def numShapes(contours):
    num_shapes = len(contours)
    return num_shapes

'''this function is used in finding the minimum points of a polynomial graph. it returns an indicative 0 if the input y value is not proceeded by any lower values within the error range therefore the graph is increasing to the right of the point'''
def errorCheckIncreasing(y_vals,iteration, error):
    buffer = 0
    for i in range(error):
        if i == (len(y_vals)- error -1):
            break
        elif((y_vals[iteration + i + 1]) < (y_vals[iteration])):
            buffer = 1
            break
        else:
            continue
    return buffer

''' this function is also used in finding minimum points. It returns 0 if y input has no values before it that are lower then it making it the lowest value in the range. In conjunction with the previous function a 0 signifies a minimum point'''
def errorCheckDecreasing(y_vals, iteration, error):
    buffer = 0
    for i in range(error):
        if (iteration - i) == -1:
            break
        elif (y_vals[iteration - i  - 1]) < (y_vals[iteration]):
            buffer = 1
            break
        else:
            continue
    return buffer

#This finds an error in the Y-coordinate calculations done in the cv2.getcontours function
def Find_y_error(Image):
    height, width, disregard = Image.shape
    error = math.ceil(height/70)
    return error
		
'''this tests to see if the range of y-values are within the Y-Error meaning that the graph will be a straight line and when graphing radius over radians, a straight line indicates a shape of constant radius which is a circle'''
def circleTest(errorY, range):
    tf = False
    if range < errorY:
        tf = True
    else:
        pass
    return tf
		
'''this function finds the coordinates of the minimum points on each graph aswell as indicating if they are local mins or absolute Minimums. It returns a list of all minimum indexes, a list of absolute minimus indexes and an indication to whether the shape is a circle or not'''
def local_minimum(x_vals, y_vals):
    max_index, max_value = max(enumerate(y_vals), key=lambda pair: pair[1])
    min_index, min_value = min(enumerate(y_vals), key=lambda pair: pair[1])
    errorY = Find_y_error(Image) #this gives an accurate representation of the errors in pixel calcluations involving the contours
    errorX =  math.ceil(len(x_vals)*0.1/math.pi)         # this is a bound that the pixel errors could lie in
    mins = []
    absMins = []
    maxVal = round(max_value[0])
    minVal = round(min_value[0])
    circle_indicator = 0
    if circleTest(errorY, maxVal-minVal) == True:
        circle_indicator = 1
    else:
        for y in range(len(y_vals)-errorX):
            if errorCheckIncreasing(y_vals, y, errorX) + errorCheckDecreasing(y_vals, y, errorX) == 0:
                mins.append(y)
        deleted_items = 0
        for i in range(len(mins)-1-deleted_items):
            if math.isclose(mins[i], mins[i+1], abs_tol=errorX) == True:
                mins[i] = math.ceil((mins[i] + mins [i + 1])/2)
                del mins[i+1]
                deleted_items += 1
            else:
                continue
        for i in range(len(mins)):
            if  math.isclose(y_vals[mins[i]], minVal + errorY, abs_tol=errorY) == True or math.isclose(y_vals[mins[i]], minVal - errorY, abs_tol=errorY) == True:
                absMins.append(mins[i])
            else:
                continue
    return mins, absMins, circle_indicator

#this function classifies the graphs into what shapes they represent
def classification(mins, absMins, circle_indicator):
    local_mins = list(set(mins) - set(absMins))
    shape = 'Null'
    if len(mins) == 4 and len(local_mins) == 0:
        shape = 'Square'
    elif len(mins) == 4 and len(local_mins)== 2:
        shape = 'Rectangle'
    elif circle_indicator == 1:
        shape = 'Circle'
    elif  len(mins) == 3 and len(local_mins) == 0:
        shape = 'Equalateral Triangle'
    elif len(mins) == 3 and len(local_mins) == 2:
        shape = 'Triangle'
    elif len(mins) == 5 and len(local_mins) == 0:
        shape = 'Pentagon'
    elif len(mins) == 6 and len(local_mins) == 0:
        shape = 'Hexagon'
    elif len(mins) == 7 and len(local_mins) == 0:
        shape = 'Heptagon'
    elif len(mins) == 8 and len(local_mins) == 0:
        shape = 'Octagon'
    elif len(mins) == 9 and len(local_mins) == 0:
        shape = 'Nonagon'
    elif len(mins) == 10 and len(local_mins) == 0:
        shape = 'Decagon'
    return shape


# Main code begins here

Image = cv2.imread("basic_shapes.jpg")

masked_image = WhiteBack(Image)

contours = getContours(masked_image)
contrast = cv2.drawContours(Image, contours, -1, (255,0,0),1)


#sorting the cnt array
cnt = np.array(sorted(contours, key=cv2.contourArea))
number_of_shapes = numShapes(cnt)

#finding the length of the shape arrays
sizes = []
x_values = []
y_values = []

for j in range(number_of_shapes):
    sizes.append(len(cnt[j][0][0]))
    for e in range(len(cnt[j])):
        x_values.append(cnt[j][e][0][0])
        y_values.append(cnt[j][e][0][1])

#calculating the areas and storing in an array
areas = []
for i in range(number_of_shapes):
    areas.append(cv2.contourArea(cnt[i]))

#calculating the centroids of each shape using cv2 package 
centroid_x = []
centroid_y = []

for o in range(number_of_shapes):
    moment = cv2.moments(cnt[o])
    x =int(moment['m10']/moment['m00'])
    centroid_x.append(x)
    y = int(moment['m01']/moment['m00'])
    centroid_y.append(y)

#full number of points per shape
points = []
for f in range(number_of_shapes):
    points.append(len(cnt[f]))


#change the centroid array to be read with the x and y values
centr_x =[]
centr_y = []

for r in range(number_of_shapes):
    for k in range(points[r]):
        centr_x.append(centroid_x[r])
        centr_y.append(centroid_y[r])

#calculating distance to centroid at each point
radius = []
for l in range(len(x_values)):
        r = 0
        x_dist = np.square(x_values[l] - centr_x[l])
        y_dist = np.square(y_values[l] - centr_y[l])
        rad = np.sqrt(x_dist + y_dist)
        radius.append([rad])

#creating a list of lists containing the x-values for each graph 
x_graph = []
counter = 0
for h in range(number_of_shapes):
    x_graph.append(np.linspace(0,math.pi*2, points[h]))

#convert to a numpy array to GRAPH
radius = np.array(radius)
x_graph = np.array(x_graph)

#plotting and classifying the graphs
finish = 0
for i in range(len(points)):
    if i == 0:
        start = 0
    else:
        start += points[i-1]
    finish += points[i]
    plt.plot(x_graph[i], radius[start:finish], c='g')
    mins, absMins, circle_indicator = local_minimum(x_graph[i], radius[start:finish])
    print(classification(mins, absMins, circle_indicator))


cv2.waitKey(100)  # keeps the window open until esc pressed
cv2.destroyAllWindows()
