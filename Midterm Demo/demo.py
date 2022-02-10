import numpy as np 
import cv2 
import random
import keyboard

print("Welcome to the Kitchen! You have not moved to a station yet.")
print("Customer 1 wants Pork Chops.")

#RED: Ingredient Storage
#BLUE: Chopping Station
#GREEN: Cooking Station

class PorkChops:
	pickedUp = False
	chopped = False
	cooked = False


porkchops = PorkChops()

while(1):
	posRed = 0
	posBlue = 0
	posGreen = 0
	posFound = 0

	alreadyPrintedBlue = 0
	alreadyPrintedRed = 0
	alreadyPrintedGreen = 0

	webcam = cv2.VideoCapture(0) 
	
	if (porkchops.pickedUp == True and porkchops.chopped == True and porkchops.cooked == True):
		print("You have sucessfully cooked Pork Chops!")
		break

	# Start a while loop 
	while(1): 
		# Reading the video from the 
		# webcam in image frames 

		_, imageFrame = webcam.read() 

		# Convert the imageFrame in 
		# BGR(RGB color space) to 
		# HSV(hue-saturation-value) 
		# color space 
		hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV) 

		# Set range for red color and 
		# define mask 
		red_lower = np.array([160, 130, 58], np.uint8) 
		red_upper = np.array([179, 255, 255], np.uint8) 
		red_mask = cv2.inRange(hsvFrame, red_lower, red_upper) 

		# Set range for green color and 
		# define mask 
		green_lower = np.array([25, 52, 72], np.uint8) 
		green_upper = np.array([102, 255, 255], np.uint8) 
		green_mask = cv2.inRange(hsvFrame, green_lower, green_upper) 

		# Set range for blue color and 
		# define mask 
		blue_lower = np.array([99, 162, 124], np.uint8) 
		blue_upper = np.array([179, 255, 255], np.uint8) 
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

				# Speech Implementation Here


				


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

				# Speech Implementation Here


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
				
				# Speech Implementation Here
				

		if(posFound == 1):
			posFound = 0
			if (posBlue == 1 and alreadyPrintedBlue == 0):
				if (porkchops.pickedUp == False):
					print("You have moved to the chopping station holding nothing")
				elif (porkchops.pickedUp == True):
					print("You have moved to the chopping station with uncooked pork")
					print("Press A to pretend you started chopping gesture")
					while(1):
						if (keyboard.read_key() == "A" or keyboard.read_key() == "a"):
							print("Pork chopped up!")
							porkchops.chopped = True
							break
			elif (posRed == 1 and alreadyPrintedRed == 0):
				if (porkchops.pickedUp == False):
					print("You have moved to the ingedient station!")
					print("Press A to pretend you said 'Pick up Pork'")
					while(1):
						if (keyboard.read_key() == "A" or keyboard.read_key() == "a"):
							print("Pork picked up!")
							porkchops.pickedUp = True
							break
				alreadyPrintedRed = 1
			elif (posGreen == 1 and alreadyPrintedGreen == 0):
				if (porkchops.pickedUp == False and porkchops.chopped == False):
					print("You have moved to the cooking station holding nothing")
				elif (porkchops.pickedUp == True and porkchops.chopped == True and porkchops.cooked == False):
					print("You have moved to the cooking station holding uncooked pork")
					print("Press A to pretend you waited for it to cook")
					while(1):
						if (keyboard.read_key() == "A" or keyboard.read_key() == "a"):
							print("Pork cooked!")
							porkchops.cooked = True
							break
				alreadyPrintedGreen = 1
		
		# Program Termination 
		cv2.imshow("Multiple Color Detection in Real-TIme", imageFrame) 
		if cv2.waitKey(10) & 0xFF == ord('q') or (porkchops.chopped == True and porkchops.cooked == True and porkchops.pickedUp == True): 
			cv2.destroyAllWindows() 
			print("You have sucessfully cooked Pork Chops!")
			quit()

		