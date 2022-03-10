import cv2
import numpy as np
from pymouse import PyMouse

# Resize camera feed
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

# Camera setup
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Resize camera
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Mouse movement functionality
m = PyMouse()
last_x = 99999
last_y = 99999
posCount = 0
clicked = False

# Tracker functionality
ret,frame=cap.read()
x,y,w,h = cv2.selectROI('select', frame)
cv2.destroyWindow('select')
track_window = (x, y, w, h)
roi = frame[y:y+h, x:x+w]
hsv_roi =  cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv_roi, np.array((0., 60.,32.)), np.array((180.,255.,255.)))
roi_hist = cv2.calcHist([hsv_roi],[0],mask,[180],[0,180])
cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)
term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )

while(1):
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    
    if ret == True:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        dst = cv2.calcBackProject([hsv],[0],roi_hist,[0,180],1)
        ret, track_window = cv2.meanShift(dst, track_window, term_crit)
        x,y,w,h = track_window
       
        frame = cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0),2)
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

        frame = image_resize(frame, width = 480, height = 640) 
        cv2.imshow('Camera',frame)

        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
    else:
        break

cv2.destroyAllWindows()