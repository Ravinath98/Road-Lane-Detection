#import the required libaries
import glob
import os
import re
import cv2
import numpy as np
import matplotlib.image as mpimg

#define the paths
input_images_folder_path="TestVideo_1/"
output_images_folder_path = "Output_Images_1/"

#Point class
class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y

#function to get the intersection of 2 lines
def lineLineIntersection(a, b, c, d):
	# here, line ab represented as a1x + b1y = c1
	a1 = b.y - a.y
	b1 = a.x - b.x
	c1 = a1 * (a.x) + b1 * (a.y)

	# here,line cd represented as a2x + b2y = c2
	a2 = d.y - c.y
	b2 = c.x - d.x
	c2 = a2 * (c.x) + b2 * (c.y)

	determinant = a1*b2 - a2*b1

	if (determinant == 0):
		return Point(10**9, 10**9)
	else:
		x = (b2*c1 - b1*c2)/determinant
		y = (a1*c2 - a2*c1)/determinant
		return Point(x, y)

#function to generate the video from image sequence
def GenerateVideo():
    def atoi(text):
        return int(text) if text.isdigit() else text

    def natural_keys(text):
        return [atoi(c) for c in re.split(r'(\d+)', text)]

    images = []
    filenames = []
    for filename in glob.glob('Output_Images_1/*.jpg'):
        filenames.append(filename)
        filenames.sort(key=natural_keys)

    for file in filenames:
        img = cv2.imread(file)
        height, width, layers = img.shape
        size = (width, height)
        images.append(img)

    out = cv2.VideoWriter('road_lane_out.avi', cv2.VideoWriter_fourcc(*'DIVX'), 15, size)

    for i in range(len(images)):
        out.write(images[i])
    out.release()

#function to make the coordinates
def make_coordinates(image, line_parameters):
    slope, intercept = line_parameters
    y1 = image.shape[0]
    y2 = int(y1 * (3 / 5))
    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)
    return np.array([x1, y1, x2, y2])

#function to calculate the average slope intercepts
def avgSlopeIntercept(image, lines):
    left_fit = []
    right_fit = []
    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)
        parameters = np.polyfit((x1, x2), (y1, y2), 1)
        slope = parameters[0]
        intercept = parameters[1]
        if slope < 0:
            left_fit.append((slope, intercept))
        else:
            right_fit.append((slope, intercept))
    left_fit_average = np.average(left_fit, axis=0) #get the average of negative slopes
    right_fit_average = np.average(right_fit, axis=0) #get the average of positive slopes
    left_line = make_coordinates(image, left_fit_average) #get the left line
    right_line = make_coordinates(image, right_fit_average) #get the right line
    return np.array([left_line, right_line]) #return the left and right lines

#function to display the lines in the original image
def displayLines(image, lines):
    line_image = np.zeros_like(image)
    if lines is not None:
        #get the 4 points to create the 2 lane lines....
        a = Point(lines[0][0], lines[0][1])
        b = Point(lines[0][2], lines[0][3])
        c = Point(lines[1][0], lines[1][1])
        d = Point(lines[1][2], lines[1][3])
        intersection = lineLineIntersection(a, b, c, d)
        x_end=int(intersection.x)
        y_end=int(intersection.y)

        for x1, y1, x2, y2 in lines:
            cv2.line(line_image, (x1, y1), (x_end,y_end), (0, 0, 255), 15) #draw each line
        center_coordinates=(x_end,y_end)
        cv2.circle(line_image, center_coordinates, 20, (0, 255, 0), 2) #draw the circle
    return line_image

#loop over the images
for image_path in os.listdir(input_images_folder_path):
    input_path = os.path.join(input_images_folder_path, image_path) #get the each image
    # print(input_path)
    image = cv2.imread(input_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    [rows, columns] = gray_image.shape
    blur = cv2.GaussianBlur(gray_image, (5, 5), 0)
    canny_filtered_image = cv2.Canny(blur, 100, 200)

    for i in range(rows):
        for j in range(columns):
            if canny_filtered_image[i][j] > 100:
                canny_filtered_image[i][j] = 255
            else:
                canny_filtered_image[i][j] = 0

    lane_detect = np.zeros(shape=(rows, columns))

    for i in range(300):
        for j in range(350):
            if canny_filtered_image[595 - i][350 + j] == 255:
                lane_detect[595 - i][350 + j] = 255
                break

    for i in range(300):
        for j in range(350):
            if canny_filtered_image[595 - i][350 - j] == 255:
                lane_detect[595 - i][350 - j] = 255
                break

    lane_detect_image = lane_detect.astype(np.uint8)
    # lines = cv2.HoughLinesP(lane_detect_image, 2, np.pi / 180, 40, np.array([]), minLineLength=30, maxLineGap=10)
    lines = cv2.HoughLinesP(lane_detect_image, 2, np.pi / 180, 30, np.array([]), minLineLength=20, maxLineGap=80)
    averaged_lines = avgSlopeIntercept(image, lines)
    line_image = displayLines(image, averaged_lines)
    combo_image = cv2.addWeighted(image, 0.8, line_image, 1, 1)
    mpimg.imsave(output_images_folder_path + '/' + input_path[12:-4] + '_lane_line_detected.jpg', combo_image)

#call the video generate function
GenerateVideo()





