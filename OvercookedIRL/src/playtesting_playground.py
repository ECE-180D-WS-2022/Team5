# -*- coding: utf-8 -*-
"""
Created on Sat May 28 11:05:48 2022

@author: Kellen Cheng
"""

# File is used to test for small loops, other miscellaneous small bits of code
import pygame
import time
import datetime

timer = pygame.time.Clock()

start = time.perf_counter()

def format_timedelta(td):
    minutes, seconds = divmod(td.seconds + td.days * 86400, 60)
    hours, minutes = divmod(minutes, 60)
    return '{:02d}:{:02d}'.format(minutes, seconds)

increment = datetime.timedelta(seconds=1.0)
interval = datetime.timedelta(minutes=10.0)
while(True):
    tick = time.perf_counter()
    temp = datetime.timedelta(seconds=tick-start)
    time_left = interval-temp
    
    print(format_timedelta(time_left))
    
# %%
t1 = format_timedelta(time_left)
t11 = datetime.datetime.strptime(t1, "%M:%S")
if datetime.timedelta(minutes=t11.minute, seconds=t11.second) > interval - datetime.timedelta(seconds=30.0):
    print("Here!")
