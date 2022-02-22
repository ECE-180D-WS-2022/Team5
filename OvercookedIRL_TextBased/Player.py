import sys
import os
from Station import Station

class Player:
    def __init__(self, name):
        self.name = name
        self.inventory = []
        self.location = "Starting Position"
        self.plate = []