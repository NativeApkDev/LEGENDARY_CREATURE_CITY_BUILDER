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
ELEMENT_CHART: list = [
    ["ATTACKING\nELEMENT", "TERRA", "FLAME", "SEA", "NATURE", "ELECTRIC", "ICE", "METAL", "DARK", "LIGHT", "WAR", "PURE",
     "LEGEND", "PRIMAL", "WIND"],
    ["DOUBLE\nDAMAGE", "ELECTRIC\nDARK", "NATURE\nICE", "FLAME\nWAR", "SEA\nLIGHT", "SEA\nMETAL", "NATURE\nWAR",
     "TERRA\nICE", "METAL\nLIGHT", "ELECTRIC\nDARK", "TERRA\nFLAME", "LEGEND", "PRIMAL", "PURE", "WIND"],
    ["HALF\nDAMAGE", "METAL\nWAR", "SEA\nWAR", "NATURE\nELECTRIC", "FLAME\nICE", "TERRA\nLIGHT", "FLAME\nMETAL",
     "ELECTRIC\nDARK", "TERRA", "NATURE", "SEA\nICE", "PRIMAL", "PURE", "LEGEND", "N/A"],
    ["NORMAL\nDAMAGE", "OTHER", "OTHER", "OTHER", "OTHER", "OTHER", "OTHER", "OTHER", "OTHER", "OTHER", "OTHER", "OTHER",
     "OTHER", "OTHER", "OTHER"]
]


# Creating static functions to be used in this game.


def is_number(string: str) -> bool:
    try:
        mpf(string)
        return True
    except ValueError:
        return False


def tabulate_element_chart() -> str:
    return str(tabulate(ELEMENT_CHART, headers='firstrow', tablefmt='fancy_grid'))


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


def get_elemental_damage_multiplier(element1: str, element2: str) -> mpf:
    if element1 == "TERRA":
        return mpf("2") if element2 in ["ELECTRIC, DARK"] else mpf("0.5") if element2 in ["METAL", "WAR"] else mpf("1")
    elif element1 == "FLAME":
        return mpf("2") if element2 in ["NATURE", "ICE"] else mpf("0.5") if element2 in ["SEA", "WAR"] else mpf("1")
    elif element1 == "SEA":
        return mpf("2") if element2 in ["FLAME", "WAR"] else mpf("0.5") if element2 in ["NATURE", "ELECTRIC"] else \
            mpf("1")
    elif element1 == "NATURE":
        return mpf("2") if element2 in ["SEA", "LIGHT"] else mpf("0.5") if element2 in ["FLAME", "ICE"] else mpf("1")
    elif element1 == "ELECTRIC":
        return mpf("2") if element2 in ["SEA", "METAL"] else mpf("0.5") if element2 in ["TERRA", "LIGHT"] else mpf("1")
    elif element1 == "ICE":
        return mpf("2") if element2 in ["NATURE", "WAR"] else mpf("0.5") if element2 in ["FLAME", "METAL"] else mpf("1")
    elif element1 == "METAL":
        return mpf("2") if element2 in ["TERRA", "ICE"] else mpf("0.5") if element2 in ["ELECTRIC", "DARK"] else \
            mpf("1")
    elif element1 == "DARK":
        return mpf("2") if element2 in ["METAL", "LIGHT"] else mpf("0.5") if element2 == "TERRA" else mpf("1")
    elif element1 == "LIGHT":
        return mpf("2") if element2 in ["ELECTRIC", "DARK"] else mpf("0.5") if element2 == "NATURE" else mpf("1")
    elif element1 == "WAR":
        return mpf("2") if element2 in ["TERRA", "FLAME"] else mpf("0.5") if element2 in ["SEA", "ICE"] else mpf("1")
    elif element1 == "PURE":
        return mpf("2") if element2 == "LEGEND" else mpf("0.5") if element2 == "PRIMAL" else mpf("1")
    elif element1 == "LEGEND":
        return mpf("2") if element2 == "PRIMAL" else mpf("0.5") if element2 == "PURE" else mpf("1")
    elif element1 == "PRIMAL":
        return mpf("2") if element2 == "PURE" else mpf("0.5") if element2 == "LEGEND" else mpf("1")
    elif element1 == "WIND":
        return mpf("2") if element2 == "WIND" else mpf("1")
    else:
        return mpf("1")


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

    def __init__(self, name):
        # type: (str) -> None
        self.name: str = name if name in self.POSSIBLE_NAMES else self.POSSIBLE_NAMES[0]

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
        # type: () -> Action
        return copy.deepcopy(self)


class AwakenBonus:
    """
    This class contains attributes of the bonus gained for awakening a legendary creature.
    """

    def __init__(self, max_hp_percentage_up, max_magic_points_percentage_up, attack_power_percentage_up,
                 defense_percentage_up, attack_speed_up, crit_rate_up, crit_damage_up, resistance_up,
                 accuracy_up, new_skill_gained):
        # type: (mpf, mpf, mpf, mpf, mpf, mpf, mpf, mpf, mpf, Skill) -> None
        self.max_hp_percentage_up: mpf = max_hp_percentage_up
        self.max_magic_points_percentage_up: mpf = max_magic_points_percentage_up
        self.attack_power_percentage_up: mpf = attack_power_percentage_up
        self.defense_percentage_up: mpf = defense_percentage_up
        self.attack_speed_up: mpf = attack_speed_up
        self.crit_rate_up: mpf = crit_rate_up
        self.crit_damage_up: mpf = crit_damage_up
        self.resistance_up: mpf = resistance_up
        self.accuracy_up: mpf = accuracy_up
        self.new_skill_gained: Skill = new_skill_gained

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
        # type: () -> AwakenBonus
        return copy.deepcopy(self)


class Battle:
    """
    This class contains attributes of a battle which takes place in this game.
    """

    def __init__(self, team1, team2):
        # type: (Team, Team) -> None
        self.team1: Team = team1
        self.team2: Team = team2
        self.reward: Reward
        self.whose_turn: LegendaryCreature or None = None
        self.winner: Team or None = None

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
        # type: () -> Battle
        return copy.deepcopy(self)


class Arena:
    """
    This class contains attributes of a battle arena in this game. This arena allows players to attack CPU controlled
    opponents.
    """

    def __init__(self, potential_opponents=None):
        # type: (list) -> None
        if potential_opponents is None:
            potential_opponents = []
        self.__potential_opponents: list = potential_opponents   # initial value

    def add_opponent(self, opponent):
        # type: (CPU) -> bool
        if opponent not in self.__potential_opponents:
            self.__potential_opponents.append(opponent)
            return True
        return False

    def remove_opponent(self, opponent):
        # type: (CPU) -> bool
        if opponent in self.__potential_opponents:
            self.__potential_opponents.remove(opponent)
            return True
        return False

    def get_potential_opponents(self):
        # type: () -> list
        return self.__potential_opponents

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


class LiveArena:
    """
    This class contains attributes of a battle arena allowing live battle between two player in this game. In this case,
    players take turn in making moves and the game pauses until the player makes a move.
    """

    def __init__(self, players_in_the_room=None):
        # type: (list) -> None
        if players_in_the_room is None:
            players_in_the_room = []
        self.__players_in_the_room: list = players_in_the_room  # initial value

    def get_players_in_the_room(self):
        # type: () -> list
        return self.__players_in_the_room

    def add_player_to_room(self, player):
        # type: (Player) -> None
        self.__players_in_the_room.append(player)

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

    LEVEL_NUMBER: int = 0

    def __init__(self, stages, reward):
        # type: (list, Reward) -> None
        Level.LEVEL_NUMBER += 1
        self.name: str = "LEVEL " + str(Level.LEVEL_NUMBER)
        self.__stages: list = stages
        self.is_cleared: bool = False
        self.clear_reward: Reward = reward

    def curr_stage(self, stage_number):
        # type: (int) -> Stage or None
        if stage_number < 0 or stage_number >= len(self.__stages):
            return None
        return self.__stages[stage_number]

    def next_stage(self, stage_number):
        # type: (int) -> Stage or None
        if stage_number < -1 or stage_number >= len(self.__stages) - 1:
            return None
        return self.__stages[stage_number + 1]

    def get_stages(self):
        # type: () -> list
        return self.__stages

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
        # type: () -> Level
        return copy.deepcopy(self)


class Stage:
    """
    This class contains attributes of a stage in a level in this game.
    """

    def __init__(self, enemies_list):
        # type: (list) -> None
        self.__enemies_list: list = enemies_list
        self.is_cleared: bool = False

    def get_enemies_list(self):
        # type: () -> list
        return self.__enemies_list

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
        # type: () -> Stage
        return copy.deepcopy(self)


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
        self.live_arena_points: int = 1000
        self.live_arena_wins: int = 0
        self.live_arena_losses: int = 0
        self.battle_team: Team = Team()
        self.item_inventory: ItemInventory = ItemInventory()
        self.legendary_creature_inventory: LegendaryCreatureInventory = LegendaryCreatureInventory()
        self.player_city: PlayerCity = PlayerCity()
        self.__unlocked_levels: list = []  # initial value
        self.__friends: list = []  # initial value
        self.friend_points: int = 0  # initial value

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

    def get_unlocked_levels(self):
        # type: () -> list
        return self.__unlocked_levels

    def get_friends(self):
        # type: () -> list
        return self.__friends

    def add_friend(self, friend):
        # type: (Player) -> None
        self.__friends.append(friend)

    def remove_friend(self, friend):
        # type: (Player) -> bool
        if friend in self.__friends:
            self.__friends.remove(friend)
            return True
        return False

    def send_gift(self, friend):
        # type: (Player) -> bool
        if friend not in self.__friends:
            return False

        random_reward: Reward = Reward()  # TODO: generate random reward
        self.friend_points += 10
        # TODO: ensure 'friend' receives the reward

    def add_unlocked_level(self):
        # type: () -> None
        new_level_number: int = Level.LEVEL_NUMBER + 1
        new_level: Level = Level([], Reward())  # TODO: code to be updated later
        self.__unlocked_levels.append(new_level)

    def clone(self):
        # type: () -> Player
        return copy.deepcopy(self)


class CPU(Player):
    """
    This class contains attributes of a CPU controlled player.
    """

    def __init__(self, name):
        # type: (str) -> None
        Player.__init__(self, name)
        self.currently_available: bool = False
        self.next_available_time: datetime or None = None
        self.times_beaten: int = 0  # initial value


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

    def clone(self):
        # type: () -> PlayerCity
        return copy.deepcopy(self)


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

    def clone(self):
        # type: () -> CityTile
        return copy.deepcopy(self)


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

    def add_legendary_creature(self, legendary_creature):
        # type: (LegendaryCreature) -> bool
        if len(self.__legendary_creatures) < self.MAX_LEGENDARY_CREATURES:
            self.__legendary_creatures.append(legendary_creature)
            self.set_leader()
            return True
        return False

    def remove_legendary_creature(self, legendary_creature):
        # type: (LegendaryCreature) -> bool
        if legendary_creature in self.__legendary_creatures:
            self.__legendary_creatures.remove(legendary_creature)
            self.set_leader()
            return True
        return False

    def get_legendary_creatures(self):
        # type: () -> list
        return self.__legendary_creatures

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

    def __init__(self):
        # type: () -> None
        self.__legendary_creatures: list = []  # initial value

    def add_legendary_creature(self, legendary_creature):
        # type: (LegendaryCreature) -> None
        self.__legendary_creatures.append(legendary_creature)

    def remove_legendary_creature(self, legendary_creature):
        # type: (LegendaryCreature) -> bool
        if legendary_creature in self.__legendary_creatures:
            self.__legendary_creatures.remove(legendary_creature)
            return True
        return False

    def get_legendary_creatures(self):
        # type: () -> list
        return self.__legendary_creatures

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
        # type: () -> LegendaryCreatureInventory
        return copy.deepcopy(self)


class ItemInventory:
    """
    This class contains attributes of an inventory containing items.
    """

    def __init__(self):
        # type: () -> None
        self.__items: list = []  # initial value

    def add_item(self, item):
        # type: (Item) -> None
        self.__items.append(item)

    def remove_item(self, item):
        # type: (Item) -> bool
        if item in self.__items:
            self.__items.remove(item)
            return True
        return False

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

    def clone(self):
        # type: () -> ItemInventory
        return copy.deepcopy(self)


class LegendaryCreature:
    """
    This class contains attributes of a legendary creature in this game.
    """

    MIN_RATING: int = 1
    MAX_RATING: int = 6
    MIN_CRIT_RATE: mpf = mpf("0.15")
    MIN_CRIT_DAMAGE: mpf = mpf("1.5")
    MIN_RESISTANCE: mpf = mpf("0.15")
    MAX_RESISTANCE: mpf = mpf("1")
    MIN_ACCURACY: mpf = mpf("0")
    MAX_ACCURACY: mpf = mpf("1")
    MIN_ATTACK_GAUGE: mpf = mpf("0")
    FULL_ATTACK_GAUGE: mpf = mpf("1")
    MIN_EXTRA_TURN_CHANCE: mpf = mpf("0")
    MAX_EXTRA_TURN_CHANCE: mpf = mpf("0.5")
    MIN_COUNTERATTACK_CHANCE: mpf = mpf("0")
    MAX_COUNTERATTACK_CHANCE: mpf = mpf("1")
    MIN_REFLECTED_DAMAGE_PERCENTAGE: mpf = mpf("0")
    MIN_LIFE_DRAIN_PERCENTAGE: mpf = mpf("0")
    MIN_CRIT_RESIST: mpf = mpf("0")
    MAX_CRIT_RESIST: mpf = mpf("1")
    MIN_BENEFICIAL_EFFECTS: int = 0
    MAX_BENEFICIAL_EFFECTS: int = 10
    MIN_HARMFUL_EFFECTS: int = 0
    MAX_HARMFUL_EFFECTS: int = 10
    POTENTIAL_ELEMENTS: list = ["TERRA", "FLAME", "SEA", "NATURE", "ELECTRIC", "ICE", "METAL", "DARK", "LIGHT", "WAR",
                                "PURE", "LEGEND", "PRIMAL", "WIND", "BEAUTY", "MAGIC", "CHAOS", "HAPPY", "DREAM",
                                "SOUL"]
    DEFAULT_MAX_HP_PERCENTAGE_UP: mpf = mpf("0")
    DEFAULT_MAX_MAGIC_POINTS_PERCENTAGE_UP: mpf = mpf("0")
    DEFAULT_ATTACK_POWER_PERCENTAGE_UP: mpf = mpf("0")
    DEFAULT_ATTACK_SPEED_PERCENTAGE_UP: mpf = mpf("0")
    DEFAULT_DEFENSE_PERCENTAGE_UP: mpf = mpf("0")
    DEFAULT_CRIT_DAMAGE_UP: mpf = mpf("0")

    def __init__(self, name, main_element, rating, max_hp, max_magic_points, attack_power, defense, attack_speed, skills,
                 awaken_bonus):
        # type: (str, str, int, mpf, mpf, mpf, mpf, mpf, list, AwakenBonus) -> None
        self.legendary_creature_id: str = str(uuid.uuid1())  # generating random legendary creature ID
        self.name: str = name
        self.__elements: list = [main_element if main_element in self.POTENTIAL_ELEMENTS else
                                 self.POTENTIAL_ELEMENTS[0]]  # a list of elements the legendary creature has. The main
        # (i.e., first) element will be the element considered as the defending element of this legendary creature.
        self.rating: int = rating if self.MIN_RATING <= rating <= self.MAX_RATING else self.MIN_RATING
        self.level: int = 1  # initial value
        self.max_level: int = 10 * triangular(self.rating) if self.rating < self.MAX_RATING else float('inf')
        self.exp: mpf = mpf("0")
        self.required_exp: mpf = mpf("1e6")
        self.exp_per_second: mpf = mpf("0")
        self.player_gold_per_second: mpf = mpf("0")
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
        self.extra_turn_chance: mpf = self.MIN_EXTRA_TURN_CHANCE
        self.counterattack_chance: mpf = self.MIN_COUNTERATTACK_CHANCE
        self.reflected_damage_percentage: mpf = self.MIN_REFLECTED_DAMAGE_PERCENTAGE
        self.life_drain_percentage: mpf = self.MIN_LIFE_DRAIN_PERCENTAGE
        self.crit_resist: mpf = self.MIN_CRIT_RESIST
        self.stun_rate: mpf = mpf("0")
        self.__beneficial_effects: list = []
        self.__harmful_effects: list = []
        self.__skills: list = skills
        self.awaken_bonus: AwakenBonus = awaken_bonus
        self.__runes: dict = {}  # initial value
        self.max_hp_percentage_up: mpf = self.DEFAULT_MAX_HP_PERCENTAGE_UP
        self.max_magic_points_percentage_up: mpf = self.DEFAULT_MAX_MAGIC_POINTS_PERCENTAGE_UP
        self.attack_power_percentage_up: mpf = self.DEFAULT_ATTACK_POWER_PERCENTAGE_UP
        self.attack_power_percentage_down: mpf = mpf("0")
        self.attack_speed_percentage_up: mpf = self.DEFAULT_ATTACK_SPEED_PERCENTAGE_UP
        self.attack_speed_percentage_down: mpf = mpf("0")
        self.defense_percentage_up: mpf = self.DEFAULT_DEFENSE_PERCENTAGE_UP
        self.defense_percentage_down: mpf = mpf("0")
        self.crit_rate_up: mpf = mpf("0")
        self.crit_damage_up: mpf = self.DEFAULT_CRIT_DAMAGE_UP
        self.resistance_up: mpf = mpf("0")
        self.accuracy_up: mpf = mpf("0")
        self.extra_turn_chance_up: mpf = mpf("0")
        self.counterattack_chance_up: mpf = mpf("0")
        self.reflected_damage_percentage_up: mpf = mpf("0")
        self.life_drain_percentage_up: mpf = mpf("0")
        self.crit_resist_up: mpf = mpf("0")
        self.shield_percentage: mpf = mpf("0")
        self.damage_percentage_per_turn: mpf = mpf("0")
        self.heal_percentage_per_turn: mpf = mpf("0")
        self.has_awakened: bool = False
        self.can_move: bool = True
        self.can_be_healed: bool = True
        self.can_receive_beneficial_effect: bool = True
        self.can_receive_damage: bool = True
        self.can_receive_harmful_effect: bool = True
        self.can_die: bool = True
        self.damage_received_percentage_up: mpf = mpf("0")
        self.attack_gauge: mpf = self.MIN_ATTACK_GAUGE
        self.can_use_skills_with_cooltime: bool = True
        self.can_use_passive_skills: bool = True
        self.passive_skills_activated: bool = False
        self.leader_skills_activated: bool = False
        self.placed_in_training_area: bool = False
        self.corresponding_team: Team = Team()

    def restore(self):
        # type: () -> None
        self.curr_hp = self.max_hp * (1 + self.max_hp_percentage_up / 100)
        self.curr_magic_points = self.max_magic_points * (1 + self.max_magic_points_percentage_up / 100)
        self.max_hp_percentage_up = self.DEFAULT_MAX_HP_PERCENTAGE_UP
        self.max_magic_points_percentage_up = self.DEFAULT_MAX_MAGIC_POINTS_PERCENTAGE_UP
        self.attack_power_percentage_up = self.DEFAULT_ATTACK_POWER_PERCENTAGE_UP
        self.attack_power_percentage_down = mpf("0")
        self.attack_speed_percentage_up = self.DEFAULT_ATTACK_SPEED_PERCENTAGE_UP
        self.attack_speed_percentage_down = mpf("0")
        self.defense_percentage_up = self.DEFAULT_DEFENSE_PERCENTAGE_UP
        self.defense_percentage_down = mpf("0")
        self.crit_rate_up = mpf("0")
        self.crit_damage_up = self.DEFAULT_CRIT_DAMAGE_UP
        self.resistance_up = mpf("0")
        self.accuracy_up = mpf("0")
        self.extra_turn_chance_up = mpf("0")
        self.counterattack_chance_up = mpf("0")
        self.reflected_damage_percentage_up = mpf("0")
        self.life_drain_percentage_up = mpf("0")
        self.crit_resist_up = mpf("0")
        self.shield_percentage = mpf("0")
        self.damage_percentage_per_turn = mpf("0")
        self.heal_percentage_per_turn = mpf("0")
        self.can_move = True
        self.can_be_healed = True
        self.can_receive_beneficial_effect = True
        self.can_receive_damage = True
        self.can_receive_harmful_effect = True
        self.can_die = True
        self.damage_received_percentage_up = mpf("0")
        self.__beneficial_effects = []
        self.__harmful_effects = []
        self.attack_gauge: mpf = self.MIN_ATTACK_GAUGE
        self.can_use_skills_with_cooltime: bool = True
        self.can_use_passive_skills: bool = True

    def get_elements(self):
        # type: () -> list
        return self.__elements

    def add_element(self, element):
        # type: (str) -> None
        self.__elements.append(element)

    def get_beneficial_effects(self):
        # type: () -> list
        return self.__beneficial_effects

    def get_harmful_effects(self):
        # type: () -> list
        return self.__harmful_effects

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


class ItemShop:
    """
    This class contains attributes of a shop selling items.
    """


class BuildingShop:
    """
    This class contains attributes of a shop selling buildings.
    """


class Reward:
    """
    This class contains attributes of the rewards gained for doing something in this game.
    """


class Game:
    """
    This class contains attributes of the saved game data.
    """

    def __init__(self, player_data, item_shop, building_shop, battle_arena):
        # type: (Player, ItemShop, BuildingShop, Arena) -> None
        self.player_data: Player = player_data
        self.item_shop: ItemShop = item_shop
        self.building_shop: BuildingShop = building_shop
        self.battle_arena: Arena = battle_arena

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


########################################### VERSION 2 FEATURES (DRAFT CODE) ###########################################


class Guild:
    """
    This class contains attributes of a guild where players can team-up for team battles in this game.
    """

    MAX_PLAYERS: int = 30

    def __init__(self, name, players=None):
        # type: (str, list) -> None
        self.guild_id: str = str(uuid.uuid1())  # generating random guild ID
        if players is None:
            players = []
        self.name: str = name
        self.__players: list = players

    def get_players(self):
        # type: () -> list
        return self.__players

    def add_player(self, player):
        # type: (Player) -> bool
        if len(self.__players) < self.MAX_PLAYERS:
            self.__players.append(player)
            return True
        return False

    def remove_player(self, player):
        # type: (Player) -> bool
        if player in self.__players:
            self.__players.remove(player)
            return True
        return False

    def clone(self):
        # type: () -> Guild
        return copy.deepcopy(self)

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


class GuildBattle:
    """
    This class contains attributes of a battle between two guilds
    """

    def __init__(self, guild1, guild2):
        # type: (Guild, Guild) -> None
        self.guild1: Guild = guild1
        self.guild2: Guild = guild2

    def clone(self):
        # type: () -> GuildBattle
        return copy.deepcopy(self)

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


class Conversation:
    """
    This class contains attribute of a chat conversation between one player and another.
    """

    def __init__(self, player1, player2):
        # type: (Player, Player) -> None
        self.player1: Player = player1
        self.player2: Player = player2
        self.__messages: list = []  # initial value

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

    def get_messages(self):
        # type: () -> list
        return self.__messages

    def add_message(self, message):
        # type: (Message) -> bool
        if message.sender not in [self.player1, self.player2]:
            return False
        self.__messages.append(message)
        return True

    def clone(self):
        # type: () -> Conversation
        return copy.deepcopy(self)


class Message:
    """
    This class contains attributes of a message sent by a player in a conversation.
    """

    def __init__(self, sender, contents):
        # type: (Player, str) -> None
        self.time_sent: datetime = datetime.now()
        self.sender: Player = sender
        self.contents: str = contents

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
        # type: () -> Message
        return copy.deepcopy(self)


########################################### VERSION 2 FEATURES (DRAFT CODE) ###########################################


# Creating the main method used to runt the game.


def main() -> int:
    """
    This main method is used to run the game.
    :return: an integer
    """

    print("Welcome to 'Legendary Creature City Builder' by 'NativeApkDev'.")
    print("This game is an online multiplayer strategy and social-network RPG where the player raises legendary ")
    print("creatures and brings them for multiplayer battles.")
    print("Below is the element chart in 'Legendary Creature City Builder'.\n")
    print(str(tabulate_element_chart()) + "\n")
    print("The following elements do not have any elemental strengths nor weaknesses.")
    print("This is because they are ancient world elements. In this case, these elements will always ")
    print("be dealt with normal damage.\n")
    ancient_world_elements: list = ["BEAUTY", "MAGIC", "CHAOS", "HAPPY", "DREAM", "SOUL"]
    for i in range(0, len(ancient_world_elements)):
        print(str(i + 1) + ". " + str(ancient_world_elements[i]))

    # Initialising important variables to be used throughout the main function.
    # 1. The item shop
    item_shop: ItemShop = ItemShop()

    # 2. The building shop
    building_shop: BuildingShop = BuildingShop()

    # 3. The battle arena
    battle_arena: Arena = Arena()

    # Initialising variable for the saved game data
    # Asking the user to enter his/her name to check whether saved game data exists or not
    player_name: str = input("Please enter your name: ")
    file_name: str = "SAVED ANCIENT INVASION GAME DATA - " + str(player_name).upper()

    new_game: Game
    try:
        new_game = load_game_data(file_name)

        # Clearing up the command line window
        clear()

        print("Current game progress:\n", str(new_game))
    except FileNotFoundError:
        # Clearing up the command line window
        clear()

        print("Sorry! No saved game data with player name '" + str(player_name) + "' is available!")
        name: str = input("Please enter your name: ")
        player_data: Player = Player(name)
        new_game = Game(player_data, item_shop, building_shop, battle_arena)

    # Getting the current date and time
    old_now: datetime = datetime.now()
    print("Enter 'Y' for yes.")
    print("Enter anything else for no.")
    continue_playing: str = input("Do you want to continue playing 'Legendary Creature City Builder'? ")
    while continue_playing == "Y":
        # Clearing up the command line window
        clear()

        # Updating the old time
        new_now: datetime = datetime.now()
        time_difference = new_now - old_now
        seconds: int = time_difference.seconds
        old_now = new_now

        print("Enter 'Y' for yes.")
        print("Enter anything else for no.")
        continue_playing = input("Do you want to continue playing 'Legendary Creature City Builder'? ")

    # Saving game data and quitting the game.
    save_game_data(new_game, file_name)
    return 0


if __name__ == '__main__':
    main()
