# Localization


Source Code:

1. color.py: Contains our localization program

References:
1. https://machinelearningknowledge.ai/learn-object-tracking-in-opencv-python-with-code-examples/ (Object Tracking)
2. https://medium.com/easyread/mouse-control-for-shooting-game-using-opencv-and-python-452c3446d1a3 (Mouse Movement)

Design:

After running the program, the user's webcam is displayed with text that tells the user to place an object within a predetermined bounding box. Once the user does so, there is instruction to press 'b' when ready which will then start the object tracking algorithm on the user's object. Along with being able to move their cursor by moving their object, a user can register a click by staying still for 1-2 seconds. This program uses OpenCV's Mean Shift Algorithm Tracker along with our self-developed bounding box stabilizing algorithms and RGB average profiler. Our stabilizing algorithm predicts when a user wants to stay still and then makes the bounding box have less movement, while our RGB average profiler allows a user to stop tracking when their hand gets tired by placing the object out of frame and comparing RGB average values.

Bugs:

1. Bad lighting conditions can make object tracking very unstable


Plan:

1. Make it within the game rather than being autonomous while delivering high framerate
