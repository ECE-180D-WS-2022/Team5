import sys
import os
from Station import Station

class Station_Manager:
    def __init__(self):
        self.stations = []

        S1 = Station("Cutting Station", None)
        self.stations.append(S1)

        S2 = Station("Stove Station", None)
        self.stations.append(S2)

        S3 = Station("Ingredients Station", None)
        self.stations.append(S3)

        S4 = Station("Submit Station", None)
        self.stations.append(S4)

        S5 = Station("Share Station", None)
        self.stations.append(S5)

        S6 = Station("Plate Station", None)
        self.stations.append(S6)

        S7 = Station("Counter", None)
        self.stations.append(S7)
