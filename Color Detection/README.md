# Localization


Source Code:

1. color.py: Contains our localization program

References:
1. https://machinelearningknowledge.ai/learn-object-tracking-in-opencv-python-with-code-examples/ (Object Tracking)
2. https://medium.com/easyread/mouse-control-for-shooting-game-using-opencv-and-python-452c3446d1a3 (Mouse Movement)

Design:

After running the program, the user's webcam is displayed with text that tells the user to put up an object. Once ready, the user will be prompted to select a region of interest (the object), and once selected the user will be able to move their mouse by moving their object. For the clicking functionality, if the user's cursor position does not move for ~2 seconds (by not moving their object) the program will register a click.

Bugs:

1. Moving the object out of frame will not stop tracking, it will just leave the bounding box on the object's last position before becoming out of frame.
2. Having the user select a region of interest is a bad design because new users don't know the best calibration needed to have flawless movement.


Plan:

1. Based on several trials, the program should stop tracking once the object is out of frame and start tracking again once it reenters. This will need to be implemented in the case that a user does not want to always hold up their object.
2. Automate the region selection stage so the user does not have the full responsibility of getting the perfect calibration
3. Enhance stabilizer so in the case of bad calibration, the mouse will still not be jittery.
