"""
This file contains code for the server side of the game "Legendary Creature City Builder".
Author: NativeApkDev

The game "Legendary Creature City Builder" is inspired by "Dragon City"
(https://play.google.com/store/apps/details?id=es.socialpoint.DragonCity&hl=en_NZ&gl=US) and "Monster Legends"
(https://play.google.com/store/apps/details?id=es.socialpoint.MonsterLegends&hl=en_NZ&gl=US).
"""


# Game version: 1


# Importing necessary libraries


import sys
import uuid
import pickle
import copy
import random
from datetime import datetime
import os
from functools import reduce
import socket

from mpmath import mp, mpf
from tabulate import tabulate
from legendary_creature_city_builder_client import *

mp.pretty = True

# Creating static variables for the server


HOST: str = "10.11.250.207"  # IP address of the host
PORT: int = 5555  # port number

game_socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
