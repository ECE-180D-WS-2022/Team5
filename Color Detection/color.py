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
font = cv2.FONT_HERSHEY_COMPLEX
m = PyMouse()

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
		if cv2.contourArea(c) <= 6000 :
			continue
		area = cv2.contourArea(c)
		approx = cv2.approxPolyDP(c, 0.01*cv2.arcLength(c, True), True)
		x, y, _, _ = cv2.boundingRect(c)

		if 10 < len(approx) < 30:
			cv2.putText(frame, "Circle", (x, y), font, 1, (0, 0, 0))
			cv2.drawContours(frame, [approx], -1, (0, 255, 0), 3)
			m.move(x + 400, y + 400)
			print(x,y)

	cv2.imshow("frame", frame)
	
	key = cv2.waitKey(1)
	if key == 27:
		break

cap.release()
cv2.destroyAllWindows()

# https://pysource.com/2018/12/29/real-time-shape-detection-opencv-with-python-3/
# https://medium.com/easyread/mouse-control-for-shooting-game-using-opencv-and-python-452c3446d1a3