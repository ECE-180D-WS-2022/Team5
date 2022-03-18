import sys
import os
from Ingredients import Ingredients

class Station:
    def __init__(self, station_name, ingredient):
        self.station_name = station_name
        self.location = self.station_name
        self.ingredient = ingredient #current ingredient or plate object at the station
        self.busy = 0 # 0 is not busy, so able to place item here; 1 means busy, so cannot place item here