# Python code for Multiple Color Detection 

import numpy as np 
import cv2 
import time
import random
import keyboard

# Capturing video through webcam 

print("Welcome to the Kitchen! You have not moved to a station yet.")

recipes = ['RGB','RBG', 'GRB', 'GBR', 'BRG', 'BGR']
# recipes ['abc', 'bca']

while(1):
	current_dish = random.choice(recipes)
	print("Recipe to Make: " + current_dish)


	if (keyboard.read_key() == "m"):
		posRed = 0
		posBlue = 0
		posGreen = 0
		posFound = 0

		alreadyPrintedBlue = 0
		alreadyPrintedRed = 0
		alreadyPrintedGreen = 0

		listString = []
		finalString = ""
		webcam = cv2.VideoCapture(0) 
		

		# Start a while loop 
		while(1): 
			# Reading the video from the 
			# webcam in image frames 
			start_time = time.time()

			_, imageFrame = webcam.read() 

			# Convert the imageFrame in 
			# BGR(RGB color space) to 
			# HSV(hue-saturation-value) 
			# color space 
			hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV) 

			# Set range for red color and 
			# define mask 
			red_lower = np.array([136, 87, 111], np.uint8) 
			red_upper = np.array([180, 255, 255], np.uint8) 
			red_mask = cv2.inRange(hsvFrame, red_lower, red_upper) 

			# Set range for green color and 
			# define mask 
			green_lower = np.array([25, 52, 72], np.uint8) 
			green_upper = np.array([102, 255, 255], np.uint8) 
			green_mask = cv2.inRange(hsvFrame, green_lower, green_upper) 

			# Set range for blue color and 
			# define mask 
			blue_lower = np.array([94, 80, 2], np.uint8) 
			blue_upper = np.array([120, 255, 255], np.uint8) 
			blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper) 
			
			# Morphological Transform, Dilation 
			# for each color and bitwise_and operator 
			# between imageFrame and mask determines 
			# to detect only that particular color 
			kernal = np.ones((5, 5), "uint8") 
			
			# For red color 
			red_mask = cv2.dilate(red_mask, kernal) 
			res_red = cv2.bitwise_and(imageFrame, imageFrame, 
									mask = red_mask) 
			
			# For green color 
			green_mask = cv2.dilate(green_mask, kernal) 
			res_green = cv2.bitwise_and(imageFrame, imageFrame, 
										mask = green_mask) 
			
			# For blue color 
			blue_mask = cv2.dilate(blue_mask, kernal) 
			res_blue = cv2.bitwise_and(imageFrame, imageFrame, 
									mask = blue_mask) 

			# Creating contour to track red color 
			contours, hierarchy = cv2.findContours(red_mask, 
												cv2.RETR_TREE, 
												cv2.CHAIN_APPROX_SIMPLE) 
			
			for pic, contour in enumerate(contours): 
				area = cv2.contourArea(contour) 
				if(area > 300 and posFound == 0): 
					x, y, w, h = cv2.boundingRect(contour) 
					imageFrame = cv2.rectangle(imageFrame, (x, y), 
											(x + w, y + h), 
											(0, 0, 255), 2)
					posRed = 1
					posBlue = 0
					posGreen = 0
					posFound = 1
					alreadyPrintedBlue = 0
					alreadyPrintedGreen = 0
					


			# Creating contour to track green color 
			contours, hierarchy = cv2.findContours(green_mask, 
												cv2.RETR_TREE, 
												cv2.CHAIN_APPROX_SIMPLE) 
			
			for pic, contour in enumerate(contours): 
				area = cv2.contourArea(contour) 
				if(area > 300  and posFound == 0): 
					x, y, w, h = cv2.boundingRect(contour) 
					imageFrame = cv2.rectangle(imageFrame, (x, y), 
											(x + w, y + h), 
											(0, 255, 0), 2) 
					posGreen = 1
					posBlue = 0
					posRed = 0
					posFound = 1
					alreadyPrintedRed = 0
					alreadyPrintedBlue = 0


			# Creating contour to track blue color 
			contours, hierarchy = cv2.findContours(blue_mask, 
												cv2.RETR_TREE, 
												cv2.CHAIN_APPROX_SIMPLE) 
			for pic, contour in enumerate(contours): 
				area = cv2.contourArea(contour) 
				if(area > 300 and posFound == 0): 
					x, y, w, h = cv2.boundingRect(contour) 
					imageFrame = cv2.rectangle(imageFrame, (x, y), 
											(x + w, y + h), 
											(255, 0, 0), 2) 
					posBlue = 1
					posGreen = 0
					posRed = 0
					posFound = 1
					alreadyPrintedRed = 0
					alreadyPrintedGreen = 0
					

			if(posFound == 1):
				posFound = 0
				if (posBlue == 1 and alreadyPrintedBlue == 0):
					print("You moved to Blue")
					alreadyPrintedBlue = 1
					listString.append("B")
				elif (posRed == 1 and alreadyPrintedRed == 0):
					print("You moved to Red")
					alreadyPrintedRed = 1
					listString.append("R")
				elif (posGreen == 1 and alreadyPrintedGreen == 0):
					print("You moved to Green")
					alreadyPrintedGreen = 1
					listString.append("G")
				

			if (len(listString) == 3):
				finalString = "".join(listString)


			if (finalString == current_dish) and len(listString) == 3:
				print("\n")
				print("Good Job!\n")
				print("You created: " + finalString  + " when instructed to create: " + current_dish + "\n")
				cv2.destroyAllWindows()
				break
			elif (finalString != current_dish and len(listString) == 3):
				print("\n")
				print("You suck!\n")
				print("You created: " + finalString  + " when instructed to create: " + current_dish + "\n")
				cv2.destroyAllWindows()
				break
			
			# Program Termination 
			cv2.imshow("Multiple Color Detection in Real-TIme", imageFrame) 
			if cv2.waitKey(10) & 0xFF == ord('q'): 
				cv2.destroyAllWindows() 
				quit()

		