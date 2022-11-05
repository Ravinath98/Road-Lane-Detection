# Road-Lane-Detection

Input to the program

Collection of images inside a folder taken as input

Output from the program

Each image in the folder input to the program and then the program detect the road lanes of the input image.Then it will mark the 2 lane lines with vanishing point(with a circle at vanishing point)

Implementation Process with functions explanation
I have followed the steps as below to implement the program as below
1.	Convert the image to a grayscale image

Code segment used:
		gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

2.	Apply Canny edge detection algorithm

Code segment used:

canny_filtered_image = cv2.Canny(blur, 100, 200)

Here, before apply the canny edge detection algorithm, I have used a GaussianBlur to reduce the noise  and smooth of the image.After apply the canny edge detection of the image, I have created a same size image copy to draw the road lane lines as in the below step(define some threshold pixel value and assign the edge detected image pixel values as 0 and 255)

Code segment used:


    for i in range(rows):
        for j in range(columns):
            if canny_filtered_image[i][j] > 20:
                canny_filtered_image[i][j] = 255
            else:
                canny_filtered_image[i][j] = 0




3.	From the vehicle’s current center (x position), search the first edge pixel in each left and right direction (for all scanlines)

Here, I have consider a selected region of each image to find the road lane nearest pixels.The nearest pixel found by start some middle point of the road and travel in both sides(right & left until find a white pixel(255) in the image numpy array

Code segment used:

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

4.	Using the edge pixels, apply the Hough transform to determine the two line models
I have used an already available hough transform method to implement this
Code segment used:

lines = cv2.HoughLinesP(lane_detect_image, 2, np.pi / 180, 30, np.array([]), minLineLength=20, maxLineGap=80)

5.	Draw two lines over the original road image. At the intersection of the lines, draw a circle which represents the vanishing point. Draw the two lines from the image border to the vanishing point

I got the intersection of the 2 road lines using Point class and lineLineIntersection function.Then I have used the displayLines function to draw the lines in the original image(also the vanishing point circle draw using this function)


	Special things to consider
•	GenerateVideo function used to generated the video from the output images
•	avgSlopeIntercept function used to average the filtered lines 
•	make_coordinates function used to generate the line coodinates(x,y values) using line parameters
