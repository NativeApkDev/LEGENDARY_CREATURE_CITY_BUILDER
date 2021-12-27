"""
This file contains code for the server side of the game "Legendary Creature City Builder".
Author: NativeApkDev

The game "Legendary Creature City Builder" is inspired by "Dragon City"
(https://play.google.com/store/apps/details?id=es.socialpoint.DragonCity&hl=en_NZ&gl=US) and "Monster Legends"
(https://play.google.com/store/apps/details?id=es.socialpoint.MonsterLegends&hl=en_NZ&gl=US).

Code in this file is inspired by the following sources.
1. https://www.techwithtim.net/tutorials/python-online-game-tutorial/online-rock-paper-scissors-p-4/
2. https://www.youtube.com/watch?v=2klJP0DEsJg
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
from _thread import *

from mpmath import mp, mpf
from tabulate import tabulate
from legendary_creature_city_builder_client import *

mp.pretty = True


# Creating method to print out battle data in MP format


def mp_battle(x: str, y: str):
    global win1
    global win2
    if x == "1":
        user: LegendaryCreature = GameIG1.player_data.battle_team.get_legendary_creatures()[
            random.randint(0, len(GameIG1.player_data.battle_team.get_legendary_creatures()) - 1)
        ]
        target: LegendaryCreature = GameIG2.player_data.battle_team.get_legendary_creatures()[
            random.randint(0, len(GameIG2.player_data.battle_team.get_legendary_creatures()) - 1)
        ]
        raw_damage: mpf = user.attack_power * (1 + user.attack_power_percentage_up / 100 -
                                               user.attack_power_percentage_down / 100) * \
                          (1 + target.defense_percentage_up / 100 - target.defense_percentage_down / 100)
        damage_reduction_factor: mpf = mpf("1e8") / (mpf("1e8") + 3.5 * target.defense)
        damage1: mpf = raw_damage * damage_reduction_factor
        target.curr_hp -= damage1
        print(str(user.name) + " dealt " + str(damage1) + " damage on " + str(target.name) + "!")

    if y == "1":
        user: LegendaryCreature = GameIG2.player_data.battle_team.get_legendary_creatures()[
            random.randint(0, len(GameIG2.player_data.battle_team.get_legendary_creatures()) - 1)
        ]
        target: LegendaryCreature = GameIG1.player_data.battle_team.get_legendary_creatures()[
            random.randint(0, len(GameIG1.player_data.battle_team.get_legendary_creatures()) - 1)
        ]
        raw_damage: mpf = user.attack_power * (1 + user.attack_power_percentage_up / 100 -
                                               user.attack_power_percentage_down / 100) * \
                          (1 + target.defense_percentage_up / 100 - target.defense_percentage_down / 100)
        damage_reduction_factor: mpf = mpf("1e8") / (mpf("1e8") + 3.5 * target.defense)
        damage2: mpf = raw_damage * damage_reduction_factor
        target.curr_hp -= damage2
        print(str(user.name) + " dealt " + str(damage2) + " damage on " + str(target.name) + "!")
        if GameIG1.player_data.battle_team.all_died():
            win2 = 1
            win1 = 2
        elif GameIG2.player_data.battle_team.all_died():
            win1 = 1
            win2 = 2


def main():
    """
    Main function of the server
    :return: None
    """
    local_ip: str = socket.gethostbyname('localhost')
    host: str = local_ip  # IP address of the host
    port: int = 5555  # port number
    global win1
    win1 = 0
    global win2
    win2 = 0

    game_socket: socket.socket = socket.socket()
    game_socket.bind((host, port))

    game_socket.listen(1)
    c1, addr1 = game_socket.accept()
    print("Connection from: " + str(addr1))
    c2, addr2 = game_socket.accept()
    print("Connection from: " + str(addr2))

    data1: bytes = c1.recv(1024)
    global GameIG1
    GameIG1 = pickle.loads(data1)  # Game type
    data2: bytes = c2.recv(1024)
    global GameIG2
    GameIG2 = pickle.loads(data2)  # Game type
    c1.send(data2)
    c2.send(data1)

    while True:
        data1 = c1.recv(1024)
        data1_str: str = data1.decode()
        data2 = c2.recv(1024)
        data2_str: str = data2.decode()
        mp_battle(data1_str, data2_str)
        Player1Status = pickle.dumps([GameIG1, GameIG2, win1])
        Player2Status = pickle.dumps([GameIG2, GameIG1, win2])
        c1.send(Player1Status)
        c2.send(Player2Status)

    c1.close()
    c2.close()
    game_socket.close()


if __name__ == '__main__':
    main()
