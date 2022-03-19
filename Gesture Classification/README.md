# Gesture Classification README

Source Code:
- Overcooked_Gestures.py: Contains utility testing and plotting of the raw IMU data that was used.
- berryIMU.py: Contains the code that runs on the IMU hardware, so it reads in the data and classifies appropriately.

Data:
The *.mp4 files and *.txt files refer to the videos of successful gesture classification as well as raw IMU data, respectively.

Design:
The script utilizes time-series data of the gyroscopic X and gyroscopic Z values to calculate power, which is then used to establish a threshold decision boundary.

Bugs:
Note that the algorithm has not been optimized properly, and will require further testing and training with more and varied data.

Plan:
- Integrate with the visuals-based prototype game.
- Debug and ensure that MQTT improvements will work properly with the gesture classification algorithm.
- Refactor the code to remove unnecessary commands to help ensure runtime speedup. 
