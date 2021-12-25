"""
This file contains code for the client side of the game "Legendary Creature City Builder".
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
from minigames import *

from mpmath import mp, mpf
from tabulate import tabulate

mp.pretty = True

# Creating static variables to be used throughout the game.


LETTERS: str = "abcdefghijklmnopqrstuvwxyz"
HOST: str  # IP address of the host
PORT: int  # port number


# Creating static functions to be used in this game.


def is_number(string: str) -> bool:
    try:
        mpf(string)
        return True
    except ValueError:
        return False


def generate_random_name() -> str:
    res: str = ""  # initial value
    name_length: int = random.randint(5, 20)
    for i in range(name_length):
        res += LETTERS[random.randint(0, len(LETTERS) - 1)]

    return res.capitalize()


def triangular(n: int) -> int:
    return int(n * (n - 1) / 2)


def mpf_sum_of_list(a_list: list) -> mpf:
    return mpf(str(sum(mpf(str(elem)) for elem in a_list if is_number(str(elem)))))


def mpf_product_of_list(a_list: list) -> mpf:
    return mpf(reduce(lambda x, y: mpf(x) * mpf(y) if is_number(x) and
                                                      is_number(y) else mpf(x) if is_number(x) and not is_number(
        y) else mpf(y) if is_number(y) and not is_number(x) else 1, a_list, 1))


def load_game_data(file_name):
    # type: (str) -> Game
    return pickle.load(open(file_name, "rb"))


def save_game_data(game_data, file_name):
    # type: (Game, str) -> None
    pickle.dump(game_data, open(file_name, "wb"))


def clear():
    # type: () -> None
    if sys.platform.startswith('win'):
        os.system('cls')  # For Windows System
    else:
        os.system('clear')  # For Linux System


# Creating necessary classes to be used throughout the game.


class Action:
    """
    This class contains attributes of an action that can be carried out during battles in this game.
    """

    POSSIBLE_NAMES: list = ["NORMAL ATTACK", "NORMAL HEAL", "USE SKILL"]

    def __str__(self):
        # type: () -> str
        res: str = str(type(self).__name__) + "("  # initial value
        index: int = 0  # initial value
        for item in vars(self).items():
            res += str(item[0]) + "=" + str(item[1])

            if index < len(vars(self).items()) - 1:
                res += ", "

            index += 1

        return res + ")"


class AwakenBonus:
    """
    This class contains attributes of the bonus gained for awakening a legendary creature.
    """

    def __str__(self):
        # type: () -> str
        res: str = str(type(self).__name__) + "("  # initial value
        index: int = 0  # initial value
        for item in vars(self).items():
            res += str(item[0]) + "=" + str(item[1])

            if index < len(vars(self).items()) - 1:
                res += ", "

            index += 1

        return res + ")"


class Arena:
    """
    This class contains attributes of a battle arena in this game.
    """

    def __str__(self):
        # type: () -> str
        res: str = str(type(self).__name__) + "("  # initial value
        index: int = 0  # initial value
        for item in vars(self).items():
            res += str(item[0]) + "=" + str(item[1])

            if index < len(vars(self).items()) - 1:
                res += ", "

            index += 1

        return res + ")"


class Level:
    """
    This class contains attributes of a level for single player battles in this game.
    """


class Stage:
    """
    This class contains attributes of a stage in a level in this game.
    """


class Player:
    """
    This class contains attributes of the player in this game.
    """

    def __init__(self, name):
        # type: (str) -> None
        self.player_id: str = str(uuid.uuid1())  # generating random player ID
        self.name: str = name
        self.level: int = 1
        self.exp: mpf = mpf("0")
        self.required_exp: mpf = mpf("1e6")
        self.exp_per_second: mpf = mpf("0")
        self.gold: mpf = mpf("5e6")
        self.gold_per_second: mpf = mpf("0")
        self.gems: mpf = mpf("100")
        self.gems_per_second: mpf = mpf("0")
        self.food: mpf = mpf("0")
        self.food_per_second: mpf = mpf("0")
        self.arena_points: int = 1000
        self.arena_wins: int = 0
        self.arena_losses: int = 0
        self.battle_team: Team = Team()
        self.item_inventory: ItemInventory = ItemInventory()
        self.legendary_creature_inventory: LegendaryCreatureInventory = LegendaryCreatureInventory()
        self.player_city: PlayerCity = PlayerCity()

    def __str__(self):
        # type: () -> str
        res: str = str(type(self).__name__) + "("  # initial value
        index: int = 0  # initial value
        for item in vars(self).items():
            res += str(item[0]) + "=" + str(item[1])

            if index < len(vars(self).items()) - 1:
                res += ", "

            index += 1

        return res + ")"

    def clone(self):
        # type: () -> Player
        return copy.deepcopy(self)


class PlayerCity:
    """
    This class contains attributes of the city the player builds.
    """

    def __str__(self):
        # type: () -> str
        res: str = str(type(self).__name__) + "("  # initial value
        index: int = 0  # initial value
        for item in vars(self).items():
            res += str(item[0]) + "=" + str(item[1])

            if index < len(vars(self).items()) - 1:
                res += ", "

            index += 1

        return res + ")"


class CityTile:
    """
    This class contains attributes of a tile which can be built in a player's city.
    """

    def __init__(self, building=None):
        # type: (Building or None) -> None
        self.building: Building or None = building

    def __str__(self):
        # type: () -> str
        res: str = str(type(self).__name__) + "("  # initial value
        index: int = 0  # initial value
        for item in vars(self).items():
            res += str(item[0]) + "=" + str(item[1])

            if index < len(vars(self).items()) - 1:
                res += ", "

            index += 1

        return res + ")"


class Team:
    """
    This class contains attributes of a team of legendary creatures brought to battles.
    """

    MAX_LEGENDARY_CREATURES: int = 5

    def __init__(self, legendary_creatures=None):
        # type: (list) -> None
        if legendary_creatures is None:
            legendary_creatures = []
        self.__legendary_creatures: list = legendary_creatures if len(legendary_creatures) <= \
                                                                  self.MAX_LEGENDARY_CREATURES else []
        self.leader: LegendaryCreature or None = None if len(self.__legendary_creatures) == 0 else \
            self.__legendary_creatures[0]

    def set_leader(self, leader):
        # type: (LegendaryCreature) -> None
        if leader not in self.__legendary_creatures or len(self.__legendary_creatures) == 0:
            self.leader = None
        else:
            self.leader = leader

    def __str__(self):
        # type: () -> str
        res: str = str(type(self).__name__) + "("  # initial value
        index: int = 0  # initial value
        for item in vars(self).items():
            res += str(item[0]) + "=" + str(item[1])

            if index < len(vars(self).items()) - 1:
                res += ", "

            index += 1

        return res + ")"

    def clone(self):
        # type: () -> Team
        return copy.deepcopy(self)


class LegendaryCreatureInventory:
    """
    This class contains attributes of an inventory containing legendary creatures.
    """

    def __str__(self):
        # type: () -> str
        res: str = str(type(self).__name__) + "("  # initial value
        index: int = 0  # initial value
        for item in vars(self).items():
            res += str(item[0]) + "=" + str(item[1])

            if index < len(vars(self).items()) - 1:
                res += ", "

            index += 1

        return res + ")"


class ItemInventory:
    """
    This class contains attributes of an inventory containing items.
    """

    def __init__(self):
        # type: () -> None
        self.__items: list = []  # initial value

    def get_items(self):
        # type: () -> list
        return self.__items

    def __str__(self):
        # type: () -> str
        res: str = str(type(self).__name__) + "("  # initial value
        index: int = 0  # initial value
        for item in vars(self).items():
            res += str(item[0]) + "=" + str(item[1])

            if index < len(vars(self).items()) - 1:
                res += ", "

            index += 1

        return res + ")"


class LegendaryCreature:
    """
    This class contains attributes of a legendary creature in this game.
    """

    MIN_CRIT_RATE: mpf = mpf("0.15")
    MIN_CRIT_DAMAGE: mpf = mpf("1.5")
    MIN_RESISTANCE: mpf = mpf("0.15")
    MAX_RESISTANCE: mpf = mpf("1")
    MIN_ACCURACY: mpf = mpf("0")
    MAX_ACCURACY: mpf = mpf("1")
    MIN_ATTACK_GAUGE: mpf = mpf("0")
    FULL_ATTACK_GAUGE: mpf = mpf("1")
    MIN_REFLECTED_DAMAGE_PERCENTAGE: mpf = mpf("0")
    MIN_LIFE_DRAIN_PERCENTAGE: mpf = mpf("0")
    MIN_CRIT_RESIST: mpf = mpf("0")
    MAX_CRIT_RESIST: mpf = mpf("1")
    MIN_GLANCING_HIT_CHANCE: mpf = mpf("0")
    MIN_BENEFICIAL_EFFECTS: int = 0
    MAX_BENEFICIAL_EFFECTS: int = 10
    MIN_HARMFUL_EFFECTS: int = 0
    MAX_HARMFUL_EFFECTS: int = 10
    POTENTIAL_ELEMENTS: list = ["TERRA", "FLAME", "SEA", "NATURE", "ELECTRIC", "ICE", "METAL", "DARK", "LIGHT", "WAR",
                                "PURE", "LEGEND", "PRIMAL", "WIND", "BEAUTY", "MAGIC", "CHAOS", "HAPPY", "DREAM",
                                "SOUL"]

    def __init__(self, name, main_element, max_hp, max_magic_points, attack_power, defense, attack_speed, skills,
                 awaken_bonus):
        # type: (str, str, mpf, mpf, mpf, mpf, mpf, list, AwakenBonus) -> None
        self.legendary_creature_id: str = str(uuid.uuid1())  # generating random legendary creature ID
        self.name: str = name
        self.__elements: list = [main_element if main_element in self.POTENTIAL_ELEMENTS else
                                 self.POTENTIAL_ELEMENTS[0]]  # a list of elements the legendary creature has. The main
        # (i.e., first) element will be the element considered as the defending element of this legendary creature.
        self.level: int = 1  # initial value
        self.exp: mpf = mpf("0")
        self.required_exp: mpf = mpf("1e6")
        self.exp_per_second: mpf = mpf("0")
        self.curr_hp: mpf = max_hp
        self.max_hp: mpf = max_hp
        self.curr_magic_points: mpf = max_magic_points
        self.max_magic_points: mpf = max_magic_points
        self.attack_power: mpf = attack_power
        self.defense: mpf = defense
        self.attack_speed: mpf = attack_speed
        self.crit_rate: mpf = self.MIN_CRIT_RATE
        self.crit_damage: mpf = self.MIN_CRIT_DAMAGE
        self.resistance: mpf = self.MIN_RESISTANCE
        self.accuracy: mpf = self.MIN_ACCURACY
        self.__skills: list = skills
        self.awaken_bonus: AwakenBonus = awaken_bonus
        self.attack_gauge: mpf = self.MIN_ATTACK_GAUGE
        self.corresponding_team: Team = Team()

    def get_elements(self):
        # type: () -> list
        return self.__elements

    def get_skills(self):
        # type: () -> list
        return self.__skills

    def __str__(self):
        # type: () -> str
        res: str = str(type(self).__name__) + "("  # initial value
        index: int = 0  # initial value
        for item in vars(self).items():
            res += str(item[0]) + "=" + str(item[1])

            if index < len(vars(self).items()) - 1:
                res += ", "

            index += 1

        return res + ")"

    def clone(self):
        # type: () -> LegendaryCreature
        return copy.deepcopy(self)


class Item:
    """
    This class contains attributes of an item in this game.
    """

    def __str__(self):
        # type: () -> str
        res: str = str(type(self).__name__) + "("  # initial value
        index: int = 0  # initial value
        for item in vars(self).items():
            res += str(item[0]) + "=" + str(item[1])

            if index < len(vars(self).items()) - 1:
                res += ", "

            index += 1

        return res + ")"


class Egg(Item):
    """
    This class contains attributes of an egg which can be hatched for legendary creatures to come out.
    """


class Rune(Item):
    """
    This class contains attributes of a rune used to strengthen legendary creatures.
    """


class Skill:
    """
    This class contains attributes of a skill legendary creatures have.
    """

    def __str__(self):
        # type: () -> str
        res: str = str(type(self).__name__) + "("  # initial value
        index: int = 0  # initial value
        for item in vars(self).items():
            res += str(item[0]) + "=" + str(item[1])

            if index < len(vars(self).items()) - 1:
                res += ", "

            index += 1

        return res + ")"

    def clone(self):
        # type: () -> Skill
        return copy.deepcopy(self)


class ActiveSkill(Skill):
    """
    This class contains attributes of an active skill legendary creatures have.
    """


class PassiveSkill(Skill):
    """
    This class contains attributes of a passive skill legendary creatures have.
    """


class LeaderSkill(Skill):
    """
    This class contains attributes of a leader skill legendary creatures have.
    """


class DamageMultiplier:
    """
    This class contains attributes of the damage multiplier of a skill.
    """

    def __str__(self):
        # type: () -> str
        res: str = str(type(self).__name__) + "("  # initial value
        index: int = 0  # initial value
        for item in vars(self).items():
            res += str(item[0]) + "=" + str(item[1])

            if index < len(vars(self).items()) - 1:
                res += ", "

            index += 1

        return res + ")"


class BeneficialEffect:
    """
    This class contains attributes of a beneficial effect a legendary creature has.
    """

    POSSIBLE_NAMES: list = []

    def __str__(self):
        # type: () -> str
        res: str = str(type(self).__name__) + "("  # initial value
        index: int = 0  # initial value
        for item in vars(self).items():
            res += str(item[0]) + "=" + str(item[1])

            if index < len(vars(self).items()) - 1:
                res += ", "

            index += 1

        return res + ")"


class HarmfulEffect:
    """
    This class contains attributes of a harmful effect a legendary creature has.
    """

    POSSIBLE_NAMES: list = []

    def __str__(self):
        # type: () -> str
        res: str = str(type(self).__name__) + "("  # initial value
        index: int = 0  # initial value
        for item in vars(self).items():
            res += str(item[0]) + "=" + str(item[1])

            if index < len(vars(self).items()) - 1:
                res += ", "

            index += 1

        return res + ")"


class Building:
    """
    This class contains attributes of a building which can be built on a city tile.
    """


class Habitat(Building):
    """
    This class contains attributes of a habitat where legendary creatures live.
    """


class Obstacle(Building):
    """
    This class contains attributes of an obstacle to be removed by the player.
    """


class Reward:
    """
    This class contains attributes of the rewards gained for doing something in this game.
    """


class Game:
    """
    This class contains attributes of the saved game data.
    """


# Creating the main method used to runt the game.


def main():
    """
    This main method is used to run the game.
    :return: None
    """

    print("Welcome to 'Legendary Creature City Builder' by 'NativeApkDev'.")
    print("This game is an online multiplayer strategy and social-network RPG where the player raises legendary ")
    print("creatures and brings them for multiplayer battles.")


if __name__ == '__main__':
    main()
