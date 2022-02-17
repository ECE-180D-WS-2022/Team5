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

cap = cv2.VideoCapture(0)

m = PyMouse()

while True:
	_, frame = cap.read()
	frame = cv2.flip(frame, 1)

	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	lower_green = np.array([58, 77, 62])
	upper_green = np.array([93, 249, 255])
	mask_green = cv2.inRange(hsv, lower_green, upper_green)

	contoursGreen, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	for c in contoursGreen :
		if cv2.contourArea(c) <= 500 :
			continue
		x, y, _, _ = cv2.boundingRect(c)
		m.move(x, y)
		cv2.drawContours(frame, contoursGreen, -1, (0, 255, 0), 3)

	frame = image_resize(frame, width = 400)  
	cv2.imshow("frame", frame)
	
	key = cv2.waitKey(1)
	if key == 27:
		break

cap.release()
cv2.destroyAllWindows()

# https://pysource.com/2018/12/29/real-time-shape-detection-opencv-with-python-3/
# https://medium.com/easyread/mouse-control-for-shooting-game-using-opencv-and-python-452c3446d1a3