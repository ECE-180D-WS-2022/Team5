# -*- coding: utf-8 -*-
"""
Created on Sat May 28 11:05:48 2022

@author: Kellen Cheng
"""

# File is used to test for small loops, other miscellaneous small bits of code
import pygame
import time
import datetime
interval = datetime.timedelta(seconds=1.0)
startTime = time.perf_counter()
while True:
    tick = time.perf_counter()
    time_left = interval - datetime.timedelta(seconds=tick-startTime)
    zero_time = datetime.timedelta(seconds=0.0)
    print("Time left:", str(time_left), "BOOL:", str(time_left < zero_time))
