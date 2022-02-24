import cv2
import numpy as np
from pymouse import PyMouse

def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image

    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)

    else:
        r = width / float(w)
        dim = (width, int(h * r))

    resized = cv2.resize(image, dim, interpolation = inter)

    return resized


def mouseMovement():
	cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
	cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
	cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

	font = cv2.FONT_HERSHEY_COMPLEX
	m = PyMouse()

	last_x = 99999
	last_y = 99999
	posCount = 0
	clicked = False

	while True:
		_, frame = cap.read()
		frame = cv2.flip(frame, 1)

		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

		lower_green = np.array([18, 67, 38])
		upper_green = np.array([100, 255, 255])
		mask_green = cv2.inRange(hsv, lower_green, upper_green)

		kernel = np.ones((5,5), np.uint8)
		mask_green = cv2.erode(mask_green, kernel)

		contoursGreen, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

		for c in contoursGreen :
			if cv2.contourArea(c) <= 400 :
				continue
			area = cv2.contourArea(c)
			approx = cv2.approxPolyDP(c, 0.01*cv2.arcLength(c, True), True)

			if 10 < len(approx) < 30:
				x, y, _, _ = cv2.boundingRect(c)
				print(x,y)
				cv2.putText(frame, "Circle", (x, y), font, 1, (0, 0, 0))
				cv2.drawContours(frame, [approx], -1, (0, 255, 0), 3)
				m.move(x, y)

				if (abs(x - last_x) < 5) and (abs(y - last_y) < 5):
					posCount += 1
					if (posCount >= 20 and clicked == False):
						m.click(x,y)
						clicked = True
				else:
					posCount = 0
				last_x = x
				last_y = y
					
		if (clicked == True):
			clicked = False
			posCount = 0


		frame = image_resize(frame, width = 400) 
		cv2.imshow("frame", frame)
		
	# 	key = cv2.waitKey(1)
	# 	if key == 27:
	# 		break

	# cap.release()
	# cv2.destroyAllWindows()

# https://pysource.com/2018/12/29/real-time-shape-detection-opencv-with-python-3/
# https://medium.com/easyread/mouse-control-for-shooting-game-using-opencv-and-python-452c3446d1a3