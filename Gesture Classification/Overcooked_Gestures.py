# -*- coding: utf-8 -*-
"""
Created on Wed Feb  9 09:43:58 2022

@author: Kellen Cheng
"""

# Import Statements
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier

# %% Retrieve Gesture Data
def process_data(filename):
    with open(filename) as f:
        lines = f.readlines()
    
    for i in range(len(lines)):
        tmp = lines[i].split(",")
        for j in range(len(tmp)):
            tmp[j] = float(tmp[j])
        lines[i] = tmp
    
    # N.B. Data Format -> GyroX, GyroY, GyroZ, AccX, AccY, AccZ
    return np.array(lines)

# Collect chopping training data
chopping1 = process_data("chopping1.txt")
chopping2 = process_data("chopping2.txt")
chopping3 = process_data("chopping3.txt")
chopping4 = process_data("chopping4.txt")
chopping5 = process_data("chopping5.txt")

# Collect stirring training data
stirring1 = process_data("stirring1.txt")
stirring2 = process_data("stirring2.txt")
stirring3 = process_data("stirring3.txt")
stirring4 = process_data("stirring4.txt")
stirring5 = process_data("stirring5.txt")

# Collect chopping testing data
test_chop1 = process_data("test_chop1.txt")
test_chop2 = process_data("test_chop2.txt")
test_chop3 = process_data("test_chop3.txt")

# Collect stirring testing data
test_stir1 = process_data("test_stir1.txt")
test_stir2 = process_data("test_stir2.txt")
test_stir3 = process_data("test_stir3.txt")

# %% Power of Training Data
def gesture_power(gX, gZ):
    return np.sum(gX**2 + gZ**2)

train_chops = [chopping1, chopping2, chopping3, chopping4, chopping5]
train_stir = [stirring1, stirring2, stirring3, stirring4, stirring5]

test_chops = [test_chop1, test_chop2, test_chop3]
test_stir = [test_stir1, test_stir2, test_stir3]

chops = []
for elem in train_chops:
    chops.append(elem)
for elem in test_chops:
    chops.append(elem)
    
stirs = []
for elem in train_stir:
    stirs.append(elem)
for elem in test_stir:
    stirs.append(elem)

train_chop_power = [gesture_power(data[:, 0], data[:, 2]) for data in train_chops]
train_stir_power = [gesture_power(data[:, 0], data[:, 2]) for data in train_stir]
test_chop_power = [gesture_power(data[:, 0], data[:, 2]) for data in test_chops]
test_stir_power = [gesture_power(data[:, 0], data[:, 2]) for data in test_stir]

# %% Plot gX Values
gXes_chop = [elem[:, 0] for elem in chops]
gZes_chop = [elem[:, 2] for elem in chops]
gXes_stir = [elem[:, 0] for elem in stirs]
gZes_stir = [elem[:, 2] for elem in stirs]

# %% Process Gyroscopic Values
gXes_chop = np.array(gXes_chop)
print(gXes_chop.shape)
gXes_chop = np.reshape(gXes_chop, gXes_chop.shape[0] * gXes_chop.shape[1])

gXes_stir = np.array(gXes_stir)
gXes_stir = np.reshape(gXes_stir, gXes_stir.shape[0] * gXes_stir.shape[1])

gZes_chop = np.array(gZes_chop)
gZes_chop = np.reshape(gZes_chop, gZes_chop.shape[0] * gZes_chop.shape[1])

gZes_stir = np.array(gZes_stir)
gZes_stir = np.reshape(gZes_stir, gZes_stir.shape[0] * gZes_stir.shape[1])

# %% Plot Gyroscopic Values
plt.title("Visualization of Gyroscopic X-Axis Stir v. Chop Gestures")
plt.plot(gXes_chop, c="black")
plt.plot(gXes_stir, c="red")
plt.xlabel("Time Point")
plt.ylabel("Gyroscopic Value")

plt.figure()
plt.title("Visualization of Gyroscopic Z-Axis Stir v. Chop Gestures")
plt.plot(gZes_chop, c="black")
plt.plot(gZes_stir, c="red")
plt.xlabel("Time Point")
plt.ylabel("Gyroscopic Value")

# %% Plot Gesture Powers
plt.title("Training: Gesture Power v. Trial")
plt.plot(train_chop_power, c="black")
plt.plot(train_stir_power, c="red")
plt.xlim([1.0, 5.0])
plt.xticks([0, 1, 2, 3, 4], [1.0, 2.0, 3.0, 4.0, 5.0])
plt.xlabel("Trial Data Number")
plt.ylabel("Gesture Power (100 Time Points)")

plt.figure()
plt.title("Testing: Gesture Power v. Trial")
plt.plot(test_chop_power, c="black")
plt.plot(test_stir_power, c="red")
plt.xlim([1.0, 3.0])
plt.xticks([0, 1, 2], [1.0, 2.0, 3.0])
plt.xlabel("Trial Data Number")
plt.ylabel("Gesture Power (100 Time Points)")

# %% Compose Training and Testing Dataset
X_train = np.array([chopping1, chopping2, chopping3, chopping4, chopping5,
                    stirring1, stirring2, stirring3, stirring4, stirring5])
y_train = np.array([0, 0, 0, 0, 0, 1, 1, 1, 1, 1]) # 0 -> chop, 1 -> stir

X_test = np.array([test_chop1, test_chop2, test_chop3, 
                   test_stir1, test_stir2, test_stir3])
y_test = np.array([0, 0, 0, 1, 1, 1]) # 0 -> chop, 1 -> stir

# Reshape X_train and X_test
X_train = np.reshape(X_train, (X_train.shape[0], -1))
X_test = np.reshape(X_test, (X_test.shape[0], -1))

# %% Testing Cell
# clf = DecisionTreeClassifier(random_state=0)
# clf.fit(X_train, y_train)
# rand_gesture = np.reshape(test_chop2, (1, -1))
# y = clf.predict(rand_gesture)



# Retrieve Parameters
gyroX = test_stir1[:, 0]
gyroY = test_stir1[:, 1]
gyroZ = test_stir1[:, 2]
accX = test_stir1[:, 3]
accY = test_stir1[:, 4]
accZ = test_stir1[:, 5]

# gyroX = test_chop1[:, 0]
# gyroY = test_chop1[:, 1]
# gyroZ = test_chop1[:, 2]
# accX = test_chop1[:, 3]
# accY = test_chop1[:, 4]
# accZ = test_chop1[:, 5]

# Plot Parameters
plt.plot(gyroX)
plt.figure()
plt.plot(gyroY)
plt.figure()
plt.plot(gyroZ)
plt.figure()
plt.plot(accX)
plt.figure()
plt.plot(accY)
plt.figure()
plt.plot(accZ)

xyz1 = np.sum(gyroX**2 + gyroZ**2) # N.B. Remove gyroY for better results!
xyz2 = np.sum(accX**2 + accY**2 + accZ**2)
print("Avg. Gyro Power:", str(xyz1)) # Chop -> 80k to 150k, Stir -> 40k to 50k
print("Avg. Acc Power:", str(xyz2)) # Chop -> ~8k, Stir -> ~8k
























