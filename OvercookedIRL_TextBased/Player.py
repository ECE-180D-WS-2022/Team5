import sys
import os

class Player:
    def __init__(self, name):
        self.name = name
        self.inventory = []
        self.location = "Starting Position"