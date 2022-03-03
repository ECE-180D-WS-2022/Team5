from turtle import xcor
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


tracker = cv2.TrackerCSRT_create()

# Camera setup
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Mouse movement functionality
m = PyMouse()
last_x = 99999
last_y = 99999
posCount = 0
clicked = False

ok, frame = cap.read()
frame = cv2.flip(frame, 1)

bbox = cv2.selectROI(frame)

ok = tracker.init(frame,bbox)

while True:
	ok, frame= cap.read()
	frame = cv2.flip(frame, 1)

	if not ok:
		break

	ok, bbox = tracker.update(frame)

	if ok:
		(x,y,w,h)=[int(v) for v in bbox]
		cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2,1)
		m.move(x,y)

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

	else:
		cv2.putText(frame,'Error',(100,0),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)

	frame = image_resize(frame, width = 600) 
	cv2.imshow('Tracking',frame)

	if cv2.waitKey(1) & 0XFF==27:
		break

cv2.destroyAllWindows()