import cv2
import numpy as np
from pymouse import PyMouse
import keyboard

font = cv2.FONT_HERSHEY_DUPLEX

# Calibration Stage
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Mouse movement functionality
m = PyMouse()
last_x = 99999
last_y = 99999
posCount = 0
clicked = False
selected = False
term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )
buffer = 0

# Mouse Movement Stage
while(1):   
    ret, frame = cap.read()
    cv2.normalize(frame, frame, 30, 230, cv2.NORM_MINMAX)
    frame = cv2.flip(frame, 1)

    if ret == True:
        if selected == False:
            frame = cv2.rectangle(frame, (100,100), (100+100,100+100), (0,255,0),3)
            cv2.putText(frame, 'Place object in square', (50, 50), font, 1, (0, 0, 255), 2)
            cv2.putText(frame, 'press b when ready', (50, 80), font, 1, (0, 0, 255), 2)

            if keyboard.is_pressed('b'):
                x,y,w,h = 100, 100, 100, 100
                track_window = (x, y, w, h)
                roi = frame[y:y+h, x:x+w]
                hsv_roi =  cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
                mask = cv2.inRange(hsv_roi, np.array((0., 60.,32.)), np.array((180.,255.,255.)))
                roi_hist = cv2.calcHist([hsv_roi],[0],mask,[180],[0,180])
                cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)
                region = frame[y:y+h, x:x+w]
                last_b, last_g, last_r = np.mean(region, axis=(0, 1))
                selected = True

        if selected == True:
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            dst = cv2.calcBackProject([hsv],[0],roi_hist,[0,180],1)
            ret, track_window = cv2.meanShift(dst, track_window, term_crit)
            x,y,w,h = track_window

            if (buffer <= 10):
                region = frame[y:y+h, x:x+w]
                b, g, r = np.mean(region, axis=(0, 1))
                buffer += 1
            else:
                ret, color_window = cv2.CamShift(dst, track_window, term_crit)
                o,p,q,r = color_window
                region = frame[p:p+r, o:o+q]
                b, g, r = np.mean(region, axis=(0, 1))

            if (abs(b - last_b) < 30) and (abs(g - last_g) < 30) and (abs(r - last_r) < 30):
                if last_x == 99999:
                    frame = cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0),3)

                scaled_x = int(x * 3)
                scaled_y = int(y * 3)

                m.move(scaled_x, scaled_y)

                if (abs(scaled_x - last_x) < 15) and (abs(scaled_y - last_y) < 15):
                    posCount += 1
                    frame = cv2.rectangle(frame, (frameX,frameY), (frameX+frameW,frameY+frameH), (0,255,0),3)

                    if (posCount >= 15 and clicked == False):
                        m.click(scaled_x, scaled_y)
                        clicked = True
                    elif (posCount >= 1 and posCount < 15 and clicked == False):
                        m.move(last_x, last_y)
                        scaled_x = last_x
                        scaled_y = last_y
                        if (posCount == 5):
                            last_b = b
                            last_g = g
                            last_r = r
                else:
                    posCount = 0
                    frame = cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0),3)
                
                last_x = scaled_x
                last_y = scaled_y

                if posCount == 0:
                    frameX = x
                    frameY = y
                    frameW = w
                    frameH = h

                if (clicked == True):
                    clicked = False
                    posCount = 0
            else:
                frame = cv2.rectangle(frame, (x,y), (x+w,y+h), (0,0,255),3)


        cv2.imshow('Mouse Movement',frame)

        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
    else:
        break

cv2.destroyAllWindows()