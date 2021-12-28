"""
This file contains code for the client side of the game "Legendary Creature City Builder".
Author: NativeApkDev

The game "Legendary Creature City Builder" is inspired by "Dragon City"
(https://play.google.com/store/apps/details?id=es.socialpoint.DragonCity&hl=en_NZ&gl=US) and "Monster Legends"
(https://play.google.com/store/apps/details?id=es.socialpoint.MonsterLegends&hl=en_NZ&gl=US).
"""

# Game version: 1


# Importing necessary libraries
import socket
import sys
import uuid
import pickle
import copy
import random
from datetime import datetime, timedelta
import os
from functools import reduce

from mpmath import mp, mpf
from tabulate import tabulate

mp.pretty = True

# Creating static variables to be used throughout the game.


LETTERS: str = "abcdefghijklmnopqrstuvwxyz"
ELEMENT_CHART: list = [
    ["ATTACKING\nELEMENT", "TERRA", "FLAME", "SEA", "NATURE", "ELECTRIC", "ICE", "METAL", "DARK", "LIGHT", "WAR",
     "PURE",
     "LEGEND", "PRIMAL", "WIND"],
    ["DOUBLE\nDAMAGE", "ELECTRIC\nDARK", "NATURE\nICE", "FLAME\nWAR", "SEA\nLIGHT", "SEA\nMETAL", "NATURE\nWAR",
     "TERRA\nICE", "METAL\nLIGHT", "ELECTRIC\nDARK", "TERRA\nFLAME", "LEGEND", "PRIMAL", "PURE", "WIND"],
    ["HALF\nDAMAGE", "METAL\nWAR", "SEA\nWAR", "NATURE\nELECTRIC", "FLAME\nICE", "TERRA\nLIGHT", "FLAME\nMETAL",
     "ELECTRIC\nDARK", "TERRA", "NATURE", "SEA\nICE", "PRIMAL", "PURE", "LEGEND", "N/A"],
    ["NORMAL\nDAMAGE", "OTHER", "OTHER", "OTHER", "OTHER", "OTHER", "OTHER", "OTHER", "OTHER", "OTHER", "OTHER",
     "OTHER",
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


def generate_random_legendary_creature(element):
    # type: (str) -> LegendaryCreature
    name: str = generate_random_name()
    main_element: str = element
    rating: int = LegendaryCreature.MIN_RATING
    max_hp: mpf = mpf(random.randint(45000, 55000))
    max_magic_points: mpf = mpf(random.randint(45000, 55000))
    attack_power: mpf = mpf(random.randint(8500, 9500))
    defense: mpf = mpf(random.randint(8500, 9500))
    attack_speed: mpf = mpf(random.randint(100, 125))
    skills: list = [
        ActiveSkill("SINGLE-TARGET ATTACK SKILL #1", "Normal Single-Target Attack Skill", "ATTACK", False,
                    mpf("1e2") * random.randint(8, 14),
                    2, DamageMultiplier(
                random.randint(1, 3) * mpf("0.01"),
                random.randint(1, 3) * mpf("0.01"),
                mpf(3 + random.random() * 2),
                mpf(random.random()),
                mpf(3 + random.random() * 2),
                mpf(random.random()),
                random.randint(1, 3) * mpf("0.01"),
                random.randint(1, 3) * mpf("0.01"),
                mpf("0.5"),
                mpf("0.25"),
                mpf("0.05"),
                mpf("0.05"),
                mpf("0.05")
            ), [], [], mpf("0"), mpf("0"), mpf("0"), random.random() < 0.1, random.random() < 0.1,
                    random.random() < 0.1),
        ActiveSkill("SINGLE-TARGET ATTACK SKILL #2", "Strong Single-Target Attack Skill", "ATTACK", False,
                    mpf("1e9") * random.randint(8, 14),
                    4, DamageMultiplier(
                random.randint(1, 3) * mpf("0.03"),
                random.randint(1, 3) * mpf("0.03"),
                mpf(9 + random.random() * 6),
                mpf(2 * random.random()),
                mpf(9 + random.random() * 6),
                mpf(2 * random.random()),
                random.randint(1, 3) * mpf("0.03"),
                random.randint(1, 3) * mpf("0.03"),
                mpf("1.5"),
                mpf("0.75"),
                mpf("0.1"),
                mpf("0.1"),
                mpf("0.1")
            ), [BeneficialEffect(
                BeneficialEffect.POSSIBLE_NAMES[random.randint(0, len(BeneficialEffect.POSSIBLE_NAMES) - 1)], 2
            )], [HarmfulEffect(
                HarmfulEffect.POSSIBLE_NAMES[random.randint(0, len(HarmfulEffect.POSSIBLE_NAMES) - 1)], 2
            )], mpf("0.1"), mpf("0.1"), mpf("0"), random.random() < 0.3, random.random() < 0.3,
                    random.random() < 0.3),
        ActiveSkill("SINGLE-TARGET ATTACK SKILL #3", "Ultimate Single-Target Attack Skill", "ATTACK", False,
                    mpf("1e29") * random.randint(8, 14),
                    8, DamageMultiplier(
                random.randint(1, 3) * mpf("0.06"),
                random.randint(1, 3) * mpf("0.06"),
                mpf(27 + random.random() * 10),
                mpf(6 * random.random()),
                mpf(27 + random.random() * 10),
                mpf(6 * random.random()),
                random.randint(1, 3) * mpf("0.06"),
                random.randint(1, 3) * mpf("0.06"),
                mpf("4.5"),
                mpf("2.25"),
                mpf("0.3"),
                mpf("0.3"),
                mpf("0.3")
            ), [BeneficialEffect(
                BeneficialEffect.POSSIBLE_NAMES[random.randint(0, len(BeneficialEffect.POSSIBLE_NAMES) - 1)], 2
            )], [HarmfulEffect(
                HarmfulEffect.POSSIBLE_NAMES[random.randint(0, len(HarmfulEffect.POSSIBLE_NAMES) - 1)], 2
            )], mpf("0.25"), mpf("0.25"), mpf("0"), random.random() < 0.5, random.random() < 0.5,
                    random.random() < 0.5),
        ActiveSkill("MULTI-TARGET ATTACK SKILL #1", "Normal Multi-Target Attack Skill", "ATTACK", True,
                    mpf("1e2") * random.randint(8, 14),
                    2, DamageMultiplier(
                multiplier_to_self_attack_power=mpf("0.5") + mpf("0.1") * random.randint(2, 5)
            ), [], [], mpf("0"), mpf("0"), mpf("0"), random.random() < 0.1, random.random() < 0.1,
                    random.random() < 0.1),
        ActiveSkill("MULTI-TARGET ATTACK SKILL #2", "Strong Multi-Target Attack Skill", "ATTACK", True,
                    mpf("1e9") * random.randint(8, 14),
                    2, DamageMultiplier(
                multiplier_to_self_attack_power=mpf("2") + mpf("0.1") * random.randint(2, 5)
            ), [BeneficialEffect(
                BeneficialEffect.POSSIBLE_NAMES[random.randint(0, len(BeneficialEffect.POSSIBLE_NAMES) - 1)], 2
            )], [HarmfulEffect(
                HarmfulEffect.POSSIBLE_NAMES[random.randint(0, len(HarmfulEffect.POSSIBLE_NAMES) - 1)], 2
            )], mpf("0.05"), mpf("0.05"), mpf("0"), random.random() < 0.3, random.random() < 0.3,
                    random.random() < 0.3),
        ActiveSkill("MULTI-TARGET ATTACK SKILL #3", "Ultimate Multi-Target Attack Skill", "ATTACK", True,
                    mpf("1e29") * random.randint(8, 14),
                    2, DamageMultiplier(
                multiplier_to_self_attack_power=mpf("6.1") + mpf("0.1") * random.randint(2, 5),
                multiplier_to_enemy_max_hp=mpf("0.03") * random.randint(1, 3)
            ), [BeneficialEffect(
                BeneficialEffect.POSSIBLE_NAMES[random.randint(0, len(BeneficialEffect.POSSIBLE_NAMES) - 1)], 2
            )], [HarmfulEffect(
                HarmfulEffect.POSSIBLE_NAMES[random.randint(0, len(HarmfulEffect.POSSIBLE_NAMES) - 1)], 2
            )], mpf("0.15"), mpf("0.15"), mpf("0"), random.random() < 0.5, random.random() < 0.5,
                    random.random() < 0.5),
        ActiveSkill("HEAL SKILL #1", "First Heal Skill", "HEAL", True,
                    mpf("1e2") * random.randint(8, 14),
                    2, DamageMultiplier(), [], [],
                    mpf("0"), mpf("0"),
                    mpf("1e2") * random.randint(18, 24),
                    False, False, False),
        ActiveSkill("HEAL SKILL #2", "Better Heal Skill", "HEAL", True,
                    mpf("1e9") * random.randint(8, 14),
                    4, DamageMultiplier(), [], [],
                    mpf("0"), mpf("0"),
                    mpf("1e11") * random.randint(18, 24),
                    False, False, False),
        ActiveSkill("HEAL SKILL #3", "Ultimate Heal Skill", "HEAL", True,
                    mpf("1e29") * random.randint(8, 14),
                    8, DamageMultiplier(), [], [],
                    mpf("0"), mpf("0"),
                    mpf("1e35") * random.randint(18, 24),
                    False, False, False),
        PassiveSkill("EXTRA TURN PASSIVE SKILL", "Increase player's extra turn change by 15%.",
                     PassiveSkillEffect(extra_turn_chance_up=mpf("0.15"))),
        LeaderSkill("ATTACK LEADER SKILL", "Increase all allies' attack power by 20%.", mpf("0"),
                    LeaderSkillEffect(attack_power_percentage_up=mpf("20")))
    ]

    new_skill_gained: ActiveSkill = ActiveSkill("SINGLE-TARGET ATTACK SKILL #4", "Extreme Single-Target Attack Skill",
                                                "ATTACK", False,
                                                mpf("1e89") * random.randint(8, 14),
                                                8, DamageMultiplier(
            random.randint(1, 3) * mpf("0.15"),
            random.randint(1, 3) * mpf("0.15"),
            mpf(90 + random.random() * 15),
            mpf(15 * random.random()),
            mpf(90 + random.random() * 15),
            mpf(15 * random.random()),
            random.randint(1, 3) * mpf("0.15"),
            random.randint(1, 3) * mpf("0.15"),
            mpf("13.5"),
            mpf("6.75"),
            mpf("0.9"),
            mpf("0.9"),
            mpf("0.9")
        ), [BeneficialEffect(
            BeneficialEffect.POSSIBLE_NAMES[random.randint(0, len(BeneficialEffect.POSSIBLE_NAMES) - 1)], 2
        )], [HarmfulEffect(
            HarmfulEffect.POSSIBLE_NAMES[random.randint(0, len(HarmfulEffect.POSSIBLE_NAMES) - 1)], 2
        )], mpf("0.5"), mpf("0.5"), mpf("0"), random.random() < 0.9, random.random() < 0.9,
                                                random.random() < 0.9)

    awaken_bonus: AwakenBonus = AwakenBonus(mpf(random.randint(115, 135)), mpf(random.randint(115, 135)),
                                            mpf(random.randint(115, 135)), mpf(random.randint(115, 135)),
                                            mpf(random.randint(0, 15)),
                                            mpf(0.01 * random.randint(0, 15)), mpf(0.01 * random.randint(0, 15)),
                                            mpf(0.01 * random.randint(0, 15)), mpf(0.01 * random.randint(0, 15)),
                                            new_skill_gained
                                            )
    new_legendary_creature: LegendaryCreature = LegendaryCreature(name, main_element, rating, max_hp, max_magic_points,
                                                                  attack_power, defense, attack_speed, skills,
                                                                  awaken_bonus)
    return new_legendary_creature


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


def resistance_accuracy_rule(accuracy: mpf, resistance: mpf) -> mpf:
    if resistance - accuracy <= mpf("0.15"):
        return mpf("0.15")
    else:
        return resistance - accuracy


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


class Minigame:
    """
    This class contains attributes of a minigame in this game.
    """

    POSSIBLE_NAMES: list = ["BOX EATS PLANTS", "MATCH WORD PUZZLE", "MATCH-3 GAME"]

    def __init__(self, name):
        # type: (str) -> None
        self.name: str = name if name in self.POSSIBLE_NAMES else self.POSSIBLE_NAMES[0]
        self.already_played: bool = False

    def reset(self):
        # type: () -> bool
        time_now: datetime = datetime.now()
        if self.already_played and time_now.hour > 0:
            self.already_played = False
            return True
        return False

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
        # type: () -> Minigame
        return copy.deepcopy(self)


###########################################
# BOX EATS PLANTS
###########################################


class BoxEatsPlantsBoard:
    """
    This class contains attributes of a board in the game "Box Eats Plants".
    """

    BOARD_WIDTH: int = 10
    BOARD_HEIGHT: int = 10

    def __init__(self):
        # type: () -> None
        self.__tiles: list = []  # initial value
        for i in range(self.BOARD_HEIGHT):
            new: list = []  # initial value
            for j in range(self.BOARD_WIDTH):
                new.append(BoxEatsPlantsTile())

            self.__tiles.append(new)

    def num_plants(self):
        # type: () -> int
        plants: int = 0  # initial value
        for y in range(self.BOARD_HEIGHT):
            for x in range(self.BOARD_WIDTH):
                curr_tile: BoxEatsPlantsTile = self.get_tile_at(x, y)
                if isinstance(curr_tile.plant, Plant):
                    plants += 1

        return plants

    def num_rocks(self):
        # type: () -> int
        rocks: int = 0  # initial value
        for y in range(self.BOARD_HEIGHT):
            for x in range(self.BOARD_WIDTH):
                curr_tile: BoxEatsPlantsTile = self.get_tile_at(x, y)
                if isinstance(curr_tile.rock, Rock):
                    rocks += 1

        return rocks

    def num_boxes(self):
        # type: () -> int
        boxes: int = 0  # initial value
        for y in range(self.BOARD_HEIGHT):
            for x in range(self.BOARD_WIDTH):
                curr_tile: BoxEatsPlantsTile = self.get_tile_at(x, y)
                if isinstance(curr_tile.box, Box):
                    boxes += 1

        return boxes

    def spawn_plant(self):
        # type: () -> Plant
        plant_x: int = random.randint(0, self.BOARD_WIDTH - 1)
        plant_y: int = random.randint(0, self.BOARD_HEIGHT - 1)
        plant_tile: BoxEatsPlantsTile = self.__tiles[plant_y][plant_x]
        while plant_tile.plant is not None:
            plant_x = random.randint(0, self.BOARD_WIDTH - 1)
            plant_y = random.randint(0, self.BOARD_HEIGHT - 1)
            plant_tile = self.__tiles[plant_y][plant_x]

        plant: Plant = Plant(plant_x, plant_y)
        plant_tile.add_plant(plant)
        return plant

    def spawn_rock(self):
        # type: () -> Rock
        rock_x: int = random.randint(0, self.BOARD_WIDTH - 1)
        rock_y: int = random.randint(0, self.BOARD_HEIGHT - 1)
        rock_tile: BoxEatsPlantsTile = self.__tiles[rock_y][rock_x]
        while rock_tile.rock is not None:
            rock_x = random.randint(0, self.BOARD_WIDTH - 1)
            rock_y = random.randint(0, self.BOARD_HEIGHT - 1)
            rock_tile = self.__tiles[rock_y][rock_x]

        rock: Rock = Rock(rock_x, rock_y)
        rock_tile.add_rock(rock)
        return rock

    def spawn_box(self):
        # type: () -> Box
        box_x: int = random.randint(0, self.BOARD_WIDTH - 1)
        box_y: int = random.randint(0, self.BOARD_HEIGHT - 1)
        box_tile: BoxEatsPlantsTile = self.__tiles[box_y][box_x]
        while box_tile.plant is not None or box_tile.rock is not None:
            box_x = random.randint(0, self.BOARD_WIDTH - 1)
            box_y = random.randint(0, self.BOARD_HEIGHT - 1)
            box_tile = self.__tiles[box_y][box_x]
        box: Box = Box(box_x, box_y)
        box_tile.add_box(box)
        return box

    def get_tile_at(self, x, y):
        # type: (int, int) -> BoxEatsPlantsTile or None
        if x < 0 or x >= self.BOARD_WIDTH or y < 0 or y >= self.BOARD_HEIGHT:
            return None
        return self.__tiles[y][x]

    def get_tiles(self):
        # type: () -> list
        return self.__tiles

    def __str__(self):
        # type: () -> str
        return str(tabulate(self.__tiles, tablefmt='fancy_grid'))

    def clone(self):
        # type: () -> BoxEatsPlantsBoard
        return copy.deepcopy(self)


class Box:
    """
    This class contains attributes of a box in the game "Box Eats Plants".
    """

    def __init__(self, x, y):
        # type: (int, int) -> None
        self.name: str = "BOX"
        self.x: int = x
        self.y: int = y

    def move_up(self, board):
        # type: (BoxEatsPlantsBoard) -> bool
        if self.y > 0:
            old_tile: BoxEatsPlantsTile = board.get_tile_at(self.x, self.y)
            old_tile.remove_box()
            self.y -= 1
            new_tile: BoxEatsPlantsTile = board.get_tile_at(self.x, self.y)
            new_tile.add_box(self)
            return True
        return False

    def move_down(self, board):
        # type: (BoxEatsPlantsBoard) -> bool
        if self.y < board.BOARD_HEIGHT - 1:
            old_tile: BoxEatsPlantsTile = board.get_tile_at(self.x, self.y)
            old_tile.remove_box()
            self.y += 1
            new_tile: BoxEatsPlantsTile = board.get_tile_at(self.x, self.y)
            new_tile.add_box(self)
            return True
        return False

    def move_left(self, board):
        # type: (BoxEatsPlantsBoard) -> bool
        if self.x > 0:
            old_tile: BoxEatsPlantsTile = board.get_tile_at(self.x, self.y)
            old_tile.remove_box()
            self.x -= 1
            new_tile: BoxEatsPlantsTile = board.get_tile_at(self.x, self.y)
            new_tile.add_box(self)
            return True
        return False

    def move_right(self, board):
        # type: (BoxEatsPlantsBoard) -> bool
        if self.x < board.BOARD_WIDTH - 1:
            old_tile: BoxEatsPlantsTile = board.get_tile_at(self.x, self.y)
            old_tile.remove_box()
            self.x += 1
            new_tile: BoxEatsPlantsTile = board.get_tile_at(self.x, self.y)
            new_tile.add_box(self)
            return True
        return False

    def __str__(self):
        # type: () -> str
        return str(self.name)

    def clone(self):
        # type: () -> Box
        return copy.deepcopy(self)


class Plant:
    """
    This class contains attributes of a plant in the game "Box Eats Plants".
    """

    def __init__(self, x, y):
        # type: (int, int) -> None
        self.name: str = "PLANT"
        self.x: int = x
        self.y: int = y

    def move_up(self, board):
        # type: (BoxEatsPlantsBoard) -> bool
        if self.y > 0:
            old_tile: BoxEatsPlantsTile = board.get_tile_at(self.x, self.y)
            old_tile.remove_plant()
            self.y -= 1
            new_tile: BoxEatsPlantsTile = board.get_tile_at(self.x, self.y)
            new_tile.add_plant(self)
            return True
        return False

    def move_down(self, board):
        # type: (BoxEatsPlantsBoard) -> bool
        if self.y < board.BOARD_HEIGHT - 1:
            old_tile: BoxEatsPlantsTile = board.get_tile_at(self.x, self.y)
            old_tile.remove_plant()
            self.y += 1
            new_tile: BoxEatsPlantsTile = board.get_tile_at(self.x, self.y)
            new_tile.add_plant(self)
            return True
        return False

    def move_left(self, board):
        # type: (BoxEatsPlantsBoard) -> bool
        if self.x > 0:
            old_tile: BoxEatsPlantsTile = board.get_tile_at(self.x, self.y)
            old_tile.remove_plant()
            self.x -= 1
            new_tile: BoxEatsPlantsTile = board.get_tile_at(self.x, self.y)
            new_tile.add_plant(self)
            return True
        return False

    def move_right(self, board):
        # type: (BoxEatsPlantsBoard) -> bool
        if self.x < board.BOARD_WIDTH - 1:
            old_tile: BoxEatsPlantsTile = board.get_tile_at(self.x, self.y)
            old_tile.remove_plant()
            self.x += 1
            new_tile: BoxEatsPlantsTile = board.get_tile_at(self.x, self.y)
            new_tile.add_plant(self)
            return True
        return False

    def __str__(self):
        # type: () -> str
        return str(self.name)

    def clone(self):
        # type: () -> Plant
        return copy.deepcopy(self)


class Rock:
    """
    This class contains attributes of a rock in the game "Box Eats Plants".
    """

    def __init__(self, x, y):
        # type: (int, int) -> None
        self.name: str = "ROCK"
        self.x: int = x
        self.y: int = y

    def move_up(self, board):
        # type: (BoxEatsPlantsBoard) -> bool
        if self.y > 0:
            old_tile: BoxEatsPlantsTile = board.get_tile_at(self.x, self.y)
            old_tile.remove_rock()
            self.y -= 1
            new_tile: BoxEatsPlantsTile = board.get_tile_at(self.x, self.y)
            new_tile.add_rock(self)
            return True
        return False

    def move_down(self, board):
        # type: (BoxEatsPlantsBoard) -> bool
        if self.y < board.BOARD_HEIGHT - 1:
            old_tile: BoxEatsPlantsTile = board.get_tile_at(self.x, self.y)
            old_tile.remove_rock()
            self.y += 1
            new_tile: BoxEatsPlantsTile = board.get_tile_at(self.x, self.y)
            new_tile.add_rock(self)
            return True
        return False

    def move_left(self, board):
        # type: (BoxEatsPlantsBoard) -> bool
        if self.x > 0:
            old_tile: BoxEatsPlantsTile = board.get_tile_at(self.x, self.y)
            old_tile.remove_rock()
            self.x -= 1
            new_tile: BoxEatsPlantsTile = board.get_tile_at(self.x, self.y)
            new_tile.add_rock(self)
            return True
        return False

    def move_right(self, board):
        # type: (BoxEatsPlantsBoard) -> bool
        if self.x < board.BOARD_WIDTH - 1:
            old_tile: BoxEatsPlantsTile = board.get_tile_at(self.x, self.y)
            old_tile.remove_rock()
            self.x += 1
            new_tile: BoxEatsPlantsTile = board.get_tile_at(self.x, self.y)
            new_tile.add_rock(self)
            return True
        return False

    def __str__(self):
        # type: () -> str
        return str(self.name)

    def clone(self):
        # type: () -> Rock
        return copy.deepcopy(self)


class BoxEatsPlantsTile:
    """
    This class contains attributes of a tile in the minigame "Box Eats Plants".
    """

    def __init__(self):
        # type: () -> None
        self.box: Box or None = None
        self.plant: Plant or None = None
        self.rock: Rock or None = None

    def add_box(self, box):
        # type: (Box) -> bool
        if self.box is None:
            self.box = box
            return True
        return False

    def remove_box(self):
        # type: () -> None
        self.box = None

    def add_plant(self, plant):
        # type: (Plant) -> bool
        if self.plant is None:
            self.plant = plant
            return True
        return False

    def remove_plant(self):
        # type: () -> None
        self.plant = None

    def add_rock(self, rock):
        # type: (Rock) -> bool
        if self.rock is None:
            self.rock = rock
            return True
        return False

    def remove_rock(self):
        # type: () -> None
        self.rock = None

    def __str__(self):
        # type: () -> str
        if self.box is None and self.plant is None and self.rock is None:
            return "NONE"
        res: str = ""  # initial value
        if isinstance(self.box, Box):
            res += str(self.box)

        if isinstance(self.plant, Plant):
            if self.box is not None:
                res += "\n" + str(self.plant)
            else:
                res += str(self.plant)

        if isinstance(self.rock, Rock):
            if self.box is not None or self.plant is not None:
                res += "\n" + str(self.rock)
            else:
                res += str(self.rock)

        return res

    def clone(self):
        # type: () -> BoxEatsPlantsTile
        return copy.deepcopy(self)


###########################################
# BOX EATS PLANTS
###########################################


###########################################
# MATCH WORD PUZZLE
###########################################


def get_index_of_element(a_list: list, elem: object) -> int:
    for i in range(len(a_list)):
        if a_list[i] == elem:
            return i

    return -1


class MatchWordPuzzleBoard:
    """
    This class contains attributes of the board for the minigame "Match Word Puzzle".
    """

    BOARD_WIDTH: int = 6
    BOARD_HEIGHT: int = 4

    def __init__(self):
        # type: () -> None
        self.__tiles: list = []  # initial value
        chosen_keywords: list = []  # initial value
        chosen_keywords_tally: list = [0] * 12
        for i in range(12):
            curr_keyword: str = MatchWordPuzzleTile.POSSIBLE_KEYWORDS[random.randint(0,
                                                                                     len(MatchWordPuzzleTile.POSSIBLE_KEYWORDS) - 1)]
            while curr_keyword in chosen_keywords:
                curr_keyword = MatchWordPuzzleTile.POSSIBLE_KEYWORDS[random.randint(0,
                                                                                    len(MatchWordPuzzleTile.POSSIBLE_KEYWORDS) - 1)]

            chosen_keywords.append(curr_keyword)

        for i in range(self.BOARD_HEIGHT):
            new: list = []  # initial value
            for j in range(self.BOARD_WIDTH):
                curr_keyword: str = chosen_keywords[random.randint(0, len(chosen_keywords) - 1)]
                while chosen_keywords_tally[get_index_of_element(chosen_keywords, curr_keyword)] >= 2:
                    curr_keyword = chosen_keywords[random.randint(0, len(chosen_keywords) - 1)]

                new.append(MatchWordPuzzleTile(curr_keyword))
                chosen_keywords_tally[get_index_of_element(chosen_keywords, curr_keyword)] += 1

            self.__tiles.append(new)

    def all_opened(self):
        # type: () -> bool
        for i in range(self.BOARD_HEIGHT):
            for j in range(self.BOARD_WIDTH):
                if self.__tiles[i][j].is_closed:
                    return False

        return True

    def get_tile_at(self, x, y):
        # type: (int, int) -> MatchWordPuzzleTile or None
        if x < 0 or x >= self.BOARD_WIDTH or y < 0 or y >= self.BOARD_HEIGHT:
            return None
        return self.__tiles[y][x]

    def get_tiles(self):
        # type: () -> list
        return self.__tiles

    def __str__(self):
        # type: () -> str
        return str(tabulate(self.__tiles, tablefmt='fancy_grid'))

    def clone(self):
        # type: () -> MatchWordPuzzleBoard
        return copy.deepcopy(self)


class MatchWordPuzzleTile:
    """
    This class contains attributes of a tile in the minigame "Match Word Puzzle".
    """

    POSSIBLE_KEYWORDS: list = ["AND", "AS", "ASSERT", "BREAK", "CLASS", "CONTINUE", "DEF", "DEL", "ELIF", "ELSE",
                               "EXCEPT", "FALSE", "FINALLY", "FOR", "FROM", "GLOBAL", "IF", "IMPORT", "IN", "IS",
                               "LAMBDA", "NONE", "NONLOCAL", "NOT", "OR", "PASS", "RAISE", "RETURN", "TRUE",
                               "TRY", "WHILE", "WITH", "YIELD"]

    def __init__(self, contents):
        # type: (str) -> None
        self.contents: str = contents if contents in self.POSSIBLE_KEYWORDS else self.POSSIBLE_KEYWORDS[0]
        self.is_closed: bool = True

    def open(self):
        # type: () -> bool
        if self.is_closed:
            self.is_closed = False
            return True
        return False

    def __str__(self):
        # type: () -> str
        return "CLOSED" if self.is_closed else str(self.contents)

    def clone(self):
        # type: () -> MatchWordPuzzleTile
        return copy.deepcopy(self)


###########################################
# MATCH WORD PUZZLE
###########################################


###########################################
# MATCH-3 GAME
###########################################


"""
Code for match-3 game is inspired by the following sources:
1. https://www.raspberrypi.com/news/make-a-columns-style-tile-matching-game-wireframe-25/
2. https://github.com/Wireframe-Magazine/Wireframe-25/blob/master/match3.py
"""


class MatchThreeBoard:
    """
    This class contains attributes of the board for the minigame "Match-3 Game".
    """

    BOARD_WIDTH: int = 10
    BOARD_HEIGHT: int = 10

    def __init__(self):
        # type: () -> None
        self.__tiles: list = [["AND"] * self.BOARD_WIDTH for k in range(self.BOARD_HEIGHT)]  # initial value
        for i in range(self.BOARD_HEIGHT):
            new: list = []  # initial value
            for j in range(self.BOARD_WIDTH):
                curr_keyword: str = MatchThreeTile.POSSIBLE_KEYWORDS[random.randint(0,
                                                                                    len(MatchThreeTile.POSSIBLE_KEYWORDS) - 1)]
                while (i > 0 and self.__tiles[i][j].contents == self.__tiles[i - 1][j].contents) or \
                        (j > 0 and self.__tiles[i][j].contents == self.__tiles[i][j - 1].contents):
                    curr_keyword = MatchThreeTile.POSSIBLE_KEYWORDS[random.randint(0,
                                                                                   len(MatchThreeTile.POSSIBLE_KEYWORDS) - 1)]

                new.append(MatchThreeTile(curr_keyword))

            self.__tiles.append(new)

        self.__matches: list = []  # initial value

    def swap_tiles(self, x1, y1, x2, y2):
        # type: (int, int, int, int) -> bool
        if self.get_tile_at(x1, y1) is None or self.get_tile_at(x2, y2) is None:
            return False

        temp: MatchThreeTile = self.__tiles[y1][x1]
        self.__tiles[y1][x1] = self.__tiles[y2][x2]
        self.__tiles[y2][x2] = temp
        return True

    def no_possible_moves(self):
        # type: () -> bool
        # Trying all possible moves and checking whether it has matches or not
        for j in range(self.BOARD_WIDTH):
            for i in range(self.BOARD_HEIGHT - 1):
                new_board: MatchThreeBoard = self.clone()
                temp: MatchThreeTile = new_board.__tiles[i][j]
                new_board.__tiles[i][j] = new_board.__tiles[i + 1][j]
                new_board.__tiles[i + 1][j] = temp
                matches: list = new_board.check_matches()
                if len(matches) > 0:
                    return False

        for i in range(self.BOARD_HEIGHT):
            for j in range(self.BOARD_WIDTH - 1):
                new_board: MatchThreeBoard = self.clone()
                temp: MatchThreeTile = new_board.__tiles[i][j]
                new_board.__tiles[i][j] = new_board.__tiles[i][j + 1]
                new_board.__tiles[i][j + 1] = temp
                matches: list = new_board.check_matches()
                if len(matches) > 0:
                    return False

        return True

    def check_matches(self):
        # type: () -> list
        self.__matches = []  # initial value
        for j in range(self.BOARD_WIDTH):
            curr_match: list = []  # initial value
            for i in range(self.BOARD_HEIGHT):
                if len(curr_match) == 0 or self.__tiles[i][j].contents == self.__tiles[i - 1][j].contents:
                    curr_match.append((i, j))
                else:
                    if len(curr_match) >= 3:
                        self.__matches.append(curr_match)
                    curr_match = [(i, j)]
            if len(curr_match) >= 3:
                self.__matches.append(curr_match)

        for i in range(self.BOARD_HEIGHT):
            curr_match: list = []  # initial value
            for j in range(self.BOARD_WIDTH):
                if len(curr_match) == 0 or self.__tiles[i][j].contents == self.__tiles[i][j - 1].contents:
                    curr_match.append((i, j))
                else:
                    if len(curr_match) >= 3:
                        self.__matches.append(curr_match)
                    curr_match = [(i, j)]
            if len(curr_match) >= 3:
                self.__matches.append(curr_match)

        return self.__matches

    def clear_matches(self):
        # type: () -> None
        for match in self.__matches:
            for position in match:
                self.__tiles[position[0]][position[1]].contents = "NONE"

        self.__matches = []

    def fill_board(self):
        # type: () -> None
        for j in range(self.BOARD_WIDTH):
            for i in range(self.BOARD_HEIGHT):
                if self.__tiles[i][j].contents == "NONE":
                    for row in range(i, 0, -1):
                        self.__tiles[row][j].contents = self.__tiles[row - 1][j].contents
                    self.__tiles[0][j].contents = MatchThreeTile.POSSIBLE_KEYWORDS[random.randint(0,
                                                                                                  len(MatchThreeTile.POSSIBLE_KEYWORDS) - 1)]
                    while self.__tiles[0][j].contents == self.__tiles[1][j].contents or (j > 0 and
                                                                                         self.__tiles[0][j].contents ==
                                                                                         self.__tiles[0][
                                                                                             j - 1].contents) or \
                            (j < self.BOARD_WIDTH - 1 and self.__tiles[0][j].contents == self.__tiles[0][
                                j + 1].contents):
                        self.__tiles[0][j].contents = MatchThreeTile.POSSIBLE_KEYWORDS[random.randint(0,
                                                                                                      len(MatchThreeTile.POSSIBLE_KEYWORDS) - 1)]

    def get_tile_at(self, x, y):
        # type: (int, int) -> MatchThreeTile or None
        if x < 0 or x >= self.BOARD_WIDTH or y < 0 or y >= self.BOARD_HEIGHT:
            return None
        return self.__tiles[y][x]

    def get_tiles(self):
        # type: () -> list
        return self.__tiles

    def __str__(self):
        # type: () -> str
        return str(tabulate(self.__tiles, tablefmt='fancy_grid'))

    def clone(self):
        # type: () -> MatchThreeBoard
        return copy.deepcopy(self)


class MatchThreeTile:
    """
    This class contains attributes of a tile in the minigame "Match-3 Game".
    """

    POSSIBLE_KEYWORDS: list = ["AND", "AS", "ASSERT", "BREAK", "CLASS", "CONTINUE", "DEF", "DEL", "ELIF", "ELSE",
                               "EXCEPT", "FALSE", "FINALLY", "FOR", "FROM", "GLOBAL"]

    def __init__(self, contents):
        # type: (str) -> None
        self.contents: str = contents if contents in self.POSSIBLE_KEYWORDS else "NONE"

    def __str__(self):
        # type: () -> str
        return str(self.contents)

    def clone(self):
        # type: () -> MatchThreeTile
        return copy.deepcopy(self)


###########################################
# MATCH-3 GAME
###########################################


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

    def execute(self, user, target, skill_to_use=None):
        # type: (LegendaryCreature, LegendaryCreature, Skill or None) -> bool
        if self.name == "NORMAL ATTACK":
            if user == target:
                return False

            raw_damage: mpf = user.attack_power * (1 + user.attack_power_percentage_up / 100 -
                                                   user.attack_power_percentage_down / 100) * \
                              (1 + target.defense_percentage_up / 100 - target.defense_percentage_down / 100)
            damage_reduction_factor: mpf = mpf("1e8") / (mpf("1e8") + 3.5 * target.defense)
            damage: mpf = raw_damage * damage_reduction_factor
            target.curr_hp -= damage
            print(str(user.name) + " dealt " + str(damage) + " damage on " + str(target.name) + "!")
            return True

        elif self.name == "NORMAL HEAL":
            if user != target:
                return False

            heal_amount: mpf = 0.05 * user.max_hp
            user.curr_hp += heal_amount
            return True

        elif self.name == "USE SKILL":
            if isinstance(skill_to_use, ActiveSkill):
                if not skill_to_use.is_active:
                    return False

                if skill_to_use.active_skill_type == "ATTACK":
                    if user == target or user.corresponding_team == target.corresponding_team:
                        return False

                    # Attack the enem(ies)
                    if skill_to_use.is_aoe:
                        for enemy in target.corresponding_team.get_legendary_creatures():
                            damage: mpf = skill_to_use.damage_multiplier.calculate_raw_damage(user, enemy,
                                                                                              skill_to_use.does_ignore_enemies_defense,
                                                                                              skill_to_use.does_ignore_shield,
                                                                                              skill_to_use.does_ignore_invincibility)
                            enemy.curr_hp -= damage
                            print(str(user.name) + " dealt " + str(damage) + " damage on " + str(enemy.name) + "!")

                            # Considering life drain
                            life_drain: mpf = damage * (user.life_drain_percentage + user.life_drain_percentage_up) \
                                              / 100
                            user.curr_hp += life_drain
                            print(str(user.name) + " drained " + str(life_drain) + " HP!")
                            if user.curr_hp >= user.max_hp:
                                user.curr_hp = user.max_hp

                            # Taking into account "ENDURE" effect
                            if not enemy.can_die:
                                enemy.curr_hp = mpf("1")

                            if enemy.can_receive_harmful_effect:
                                # Add negative effects to the enemy
                                resist_chance: mpf = resistance_accuracy_rule(user.accuracy + user.accuracy_up,
                                                                              enemy.resistance + enemy.resistance_up)
                                for harmful_effect in skill_to_use.get_harmful_effects_to_enemies():
                                    if random.random() >= resist_chance:
                                        enemy.add_harmful_effect(harmful_effect)

                                if random.random() >= resist_chance:
                                    enemy.attack_gauge -= skill_to_use.enemies_attack_gauge_down
                                    if enemy.attack_gauge <= enemy.MIN_ATTACK_GAUGE:
                                        enemy.attack_gauge = enemy.MIN_ATTACK_GAUGE

                            # Resetting user's attack gauge to zero at first
                            user.attack_gauge = user.MIN_ATTACK_GAUGE

                            # Consider effect of passive skills of the user
                            # 1. Beneficial effects to allies
                            for legendary_creature in user.corresponding_team.get_legendary_creatures():
                                if legendary_creature.can_receive_beneficial_effect:
                                    for skill in user.get_skills():
                                        if isinstance(skill, PassiveSkill):
                                            for beneficial_effect in \
                                                    skill.passive_skill_effect.get_beneficial_effects_to_allies():
                                                legendary_creature.add_beneficial_effect(beneficial_effect)

                            # 2. Harmful effects to enemies
                            if enemy.can_receive_harmful_effect:
                                for skill in user.get_skills():
                                    if isinstance(skill, PassiveSkill):
                                        resist_chance = resistance_accuracy_rule(
                                            user.accuracy + user.accuracy_up,
                                            enemy.resistance + enemy.resistance_up)
                                        for harmful_effect in \
                                                skill.passive_skill_effect.get_harmful_effects_to_enemies():
                                            # Add negative effects to the enemy
                                            if random.random() >= resist_chance:
                                                enemy.add_harmful_effect(harmful_effect)

                            # 3. Increase allies' attack gauge
                            for legendary_creature in user.corresponding_team.get_legendary_creatures():
                                for skill in user.get_skills():
                                    if isinstance(skill, PassiveSkill):
                                        legendary_creature.attack_gauge += skill.passive_skill_effect.allies_attack_gauge_up

                            # 4. Decrease enemies' attack gauge
                            if enemy.can_receive_harmful_effect:
                                for skill in user.get_skills():
                                    if isinstance(skill, PassiveSkill):
                                        resist_chance = resistance_accuracy_rule(
                                            user.accuracy + user.accuracy_up,
                                            enemy.resistance + enemy.resistance_up)
                                        if random.random() >= resist_chance:
                                            enemy.attack_gauge -= skill.passive_skill_effect.enemies_attack_gauge_down

                            # 5. Heal allies
                            for legendary_creature in user.corresponding_team.get_legendary_creatures():
                                if legendary_creature.can_be_healed:
                                    for skill in user.get_skills():
                                        if isinstance(skill, PassiveSkill):
                                            legendary_creature.curr_hp += skill.passive_skill_effect.heal_amount_to_allies
                                            if legendary_creature.curr_hp >= legendary_creature.max_hp:
                                                legendary_creature.curr_hp = legendary_creature.max_hp
                    else:
                        damage: mpf = skill_to_use.damage_multiplier.calculate_raw_damage(user, target,
                                                                                          skill_to_use.does_ignore_enemies_defense,
                                                                                          skill_to_use.does_ignore_shield,
                                                                                          skill_to_use.does_ignore_invincibility)
                        target.curr_hp -= damage
                        print(str(user.name) + " dealt " + str(damage) + " damage on " + str(target.name) + "!")

                        # Considering life drain
                        life_drain: mpf = damage * (user.life_drain_percentage + user.life_drain_percentage_up) \
                                          / 100
                        user.curr_hp += life_drain
                        print(str(user.name) + " drained " + str(life_drain) + " HP!")
                        if user.curr_hp >= user.max_hp:
                            user.curr_hp = user.max_hp

                        # Taking into account "ENDURE" effect
                        if not target.can_die:
                            target.curr_hp = mpf("1")

                        if target.can_receive_harmful_effect:
                            # Add negative effects to the enemy
                            resist_chance: mpf = resistance_accuracy_rule(user.accuracy + user.accuracy_up,
                                                                          target.resistance + target.resistance_up)
                            for harmful_effect in skill_to_use.get_harmful_effects_to_enemies():
                                if random.random() >= resist_chance:
                                    target.add_harmful_effect(harmful_effect)

                            if random.random() >= resist_chance:
                                target.attack_gauge -= skill_to_use.enemies_attack_gauge_down
                                if target.attack_gauge <= target.MIN_ATTACK_GAUGE:
                                    target.attack_gauge = target.MIN_ATTACK_GAUGE

                        # Resetting user's attack gauge to zero at first
                        user.attack_gauge = user.MIN_ATTACK_GAUGE

                        # Consider effect of passive skills of the user
                        # 1. Beneficial effects to allies
                        for legendary_creature in user.corresponding_team.get_legendary_creatures():
                            if legendary_creature.can_receive_beneficial_effect:
                                for skill in user.get_skills():
                                    if isinstance(skill, PassiveSkill):
                                        for beneficial_effect in \
                                                skill.passive_skill_effect.get_beneficial_effects_to_allies():
                                            legendary_creature.add_beneficial_effect(beneficial_effect)

                        # 2. Harmful effects to enemies
                        if target.can_receive_harmful_effect:
                            for skill in user.get_skills():
                                if isinstance(skill, PassiveSkill):
                                    resist_chance = resistance_accuracy_rule(user.accuracy + user.accuracy_up,
                                                                             target.resistance + target.resistance_up)
                                    for harmful_effect in \
                                            skill.passive_skill_effect.get_harmful_effects_to_enemies():
                                        # Add negative effects to the enemy
                                        if random.random() >= resist_chance:
                                            target.add_harmful_effect(harmful_effect)

                        # 3. Increase allies' attack gauge
                        for legendary_creature in user.corresponding_team.get_legendary_creatures():
                            for skill in user.get_skills():
                                if isinstance(skill, PassiveSkill):
                                    legendary_creature.attack_gauge += skill.passive_skill_effect.allies_attack_gauge_up

                        # 4. Decrease enemies' attack gauge
                        if target.can_receive_harmful_effect:
                            for skill in user.get_skills():
                                if isinstance(skill, PassiveSkill):
                                    resist_chance = resistance_accuracy_rule(user.accuracy + user.accuracy_up,
                                                                             target.resistance + target.resistance_up)
                                    if random.random() >= resist_chance:
                                        target.attack_gauge -= skill.passive_skill_effect.enemies_attack_gauge_down

                        # 5. Heal allies
                        for legendary_creature in user.corresponding_team.get_legendary_creatures():
                            if legendary_creature.can_be_healed:
                                for skill in user.get_skills():
                                    if isinstance(skill, PassiveSkill):
                                        legendary_creature.curr_hp += skill.passive_skill_effect.heal_amount_to_allies
                                        if legendary_creature.curr_hp >= legendary_creature.max_hp:
                                            legendary_creature.curr_hp = legendary_creature.max_hp

                elif skill_to_use.active_skill_type == "HEAL":
                    if user.corresponding_team != target.corresponding_team:
                        return False

                    # Heal the all(ies)
                    if skill_to_use.is_aoe:
                        for ally in target.corresponding_team.get_legendary_creatures():
                            if ally.can_be_healed:
                                ally.curr_hp += skill_to_use.heal_amount_to_allies
                                if ally.curr_hp >= ally.max_hp:
                                    ally.curr_hp = ally.max_hp
                    else:
                        if target.can_be_healed:
                            target.curr_hp += skill_to_use.heal_amount_to_allies
                            if target.curr_hp >= target.max_hp:
                                target.curr_hp = target.max_hp

                elif skill_to_use.active_skill_type == "ALLIES EFFECT":
                    if user.corresponding_team != target.corresponding_team:
                        return False

                    # Give beneficial effects to all(ies)
                    if skill_to_use.is_aoe:
                        for ally in target.corresponding_team.get_legendary_creatures():
                            if ally.can_receive_beneficial_effect:
                                for beneficial_effect in skill_to_use.get_beneficial_effects_to_allies():
                                    ally.add_beneficial_effect(beneficial_effect)

                            ally.attack_gauge += skill_to_use.allies_attack_gauge_up
                    else:
                        if target.can_receive_beneficial_effect:
                            for beneficial_effect in skill_to_use.get_beneficial_effects_to_allies():
                                target.add_beneficial_effect(beneficial_effect)

                        target.attack_gauge += skill_to_use.allies_attack_gauge_up

                elif skill_to_use.active_skill_type == "ENEMIES EFFECT":
                    if user == target or user.corresponding_team == target.corresponding_team:
                        return False

                    # Give harmful effects to enem(ies)
                    if skill_to_use.is_aoe:
                        for enemy in target.corresponding_team.get_legendary_creatures():
                            resist_chance: mpf = resistance_accuracy_rule(user.accuracy, enemy.resistance)
                            for harmful_effect in skill_to_use.get_harmful_effects_to_enemies():
                                if random.random() >= resist_chance:
                                    enemy.add_harmful_effect(harmful_effect)

                            if random.random() >= resist_chance:
                                enemy.attack_gauge -= skill_to_use.enemies_attack_gauge_down
                                if enemy.attack_gauge <= enemy.MIN_ATTACK_GAUGE:
                                    enemy.attack_gauge = enemy.MIN_ATTACK_GAUGE
                    else:
                        resist_chance: mpf = resistance_accuracy_rule(user.accuracy, target.resistance)
                        for harmful_effect in skill_to_use.get_harmful_effects_to_enemies():
                            if random.random() >= resist_chance:
                                target.add_harmful_effect(harmful_effect)

                        if random.random() >= resist_chance:
                            target.attack_gauge -= skill_to_use.enemies_attack_gauge_down
                            if target.attack_gauge <= target.MIN_ATTACK_GAUGE:
                                target.attack_gauge = target.MIN_ATTACK_GAUGE

                skill_to_use.cooltime = skill_to_use.max_cooltime
                return True

            else:
                return False
        return False

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
        self.reward: Reward = Reward(mpf("10") ** sum(legendary_creature.rating for legendary_creature
                                                      in self.team2.get_legendary_creatures()),
                                     mpf("10") ** (sum(legendary_creature.rating for legendary_creature
                                                       in self.team2.get_legendary_creatures()) - 2),
                                     mpf("10") ** (sum(legendary_creature.rating for legendary_creature
                                                       in self.team2.get_legendary_creatures()) - 5),
                                     mpf("10") ** sum(legendary_creature.rating for legendary_creature
                                                      in self.team2.get_legendary_creatures()))
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

    def get_someone_to_move(self):
        # type: () -> None
        """
        Getting a legendary creature to move and have its turn.
        :return: None
        """

        # Finding out which legendary creature moves
        full_attack_gauge_list: list = []  # initial value
        while len(full_attack_gauge_list) == 0:
            for legendary_creature in self.team1.get_legendary_creatures():
                if legendary_creature.attack_gauge >= legendary_creature.FULL_ATTACK_GAUGE and legendary_creature not \
                        in full_attack_gauge_list:
                    full_attack_gauge_list.append(legendary_creature)

            for legendary_creature in self.team2.get_legendary_creatures():
                if legendary_creature.attack_gauge >= legendary_creature.FULL_ATTACK_GAUGE and legendary_creature not \
                        in full_attack_gauge_list:
                    full_attack_gauge_list.append(legendary_creature)

            self.tick()

        max_attack_gauge: mpf = max(legendary_creature.attack_gauge for legendary_creature in full_attack_gauge_list)
        for legendary_creature in full_attack_gauge_list:
            if legendary_creature.attack_gauge == max_attack_gauge:
                self.whose_turn = legendary_creature

    def tick(self):
        # type: () -> None
        """
        The clock ticks when battles are carried out.
        :return: None
        """

        for legendary_creature in self.team1.get_legendary_creatures():
            legendary_creature.attack_gauge += legendary_creature.attack_speed * 0.07

        for legendary_creature in self.team2.get_legendary_creatures():
            legendary_creature.attack_gauge += legendary_creature.attack_speed * 0.07

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
        self.__potential_opponents: list = potential_opponents  # initial value

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
        self.battle_team: Team = Team()
        self.item_inventory: ItemInventory = ItemInventory()
        self.legendary_creature_inventory: LegendaryCreatureInventory = LegendaryCreatureInventory()
        self.player_city: PlayerCity = PlayerCity()
        self.__unlocked_levels: list = []  # initial value
        self.add_unlocked_level()  # ensuring that the player has unlocked at least one level

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

    def place_egg_in_hatchery(self, egg, hatchery):
        # type: (Egg, Hatchery) -> bool
        if egg not in self.item_inventory.get_items():
            return False

        hatchery_exists: bool = False
        for section in self.player_city.get_sections():
            for y in range(section.SECTION_HEIGHT):
                for x in range(section.SECTION_WIDTH):
                    curr_tile: CityTile = section.get_tile_at(x, y)
                    if curr_tile.building == hatchery:
                        hatchery_exists = True
                        break

        if not hatchery_exists:
            return False

        if hatchery.add_egg(egg):
            # Make the egg hatch in 5 minutes
            egg.hatch_time = datetime.now() + timedelta(minutes=5)
            egg.already_placed = True
            return True
        return False

    def hatch_eggs_in_hatcheries(self):
        # type: () -> None
        """
        This function automatically hatches all eggs in the hatcheries
        :return: None
        """
        hatcheries: list = []  # initial value
        for section in self.player_city.get_sections():
            for y in range(section.SECTION_HEIGHT):
                for x in range(section.SECTION_WIDTH):
                    curr_tile: CityTile = section.get_tile_at(x, y)
                    if isinstance(curr_tile.building, Hatchery):
                        hatcheries.append(curr_tile.building)

        for hatchery in hatcheries:
            assert isinstance(hatchery, Hatchery), "Not a hatchery! Invalid instance in 'hatcheries' list!"
            for egg in hatchery.get_eggs_placed():
                if egg.hatch_time is not None:
                    if datetime.now() >= egg.hatch_time:
                        # Initialise a random legendary creature
                        hatchery.remove_egg(egg)
                        self.remove_item_from_inventory(egg)
                        new_legendary_creature: LegendaryCreature = generate_random_legendary_creature(egg.element)
                        self.add_legendary_creature(new_legendary_creature)

    def claim_reward(self, reward):
        # type: (Reward) -> None
        self.exp += reward.player_reward_exp
        self.level_up()
        self.gold += reward.player_reward_gold
        self.gems += reward.player_reward_gems
        for legendary_creature in self.battle_team.get_legendary_creatures():
            legendary_creature.exp += reward.legendary_creature_reward_exp
            legendary_creature.level_up()

        self.battle_team.recover_all()
        for item in reward.get_player_reward_items():
            self.add_item_to_inventory(item)

    def feed_legendary_creature(self, legendary_creature, food):
        # type: (LegendaryCreature, mpf) -> bool
        if legendary_creature not in self.legendary_creature_inventory.get_legendary_creatures():
            return False

        if food > self.food:
            return False

        legendary_creature.exp += food
        legendary_creature.level_up()
        return True

    def make_a_wish(self, temple_of_wishes):
        # type: (TempleOfWishes) -> bool
        temple_of_wishes_exists: bool = False
        for section in self.player_city.get_sections():
            for y in range(section.SECTION_HEIGHT):
                for x in range(section.SECTION_WIDTH):
                    curr_tile: CityTile = section.get_tile_at(x, y)
                    if curr_tile.building == temple_of_wishes:
                        temple_of_wishes_exists = True
                        break

        if not temple_of_wishes_exists:
            return False

        if temple_of_wishes.wishes_left <= 0:
            return False

        potential_objects: list = temple_of_wishes.get_obtainable_objects()
        object_obtained: Item or Reward or LegendaryCreature = \
            potential_objects[random.randint(0, len(potential_objects) - 1)]
        if isinstance(object_obtained, Item):
            self.add_item_to_inventory(object_obtained)
        elif isinstance(object_obtained, Reward):
            self.claim_reward(object_obtained)
        elif isinstance(object_obtained, LegendaryCreature):
            self.add_legendary_creature(object_obtained)
        else:
            pass

        return True

    def fuse_legendary_creatures(self, legendary_creature1, legendary_creature2, fusion_center):
        # type: (LegendaryCreature, LegendaryCreature, FusionCenter) -> bool
        if legendary_creature1 not in self.legendary_creature_inventory.get_legendary_creatures() or \
                legendary_creature2 not in self.legendary_creature_inventory.get_legendary_creatures():
            return False

        if legendary_creature1 in self.battle_team.get_legendary_creatures() or \
                legendary_creature2 in self.battle_team.get_legendary_creatures():
            return False

        if legendary_creature1.placed_in_training_area or legendary_creature1.placed_in_habitat or \
                legendary_creature2.placed_in_training_area or legendary_creature2.placed_in_habitat:
            return False

        fusion_center_exists: bool = False
        for section in self.player_city.get_sections():
            for y in range(section.SECTION_HEIGHT):
                for x in range(section.SECTION_WIDTH):
                    curr_tile: CityTile = section.get_tile_at(x, y)
                    if curr_tile.building == fusion_center:
                        fusion_center_exists = True
                        break

        if not fusion_center_exists:
            return False

        # Fuse both legendary creatures into a new one
        name: str = generate_random_name()
        main_element: str = legendary_creature1.get_elements()[0]
        elements: list = [element for element in legendary_creature1.get_elements()] + \
                         [element for element in legendary_creature2.get_elements()]
        rating: int = 1
        max_hp: mpf = legendary_creature1.max_hp + legendary_creature2.max_hp
        max_magic_points: mpf = legendary_creature1.max_magic_points + legendary_creature2.max_magic_points
        attack_power: mpf = legendary_creature1.attack_power + legendary_creature2.attack_power
        defense: mpf = legendary_creature1.defense + legendary_creature2.defense
        attack_speed: mpf = max(legendary_creature1.attack_speed, legendary_creature2.attack_speed)
        skills: list = [skill for skill in legendary_creature1.get_skills()] + \
                       [skill for skill in legendary_creature2.get_skills()]
        awaken_bonus: AwakenBonus = legendary_creature1.awaken_bonus
        new_legendary_creature: LegendaryCreature = LegendaryCreature(name, main_element, rating, max_hp,
                                                                      max_magic_points, attack_power, defense,
                                                                      attack_speed, skills, awaken_bonus)
        new_legendary_creature.set_elements(elements)
        new_legendary_creature.max_hp_percentage_up = max(legendary_creature1.max_hp_percentage_up,
                                                          legendary_creature2.max_hp_percentage_up)
        new_legendary_creature.max_magic_points_percentage_up = max(legendary_creature1.max_magic_points_percentage_up,
                                                                    legendary_creature2.max_magic_points_percentage_up)
        new_legendary_creature.attack_power_percentage_up = max(legendary_creature1.attack_power_percentage_up,
                                                                legendary_creature2.attack_power_percentage_up)
        new_legendary_creature.attack_speed_percentage_up = max(legendary_creature1.attack_speed_percentage_up,
                                                                legendary_creature2.attack_speed_percentage_up)
        new_legendary_creature.defense_percentage_up = max(legendary_creature1.defense_percentage_up,
                                                           legendary_creature2.defense_percentage_up)
        new_legendary_creature.crit_damage_up = max(legendary_creature1.crit_damage_up,
                                                    legendary_creature2.crit_damage_up)
        self.remove_legendary_creature(legendary_creature1)
        self.remove_legendary_creature(legendary_creature2)
        self.add_legendary_creature(new_legendary_creature)
        return True

    def give_item_to_legendary_creature(self, item, legendary_creature):
        # type: (Item, LegendaryCreature) -> bool
        if item not in self.item_inventory.get_items():
            return False

        if legendary_creature not in self.legendary_creature_inventory.get_legendary_creatures():
            return False

        if isinstance(item, EXPShard):
            legendary_creature.exp += item.exp_granted
            legendary_creature.level_up()
            self.remove_item_from_inventory(item)
            return True
        elif isinstance(item, LevelUpShard):
            legendary_creature.exp = legendary_creature.required_exp
            legendary_creature.level_up()
            self.remove_item_from_inventory(item)
            return True
        elif isinstance(item, SkillLevelUpShard):
            skill_index: int = random.randint(0, len(legendary_creature.get_skills()) - 1)
            curr_skill: Skill = legendary_creature.get_skills()[skill_index]
            curr_skill.level_up()
            self.remove_item_from_inventory(item)
            return True
        elif isinstance(item, AwakenShard):
            if item.legendary_creature_element in legendary_creature.get_elements():
                legendary_creature.awaken()
                self.remove_item_from_inventory(item)
                return True
            return False
        return False

    def power_up_legendary_creature(self, legendary_creature_to_power_up, material_legendary_creatures,
                                    power_up_circle):
        # type: (LegendaryCreature, list, PowerUpCircle) -> bool
        if len(material_legendary_creatures) < 0 or len(material_legendary_creatures) > \
                power_up_circle.MAX_MATERIAL_LEGENDARY_CREATURES:
            return False

        if legendary_creature_to_power_up not in self.legendary_creature_inventory.get_legendary_creatures():
            return False

        power_up_circle_exists: bool = False
        for section in self.player_city.get_sections():
            for y in range(section.SECTION_HEIGHT):
                for x in range(section.SECTION_WIDTH):
                    curr_tile: CityTile = section.get_tile_at(x, y)
                    if curr_tile.building == power_up_circle:
                        power_up_circle_exists = True
                        break

        if not power_up_circle_exists:
            return False

        power_up_circle.deselect_legendary_creature_to_power_up()
        power_up_circle.select_legendary_creature_to_power_up(legendary_creature_to_power_up)
        power_up_circle.set_material_legendary_creatures(material_legendary_creatures)
        legendary_creature_to_power_up = power_up_circle.execute_power_up()
        assert isinstance(legendary_creature_to_power_up, LegendaryCreature), "Legendary creature power-up failed!"
        for legendary_creature in material_legendary_creatures:
            self.remove_legendary_creature(legendary_creature)

        return True

    def evolve_legendary_creature(self, legendary_creature_to_evolve, material_legendary_creatures,
                                  power_up_circle):
        # type: (LegendaryCreature, list, PowerUpCircle) -> bool
        if len(material_legendary_creatures) < 0 or len(material_legendary_creatures) > \
                power_up_circle.MAX_MATERIAL_LEGENDARY_CREATURES:
            return False

        if legendary_creature_to_evolve not in self.legendary_creature_inventory.get_legendary_creatures():
            return False

        power_up_circle_exists: bool = False
        for section in self.player_city.get_sections():
            for y in range(section.SECTION_HEIGHT):
                for x in range(section.SECTION_WIDTH):
                    curr_tile: CityTile = section.get_tile_at(x, y)
                    if curr_tile.building == power_up_circle:
                        power_up_circle_exists = True
                        break

        if not power_up_circle_exists:
            return False

        power_up_circle.deselect_legendary_creature_to_power_up()
        power_up_circle.select_legendary_creature_to_power_up(legendary_creature_to_evolve)
        power_up_circle.set_material_legendary_creatures(material_legendary_creatures)
        legendary_creature_to_evolve = power_up_circle.execute_evolution()
        assert isinstance(legendary_creature_to_evolve, LegendaryCreature), "Legendary creature evolution failed!"
        for legendary_creature in material_legendary_creatures:
            self.remove_legendary_creature(legendary_creature)

        return True

    def add_legendary_creature_to_habitat(self, legendary_creature, habitat):
        # type: (LegendaryCreature, Habitat) -> bool
        if legendary_creature not in self.legendary_creature_inventory.get_legendary_creatures() or \
                legendary_creature in self.battle_team.get_legendary_creatures() or \
                legendary_creature.placed_in_training_area:
            return False

        habitat_exists: bool = False
        for section in self.player_city.get_sections():
            for y in range(section.SECTION_HEIGHT):
                for x in range(section.SECTION_WIDTH):
                    curr_tile: CityTile = section.get_tile_at(x, y)
                    if curr_tile.building == habitat:
                        habitat_exists = True
                        break

        if not habitat_exists:
            return False

        if habitat.add_legendary_creature(legendary_creature) and habitat.element in legendary_creature.get_elements():
            legendary_creature.player_gold_per_second += habitat.player_gold_per_second_increase
            self.gold_per_second += habitat.player_gold_per_second_increase
            legendary_creature.placed_in_habitat = True
            return True
        return False

    def remove_legendary_creature_from_habitat(self, legendary_creature, habitat):
        # type: (LegendaryCreature, Habitat) -> bool
        if legendary_creature not in self.legendary_creature_inventory.get_legendary_creatures() or \
                legendary_creature in self.battle_team.get_legendary_creatures() or \
                legendary_creature.placed_in_training_area:
            return False

        habitat_exists: bool = False
        for section in self.player_city.get_sections():
            for y in range(section.SECTION_HEIGHT):
                for x in range(section.SECTION_WIDTH):
                    curr_tile: CityTile = section.get_tile_at(x, y)
                    if curr_tile.building == habitat:
                        habitat_exists = True
                        break

        if not habitat_exists:
            return False

        if habitat.remove_legendary_creature(legendary_creature):
            legendary_creature.player_gold_per_second -= habitat.player_gold_per_second_increase
            self.gold_per_second -= habitat.player_gold_per_second_increase
            legendary_creature.placed_in_habitat = False
            return True
        return False

    def add_legendary_creature_to_training_area(self, legendary_creature, training_area):
        # type: (LegendaryCreature, TrainingArea) -> bool
        if legendary_creature not in self.legendary_creature_inventory.get_legendary_creatures() or \
                legendary_creature in self.battle_team.get_legendary_creatures() or \
                legendary_creature.placed_in_habitat:
            return False

        training_area_exists: bool = False
        for section in self.player_city.get_sections():
            for y in range(section.SECTION_HEIGHT):
                for x in range(section.SECTION_WIDTH):
                    curr_tile: CityTile = section.get_tile_at(x, y)
                    if curr_tile.building == training_area:
                        training_area_exists = True
                        break

        if not training_area_exists:
            return False

        if training_area.add_legendary_creature(legendary_creature):
            legendary_creature.exp_per_second += training_area.legendary_creature_exp_per_second
            legendary_creature.placed_in_training_area = True
            return True
        return False

    def remove_legendary_creature_from_training_area(self, legendary_creature, training_area):
        # type: (LegendaryCreature, TrainingArea) -> bool
        if legendary_creature not in self.legendary_creature_inventory.get_legendary_creatures() or \
                legendary_creature in self.battle_team.get_legendary_creatures() or \
                legendary_creature.placed_in_habitat:
            return False

        training_area_exists: bool = False
        for section in self.player_city.get_sections():
            for y in range(section.SECTION_HEIGHT):
                for x in range(section.SECTION_WIDTH):
                    curr_tile: CityTile = section.get_tile_at(x, y)
                    if curr_tile.building == training_area:
                        training_area_exists = True
                        break

        if not training_area_exists:
            return False

        if training_area.remove_legendary_creature(legendary_creature):
            legendary_creature.exp_per_second -= training_area.legendary_creature_exp_per_second
            legendary_creature.placed_in_training_area = False
            return True
        return False

    def add_section_to_player_city(self):
        # type: () -> bool
        if self.gold >= self.player_city.section_build_gold_cost:
            self.gold -= self.player_city.section_build_gold_cost
            self.player_city.add_section()
            return True
        return False

    def level_up_building_at_section_tile(self, section_index, tile_x, tile_y):
        # type: (int, int, int) -> bool
        if section_index < 0 or section_index >= len(self.player_city.get_sections()):
            return False

        corresponding_section: Section = self.player_city.get_sections()[section_index]
        if isinstance(corresponding_section.get_tile_at(tile_x, tile_y), CityTile):
            curr_tile: CityTile = corresponding_section.get_tile_at(tile_x, tile_y)
            if isinstance(curr_tile.building, Building):
                curr_building: Building = curr_tile.building
                if self.gold < curr_building.upgrade_gold_cost or self.gems < curr_building.upgrade_gem_cost:
                    return False

                self.gold -= curr_building.upgrade_gold_cost
                self.gems -= curr_building.upgrade_gem_cost

                if isinstance(curr_building, Guardstone):
                    for legendary_creature in self.legendary_creature_inventory.get_legendary_creatures():
                        assert isinstance(legendary_creature, LegendaryCreature), "Invalid argument in the list of " \
                                                                                  "legendary creatures in player's " \
                                                                                  "legendary creature inventory."
                        initial_legendary_creature_defense_percentage_up: mpf = \
                            curr_building.legendary_creature_defense_percentage_up
                        curr_building.level_up()
                        legendary_creature.DEFAULT_DEFENSE_PERCENTAGE_UP += \
                            (curr_building.legendary_creature_defense_percentage_up -
                             initial_legendary_creature_defense_percentage_up)
                        legendary_creature.defense_percentage_up += \
                            (curr_building.legendary_creature_defense_percentage_up -
                             initial_legendary_creature_defense_percentage_up)
                elif isinstance(curr_building, LegendaryCreatureSanctuary):
                    for legendary_creature in self.legendary_creature_inventory.get_legendary_creatures():
                        assert isinstance(legendary_creature, LegendaryCreature), "Invalid argument in the list of " \
                                                                                  "legendary creatures in player's " \
                                                                                  "legendary creature inventory."
                        initial_legendary_creature_attack_power_percentage_up: mpf = \
                            curr_building.legendary_creature_attack_power_percentage_up
                        curr_building.level_up()
                        legendary_creature.DEFAULT_ATTACK_POWER_PERCENTAGE_UP += \
                            (curr_building.legendary_creature_attack_power_percentage_up -
                             initial_legendary_creature_attack_power_percentage_up)
                        legendary_creature.attack_power_percentage_up += \
                            (curr_building.legendary_creature_attack_power_percentage_up -
                             initial_legendary_creature_attack_power_percentage_up)
                elif isinstance(curr_building, SurvivalAltar):
                    for legendary_creature in self.legendary_creature_inventory.get_legendary_creatures():
                        assert isinstance(legendary_creature, LegendaryCreature), "Invalid argument in the list of " \
                                                                                  "legendary creatures in player's " \
                                                                                  "legendary creature inventory."
                        initial_legendary_creature_max_hp_percentage_up: mpf = \
                            curr_building.legendary_creature_max_hp_percentage_up
                        curr_building.level_up()
                        legendary_creature.DEFAULT_MAX_HP_PERCENTAGE_UP += \
                            (curr_building.legendary_creature_max_hp_percentage_up -
                             initial_legendary_creature_max_hp_percentage_up)
                        legendary_creature.max_hp_percentage_up += \
                            (curr_building.legendary_creature_max_hp_percentage_up -
                             initial_legendary_creature_max_hp_percentage_up)
                elif isinstance(curr_building, MagicAltar):
                    for legendary_creature in self.legendary_creature_inventory.get_legendary_creatures():
                        assert isinstance(legendary_creature, LegendaryCreature), "Invalid argument in the list of " \
                                                                                  "legendary creatures in player's " \
                                                                                  "legendary creature inventory."
                        initial_legendary_creature_max_magic_points_percentage_up: mpf = \
                            curr_building.legendary_creature_max_magic_points_percentage_up
                        curr_building.level_up()
                        legendary_creature.DEFAULT_MAX_MAGIC_POINTS_PERCENTAGE_UP += \
                            (curr_building.legendary_creature_max_magic_points_percentage_up -
                             initial_legendary_creature_max_magic_points_percentage_up)
                        legendary_creature.max_magic_points_percentage_up += \
                            (curr_building.legendary_creature_max_magic_points_percentage_up -
                             initial_legendary_creature_max_magic_points_percentage_up)
                elif isinstance(curr_building, BoosterTower):
                    for legendary_creature in self.legendary_creature_inventory.get_legendary_creatures():
                        assert isinstance(legendary_creature, LegendaryCreature), "Invalid argument in the list of " \
                                                                                  "legendary creatures in player's " \
                                                                                  "legendary creature inventory."
                        initial_legendary_creature_attack_speed_percentage_up: mpf = \
                            curr_building.legendary_creature_attack_speed_percentage_up
                        curr_building.level_up()
                        legendary_creature.DEFAULT_ATTACK_SPEED_PERCENTAGE_UP += \
                            (curr_building.legendary_creature_attack_speed_percentage_up -
                             initial_legendary_creature_attack_speed_percentage_up)
                        legendary_creature.attack_speed_percentage_up += \
                            (curr_building.legendary_creature_attack_speed_percentage_up -
                             initial_legendary_creature_attack_speed_percentage_up)
                elif isinstance(curr_building, PlayerEXPTower):
                    initial_exp_per_second: mpf = curr_building.exp_per_second
                    curr_building.level_up()
                    self.exp_per_second += (curr_building.exp_per_second - initial_exp_per_second)
                elif isinstance(curr_building, FoodFarm):
                    initial_food_per_second: mpf = curr_building.food_per_second
                    curr_building.level_up()
                    self.food_per_second += (curr_building.food_per_second - initial_food_per_second)
                elif isinstance(curr_building, GoldMine):
                    initial_gold_per_second: mpf = curr_building.gold_per_second
                    curr_building.level_up()
                    self.gold_per_second += (curr_building.gold_per_second - initial_gold_per_second)
                elif isinstance(curr_building, GemMine):
                    initial_gems_per_second: mpf = curr_building.gem_per_second
                    curr_building.level_up()
                    self.gems_per_second += (curr_building.gem_per_second - initial_gems_per_second)
                elif isinstance(curr_building, Habitat):
                    initial_gold_per_second: mpf = curr_building.player_gold_per_second_increase
                    curr_building.level_up()
                    for legendary_creature in curr_building.get_legendary_creatures_placed():
                        legendary_creature.player_gold_per_second += (curr_building.player_gold_per_second_increase -
                                                                      initial_gold_per_second)
                        self.gold_per_second += (curr_building.player_gold_per_second_increase -
                                                 initial_gold_per_second)

                else:
                    curr_building.level_up()
                return True

            return False
        return False

    def build_at_section_tile(self, section_index, tile_x, tile_y, building):
        # type: (int, int, int, Building) -> bool
        if section_index < 0 or section_index >= len(self.player_city.get_sections()):
            return False

        corresponding_section: Section = self.player_city.get_sections()[section_index]
        if isinstance(corresponding_section.get_tile_at(tile_x, tile_y), CityTile):
            curr_tile: CityTile = corresponding_section.get_tile_at(tile_x, tile_y)
            if curr_tile.building is not None:
                return False

            if self.gold < building.gold_cost or self.gems < building.gem_cost:
                return False

            self.gold -= building.gold_cost
            self.gems -= building.gem_cost

            if isinstance(building, Guardstone):
                for legendary_creature in self.legendary_creature_inventory.get_legendary_creatures():
                    assert isinstance(legendary_creature, LegendaryCreature), "Invalid argument in the list of " \
                                                                              "legendary creatures in player's " \
                                                                              "legendary creature inventory."
                    legendary_creature.DEFAULT_DEFENSE_PERCENTAGE_UP += \
                        building.legendary_creature_defense_percentage_up
                    legendary_creature.defense_percentage_up += building.legendary_creature_defense_percentage_up
            elif isinstance(building, LegendaryCreatureSanctuary):
                for legendary_creature in self.legendary_creature_inventory.get_legendary_creatures():
                    assert isinstance(legendary_creature, LegendaryCreature), "Invalid argument in the list of " \
                                                                              "legendary creatures in player's " \
                                                                              "legendary creature inventory."
                    legendary_creature.DEFAULT_ATTACK_POWER_PERCENTAGE_UP += \
                        building.legendary_creature_attack_power_percentage_up
                    legendary_creature.attack_power_percentage_up += \
                        building.legendary_creature_attack_power_percentage_up
            elif isinstance(building, SurvivalAltar):
                for legendary_creature in self.legendary_creature_inventory.get_legendary_creatures():
                    assert isinstance(legendary_creature, LegendaryCreature), "Invalid argument in the list of " \
                                                                              "legendary creatures in player's " \
                                                                              "legendary creature inventory."
                    legendary_creature.DEFAULT_MAX_HP_PERCENTAGE_UP += \
                        building.legendary_creature_max_hp_percentage_up
                    legendary_creature.max_hp_percentage_up += \
                        building.legendary_creature_max_hp_percentage_up
            elif isinstance(building, MagicAltar):
                for legendary_creature in self.legendary_creature_inventory.get_legendary_creatures():
                    assert isinstance(legendary_creature, LegendaryCreature), "Invalid argument in the list of " \
                                                                              "legendary creatures in player's " \
                                                                              "legendary creature inventory."
                    legendary_creature.DEFAULT_MAX_MAGIC_POINTS_PERCENTAGE_UP += \
                        building.legendary_creature_max_magic_points_percentage_up
                    legendary_creature.max_magic_points_percentage_up += \
                        building.legendary_creature_max_magic_points_percentage_up
            elif isinstance(building, BoosterTower):
                for legendary_creature in self.legendary_creature_inventory.get_legendary_creatures():
                    assert isinstance(legendary_creature, LegendaryCreature), "Invalid argument in the list of " \
                                                                              "legendary creatures in player's " \
                                                                              "legendary creature inventory."
                    legendary_creature.DEFAULT_ATTACK_SPEED_PERCENTAGE_UP += \
                        building.legendary_creature_attack_speed_percentage_up
                    legendary_creature.attack_speed_percentage_up += \
                        building.legendary_creature_attack_speed_percentage_up
            elif isinstance(building, PlayerEXPTower):
                self.exp_per_second += building.exp_per_second
            elif isinstance(building, FoodFarm):
                self.food_per_second += building.food_per_second
            elif isinstance(building, GoldMine):
                self.gold_per_second += building.gold_per_second
            elif isinstance(building, GemMine):
                self.gems_per_second += building.gem_per_second
            elif isinstance(building, Obstacle):
                # Cannot build obstacle
                return False

            curr_tile.building = building
            return True
        return False

    def remove_building_from_section_tile(self, section_index, tile_x, tile_y):
        # type: (int, int, int) -> bool
        if section_index < 0 or section_index >= len(self.player_city.get_sections()):
            return False

        corresponding_section: Section = self.player_city.get_sections()[section_index]
        if isinstance(corresponding_section.get_tile_at(tile_x, tile_y), CityTile):
            curr_tile: CityTile = corresponding_section.get_tile_at(tile_x, tile_y)
            if isinstance(curr_tile.building, Building):
                curr_building: Building = curr_tile.building
                self.gold += curr_building.sell_gold_gain
                self.gems += curr_building.sell_gem_gain

                if isinstance(curr_building, Guardstone):
                    for legendary_creature in self.legendary_creature_inventory.get_legendary_creatures():
                        assert isinstance(legendary_creature, LegendaryCreature), "Invalid argument in the list of " \
                                                                                  "legendary creatures in player's " \
                                                                                  "legendary creature inventory."
                        legendary_creature.DEFAULT_DEFENSE_PERCENTAGE_UP -= \
                            curr_building.legendary_creature_defense_percentage_up
                        legendary_creature.defense_percentage_up -= \
                            curr_building.legendary_creature_defense_percentage_up
                elif isinstance(curr_building, LegendaryCreatureSanctuary):
                    for legendary_creature in self.legendary_creature_inventory.get_legendary_creatures():
                        assert isinstance(legendary_creature, LegendaryCreature), "Invalid argument in the list of " \
                                                                                  "legendary creatures in player's " \
                                                                                  "legendary creature inventory."
                        legendary_creature.DEFAULT_ATTACK_POWER_PERCENTAGE_UP -= \
                            curr_building.legendary_creature_attack_power_percentage_up
                        legendary_creature.attack_power_percentage_up -= \
                            curr_building.legendary_creature_attack_power_percentage_up
                elif isinstance(curr_building, SurvivalAltar):
                    for legendary_creature in self.legendary_creature_inventory.get_legendary_creatures():
                        assert isinstance(legendary_creature, LegendaryCreature), "Invalid argument in the list of " \
                                                                                  "legendary creatures in player's " \
                                                                                  "legendary creature inventory."
                        legendary_creature.DEFAULT_MAX_HP_PERCENTAGE_UP -= \
                            curr_building.legendary_creature_max_hp_percentage_up
                        legendary_creature.max_hp_percentage_up -= \
                            curr_building.legendary_creature_max_hp_percentage_up
                elif isinstance(curr_building, MagicAltar):
                    for legendary_creature in self.legendary_creature_inventory.get_legendary_creatures():
                        assert isinstance(legendary_creature, LegendaryCreature), "Invalid argument in the list of " \
                                                                                  "legendary creatures in player's " \
                                                                                  "legendary creature inventory."
                        legendary_creature.DEFAULT_MAX_MAGIC_POINTS_PERCENTAGE_UP -= \
                            curr_building.legendary_creature_max_magic_points_percentage_up
                        legendary_creature.max_magic_points_percentage_up -= \
                            curr_building.legendary_creature_max_magic_points_percentage_up
                elif isinstance(curr_building, BoosterTower):
                    for legendary_creature in self.legendary_creature_inventory.get_legendary_creatures():
                        assert isinstance(legendary_creature, LegendaryCreature), "Invalid argument in the list of " \
                                                                                  "legendary creatures in player's " \
                                                                                  "legendary creature inventory."
                        legendary_creature.DEFAULT_ATTACK_SPEED_PERCENTAGE_UP -= \
                            curr_building.legendary_creature_attack_speed_percentage_up
                        legendary_creature.attack_speed_percentage_up -= \
                            curr_building.legendary_creature_attack_speed_percentage_up
                elif isinstance(curr_building, PlayerEXPTower):
                    self.exp_per_second -= curr_building.exp_per_second
                elif isinstance(curr_building, FoodFarm):
                    self.food_per_second -= curr_building.food_per_second
                elif isinstance(curr_building, GoldMine):
                    self.gold_per_second -= curr_building.gold_per_second
                elif isinstance(curr_building, GemMine):
                    self.gems_per_second -= curr_building.gem_per_second
                elif isinstance(curr_building, Obstacle):
                    self.gold += curr_building.remove_gold_gain
                    self.gems += curr_building.remove_gem_gain

                curr_tile.building = None
                return True
            return False
        return False

    def place_rune_on_legendary_creature(self, legendary_creature, rune):
        # type: (LegendaryCreature, Rune) -> bool
        if legendary_creature in self.legendary_creature_inventory.get_legendary_creatures() and rune in \
                self.item_inventory.get_items():
            legendary_creature.place_rune(rune)
            return True
        return False

    def remove_rune_from_legendary_creature(self, legendary_creature, slot_number):
        # type: (LegendaryCreature, int) -> bool
        if legendary_creature in self.legendary_creature_inventory.get_legendary_creatures():
            if slot_number in legendary_creature.get_runes().keys():
                legendary_creature.remove_rune(slot_number)
                return True
            return False
        return False

    def level_up(self):
        # type: () -> None
        while self.exp >= self.required_exp:
            self.level += 1
            self.required_exp *= mpf("10") ** self.level

    def purchase_item(self, item):
        # type: (Item) -> bool
        if self.gold >= item.gold_cost and self.gems >= item.gem_cost:
            self.gold -= item.gold_cost
            self.gems -= item.gem_cost
            self.add_item_to_inventory(item)
            return True
        return False

    def sell_item(self, item):
        # type: (Item) -> bool
        if item in self.item_inventory.get_items():
            if isinstance(item, Rune):
                if item.already_placed:
                    return False

            self.remove_item_from_inventory(item)
            self.gold += item.sell_gold_gain
            self.gems += item.sell_gem_gain
            return True
        return False

    def level_up_rune(self, rune):
        # type: (Rune) -> bool
        if rune in self.item_inventory.get_items():
            if self.gold >= rune.level_up_gold_cost:
                self.gold -= rune.level_up_gold_cost
                return rune.level_up()
            return False
        else:
            # Check whether a legendary creature has the rune 'rune' or not
            for legendary_creature in self.legendary_creature_inventory.get_legendary_creatures():
                if rune in legendary_creature.get_runes().values():
                    if self.gold >= rune.level_up_gold_cost:
                        self.gold -= rune.level_up_gold_cost
                        return legendary_creature.level_up_rune(rune.slot_number)
                    return False
            return False

    def add_item_to_inventory(self, item):
        # type: (Item) -> None
        self.item_inventory.add_item(item)

    def remove_item_from_inventory(self, item):
        # type: (Item) -> bool
        if isinstance(item, Rune):
            for legendary_creature in self.legendary_creature_inventory.get_legendary_creatures():
                if item in legendary_creature.get_runes().values():
                    return False

        return self.item_inventory.remove_item(item)

    def add_legendary_creature(self, legendary_creature):
        # type: (LegendaryCreature) -> None
        self.gold_per_second += legendary_creature.player_gold_per_second
        self.legendary_creature_inventory.add_legendary_creature(legendary_creature)

    def remove_legendary_creature(self, legendary_creature):
        # type: (LegendaryCreature) -> bool
        if legendary_creature in self.battle_team.get_legendary_creatures() or \
                legendary_creature.placed_in_training_area or legendary_creature.placed_in_habitat:
            return False
        if self.legendary_creature_inventory.remove_legendary_creature(legendary_creature):
            self.gold_per_second -= legendary_creature.player_gold_per_second
            return True

    def add_legendary_creature_to_team(self, legendary_creature):
        # type: (LegendaryCreature) -> bool
        if legendary_creature in self.legendary_creature_inventory.get_legendary_creatures():
            if self.battle_team.add_legendary_creature(legendary_creature):
                legendary_creature.corresponding_team = self.battle_team
                return True
            return False
        return False

    def remove_legendary_creature_from_team(self, legendary_creature):
        # type: (LegendaryCreature) -> bool
        if legendary_creature in self.legendary_creature_inventory.get_legendary_creatures():
            legendary_creature.corresponding_team = Team()
            return self.battle_team.remove_legendary_creature(legendary_creature)
        return False

    def get_unlocked_levels(self):
        # type: () -> list
        return self.__unlocked_levels

    def add_unlocked_level(self):
        # type: () -> None
        new_level_number: int = Level.LEVEL_NUMBER + 1
        level_stages: list = []  # initial value
        for i in range(5):
            level_stages.append(Stage([generate_random_legendary_creature(
                Egg.POTENTIAL_ELEMENTS[random.randint(0, len(Egg.POTENTIAL_ELEMENTS) - 1)]
            ),
                generate_random_legendary_creature(
                    Egg.POTENTIAL_ELEMENTS[random.randint(0, len(Egg.POTENTIAL_ELEMENTS) - 1)]
                ),
                generate_random_legendary_creature(
                    Egg.POTENTIAL_ELEMENTS[random.randint(0, len(Egg.POTENTIAL_ELEMENTS) - 1)]
                ),
                generate_random_legendary_creature(
                    Egg.POTENTIAL_ELEMENTS[random.randint(0, len(Egg.POTENTIAL_ELEMENTS) - 1)]
                ),
                generate_random_legendary_creature(
                    Egg.POTENTIAL_ELEMENTS[random.randint(0, len(Egg.POTENTIAL_ELEMENTS) - 1)]
                )]))

        level_ups: int = 5 * (new_level_number - 1)
        for stage in level_stages:
            for legendary_creature in stage.get_enemies_list():
                for k in range(level_ups):
                    legendary_creature.exp = legendary_creature.required_exp
                    legendary_creature.level_up()
                    if legendary_creature.level == legendary_creature.max_level:
                        legendary_creature.evolve()

        new_level: Level = Level(level_stages, Reward(
            mpf("10") ** (5 * new_level_number),
            mpf("10") ** (5 * new_level_number),
            mpf(5 * new_level_number),
            mpf("10") ** (5 * new_level_number),
            [Egg(mpf("1e6"), mpf("10"),
                 Egg.POTENTIAL_ELEMENTS[random.randint(0, len(Egg.POTENTIAL_ELEMENTS) - 1)]),
             AwakenShard(mpf("1e6"), mpf("10"),
                         Egg.POTENTIAL_ELEMENTS[random.randint(0, len(Egg.POTENTIAL_ELEMENTS) - 1)])]
        ))
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
        self.times_beaten: int = 0  # initial value

    def strengthen(self):
        # type: () -> None
        for legendary_creature in self.battle_team.get_legendary_creatures():
            level_ups: int = 2 ** self.times_beaten
            for i in range(level_ups):
                legendary_creature.exp = legendary_creature.required_exp
                legendary_creature.level_up()
                if legendary_creature.level == legendary_creature.max_level:
                    legendary_creature.evolve()


class PlayerCity:
    """
    This class contains attributes of the city the player builds.
    """

    def __init__(self):
        # type: () -> None
        self.__sections: list = [Section()]  # initial value
        self.section_build_gold_cost: mpf = mpf("1e8")

    def add_section(self):
        # type: () -> None
        self.section_build_gold_cost *= mpf("10") ** (triangular(len(self.__sections)))
        self.__sections.append(Section())

    def get_sections(self):
        # type: () -> list
        return self.__sections

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


class Section:
    """
    This class contains attributes of a section in a player's city.
    """

    SECTION_WIDTH: int = 10
    SECTION_HEIGHT: int = 10

    def __init__(self):
        # type: () -> None
        self.__tiles: list = []  # initial value
        for i in range(self.SECTION_WIDTH):
            new = []  # initial value
            for k in range(self.SECTION_HEIGHT):
                # Ensuring that obstacles are not placed at the edges of the section
                place_obstacle: bool = random.random() <= 0.3
                if place_obstacle and not self.is_edge(i, k):
                    new.append(CityTile(Obstacle()))
                else:
                    new.append(CityTile())

            self.__tiles.append(new)

    def is_edge(self, x, y):
        # type: (int, int) -> bool
        return (x == 0 and y == 0) or (x == 0 and y == self.SECTION_HEIGHT - 1) or \
               (x == self.SECTION_WIDTH - 1 and y == 0) or (x == self.SECTION_WIDTH - 1
                                                            and y == self.SECTION_HEIGHT - 1)

    def get_tiles(self):
        # type: () -> list
        return self.__tiles

    def get_tile_at(self, x, y):
        # type: (int, int) -> CityTile or None
        if x < 0 or x >= self.SECTION_WIDTH or y < 0 or y >= self.SECTION_HEIGHT:
            return None
        return self.__tiles[y][x]

    def __str__(self):
        # type: () -> str
        return str(tabulate(self.__tiles, headers='firstrow', tablefmt='fancy_grid'))

    def clone(self):
        # type: () -> Section
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
        if isinstance(self.building, Building):
            return "CityTile(" + str(self.building.name) + ")"
        return "CityTile(GRASS)"

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

    def set_leader(self, leader=None):
        # type: (LegendaryCreature or None) -> None
        if leader not in self.__legendary_creatures or len(self.__legendary_creatures) == 0 or leader is None:
            self.leader = None
        else:
            self.leader = leader

    def recover_all(self):
        # type: () -> None
        for legendary_creature in self.__legendary_creatures:
            legendary_creature.restore()

    def all_died(self):
        # type: () -> bool
        for legendary_creature in self.__legendary_creatures:
            if legendary_creature.get_is_alive():
                return False
        return True

    def add_legendary_creature(self, legendary_creature):
        # type: (LegendaryCreature) -> bool
        if len(self.__legendary_creatures) < self.MAX_LEGENDARY_CREATURES:
            legendary_creature_ids: list = [creature.legendary_creature_id for creature
                                            in self.__legendary_creatures]
            if legendary_creature.legendary_creature_id not in legendary_creature_ids:
                self.__legendary_creatures.append(legendary_creature)
                self.set_leader()
                return True
            return False
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

    def __init__(self, name, main_element, rating, max_hp, max_magic_points, attack_power, defense, attack_speed,
                 skills,
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
        self.player_gold_per_second: mpf = mpf(int(max_hp / 500))
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
        self.placed_in_habitat: bool = False
        self.corresponding_team: Team = Team()

    def set_elements(self, elements):
        # type: (list) -> None
        self.__elements = elements

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

    def awaken(self):
        # type: () -> bool
        if not self.has_awakened:
            self.name = "AWAKENED " + str(self.name)
            self.max_hp *= 1 + self.awaken_bonus.max_hp_percentage_up / 100
            self.max_magic_points *= 1 + self.awaken_bonus.max_magic_points_percentage_up / 100
            self.attack_power *= 1 + self.awaken_bonus.attack_power_percentage_up / 100
            self.defense *= 1 + self.awaken_bonus.defense_percentage_up / 100
            self.attack_speed += self.awaken_bonus.attack_speed_up
            self.crit_rate += self.awaken_bonus.crit_rate_up
            self.crit_damage += self.awaken_bonus.crit_damage_up
            self.resistance += self.awaken_bonus.resistance_up
            if self.resistance > self.MAX_RESISTANCE:
                self.resistance = self.MAX_RESISTANCE

            self.accuracy += self.awaken_bonus.accuracy_up
            if self.accuracy > self.MAX_ACCURACY:
                self.accuracy = self.MAX_ACCURACY

            self.__skills.append(self.awaken_bonus.new_skill_gained)
            self.restore()
            self.has_awakened = True
            return True
        return False

    def evolve(self):
        # type: () -> bool
        if self.level == self.max_level and self.rating < self.MAX_RATING and self.exp >= self.required_exp:
            self.rating += 1
            self.level = 1
            self.max_level = 10 * triangular(self.rating) if self.rating < self.MAX_RATING else float('inf')
            self.exp = mpf("0")
            self.required_exp = mpf("1e6")
            temp_runes: dict = self.__runes
            for slot_number in self.__runes.keys():
                self.remove_rune(slot_number)

            self.attack_power *= triangular(self.level) + 1
            self.max_hp *= triangular(self.level) + 1
            self.max_magic_points *= triangular(self.level) + 1
            self.defense *= triangular(self.level) + 1
            self.attack_speed += 3
            for rune in temp_runes.values():
                self.place_rune(rune)

            self.restore()
            return True
        return False

    def use_passive_skills(self):
        # type: () -> bool
        if self.can_use_passive_skills and not self.passive_skills_activated:
            for skill in self.__skills:
                if isinstance(skill, PassiveSkill):
                    self.max_hp_percentage_up += skill.passive_skill_effect.max_hp_percentage_up
                    self.max_magic_points_percentage_up += skill.passive_skill_effect.max_magic_points_percentage_up
                    self.attack_power_percentage_up += skill.passive_skill_effect.attack_power_percentage_up
                    self.defense_percentage_up += skill.passive_skill_effect.defense_percentage_up
                    self.attack_speed_percentage_up += skill.passive_skill_effect.attack_speed_percentage_up
                    self.crit_rate_up += skill.passive_skill_effect.crit_rate_up
                    self.crit_damage_up += skill.passive_skill_effect.crit_damage_up
                    self.resistance_up += skill.passive_skill_effect.resistance_up
                    self.accuracy_up += skill.passive_skill_effect.accuracy_up
                    self.extra_turn_chance_up += skill.passive_skill_effect.extra_turn_chance_up

            self.passive_skills_activated = True
            return True
        return False

    def deactivate_passive_skills(self):
        # type: () -> bool
        if self.passive_skills_activated:
            for skill in self.__skills:
                if isinstance(skill, PassiveSkill):
                    self.max_hp_percentage_up -= skill.passive_skill_effect.max_hp_percentage_up
                    self.max_magic_points_percentage_up -= skill.passive_skill_effect.max_magic_points_percentage_up
                    self.attack_power_percentage_up -= skill.passive_skill_effect.attack_power_percentage_up
                    self.defense_percentage_up -= skill.passive_skill_effect.defense_percentage_up
                    self.attack_speed_percentage_up -= skill.passive_skill_effect.attack_speed_percentage_up
                    self.crit_rate_up -= skill.passive_skill_effect.crit_rate_up
                    self.crit_damage_up -= skill.passive_skill_effect.crit_damage_up
                    self.resistance_up -= skill.passive_skill_effect.resistance_up
                    self.accuracy_up -= skill.passive_skill_effect.accuracy_up
                    self.extra_turn_chance_up -= skill.passive_skill_effect.extra_turn_chance_up

            self.passive_skills_activated = False
            return True
        return False

    def use_leader_skills(self):
        # type: () -> bool
        if not self.leader_skills_activated:
            for legendary_creature in self.corresponding_team.get_legendary_creatures():
                for skill in self.__skills:
                    if isinstance(skill, LeaderSkill):
                        legendary_creature.max_hp_percentage_up += skill.leader_skill_effect.max_hp_percentage_up
                        legendary_creature.max_magic_points_percentage_up += \
                            skill.leader_skill_effect.max_magic_points_percentage_up
                        legendary_creature.attack_power_percentage_up += \
                            skill.leader_skill_effect.attack_power_percentage_up
                        legendary_creature.defense_percentage_up += skill.leader_skill_effect.defense_percentage_up
                        legendary_creature.attack_speed_percentage_up += \
                            skill.leader_skill_effect.attack_speed_percentage_up
                        legendary_creature.crit_rate_up += skill.leader_skill_effect.crit_rate_up
                        legendary_creature.crit_damage_up += skill.leader_skill_effect.crit_damage_up
                        legendary_creature.resistance_up += skill.leader_skill_effect.resistance_up
                        legendary_creature.accuracy_up += skill.leader_skill_effect.accuracy_up

            self.leader_skills_activated = True
            return True
        return False

    def deactivate_leader_skills(self):
        # type: () -> bool
        if self.leader_skills_activated:
            for legendary_creature in self.corresponding_team.get_legendary_creatures():
                for skill in self.__skills:
                    if isinstance(skill, LeaderSkill):
                        legendary_creature.max_hp_percentage_up -= skill.leader_skill_effect.max_hp_percentage_up
                        legendary_creature.max_magic_points_percentage_up -= \
                            skill.leader_skill_effect.max_magic_points_percentage_up
                        legendary_creature.attack_power_percentage_up -= \
                            skill.leader_skill_effect.attack_power_percentage_up
                        legendary_creature.defense_percentage_up -= skill.leader_skill_effect.defense_percentage_up
                        legendary_creature.attack_speed_percentage_up -= \
                            skill.leader_skill_effect.attack_speed_percentage_up
                        legendary_creature.crit_rate_up -= skill.leader_skill_effect.crit_rate_up
                        legendary_creature.crit_damage_up -= skill.leader_skill_effect.crit_damage_up
                        legendary_creature.resistance_up -= skill.leader_skill_effect.resistance_up
                        legendary_creature.accuracy_up -= skill.leader_skill_effect.accuracy_up

            self.leader_skills_activated = False
            return True
        return False

    def get_is_alive(self):
        # type: () -> bool
        return self.curr_hp > 0

    def recover_magic_points(self):
        # type: () -> None
        self.curr_magic_points += self.max_magic_points / 12
        if self.curr_magic_points >= self.max_magic_points:
            self.curr_magic_points = self.max_magic_points

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

    def add_beneficial_effect(self, beneficial_effect):
        # type: (BeneficialEffect) -> bool
        if len(self.__beneficial_effects) < self.MAX_BENEFICIAL_EFFECTS:
            if beneficial_effect.name in [b.name for b in self.__beneficial_effects] and not \
                    beneficial_effect.can_be_stacked:
                return False

            self.attack_power_percentage_up += beneficial_effect.attack_power_percentage_up
            self.attack_speed_percentage_up += beneficial_effect.attack_speed_percentage_up
            self.defense_percentage_up += beneficial_effect.defense_percentage_up
            self.crit_rate_up += beneficial_effect.crit_rate_up
            if beneficial_effect.prevents_damage:
                self.can_receive_damage = False

            if beneficial_effect.blocks_debuffs:
                self.can_receive_harmful_effect = False

            if beneficial_effect.prevents_death:
                self.can_die = False

            self.heal_percentage_per_turn += beneficial_effect.heal_percentage_per_turn
            self.counterattack_chance_up += beneficial_effect.counterattack_chance_up
            self.reflected_damage_percentage_up += beneficial_effect.reflected_damage_percentage_up
            self.life_drain_percentage_up += beneficial_effect.life_drain_percentage_up
            self.crit_resist_up += beneficial_effect.crit_resist_up
            self.shield_percentage += beneficial_effect.shield_percentage_up
            self.__beneficial_effects.append(beneficial_effect)
            return True
        return False

    def remove_beneficial_effect(self, beneficial_effect):
        # type: (BeneficialEffect) -> bool
        if beneficial_effect in self.__beneficial_effects:
            self.attack_power_percentage_up -= beneficial_effect.attack_power_percentage_up
            self.attack_speed_percentage_up -= beneficial_effect.attack_speed_percentage_up
            self.defense_percentage_up -= beneficial_effect.defense_percentage_up
            self.crit_rate_up -= beneficial_effect.crit_rate_up
            if beneficial_effect.prevents_damage:
                self.can_receive_damage = True

            if beneficial_effect.blocks_debuffs:
                self.can_receive_harmful_effect = True

            if beneficial_effect.prevents_death:
                self.can_die = True

            self.heal_percentage_per_turn -= beneficial_effect.heal_percentage_per_turn
            self.counterattack_chance_up -= beneficial_effect.counterattack_chance_up
            self.reflected_damage_percentage_up -= beneficial_effect.reflected_damage_percentage_up
            self.life_drain_percentage_up -= beneficial_effect.life_drain_percentage_up
            self.crit_resist_up -= beneficial_effect.crit_resist_up
            self.shield_percentage -= beneficial_effect.shield_percentage_up
            self.__beneficial_effects.remove(beneficial_effect)
            return True
        return False

    def add_harmful_effect(self, harmful_effect):
        # type: (HarmfulEffect) -> bool
        if len(self.__harmful_effects) < self.MAX_HARMFUL_EFFECTS:
            if harmful_effect.name in [h.name for h in self.__harmful_effects] and not \
                    harmful_effect.can_be_stacked:
                return False

            self.attack_power_percentage_down += harmful_effect.attack_power_percentage_down
            self.attack_speed_percentage_down += harmful_effect.attack_speed_percentage_down
            self.defense_percentage_down += harmful_effect.defense_percentage_down
            if harmful_effect.blocks_beneficial_effects:
                self.can_receive_beneficial_effect = False

            self.damage_received_percentage_up += harmful_effect.damage_received_percentage_up
            if harmful_effect.blocks_heal:
                self.can_be_healed = False

            if harmful_effect.blocks_passive_skills:
                self.can_use_passive_skills = False
                self.deactivate_passive_skills()

            if harmful_effect.blocks_skills_with_cooltime:
                self.can_use_skills_with_cooltime = False

            self.damage_percentage_per_turn += harmful_effect.damage_percentage_per_turn
            if harmful_effect.prevents_moves:
                self.can_move = False

            self.__harmful_effects.append(harmful_effect)
            return True
        return False

    def remove_harmful_effect(self, harmful_effect):
        # type: (HarmfulEffect) -> bool
        if harmful_effect in self.__harmful_effects:
            self.attack_power_percentage_down -= harmful_effect.attack_power_percentage_down
            self.attack_speed_percentage_down -= harmful_effect.attack_speed_percentage_down
            self.defense_percentage_down -= harmful_effect.defense_percentage_down
            if harmful_effect.blocks_beneficial_effects:
                self.can_receive_beneficial_effect = True

            self.damage_received_percentage_up -= harmful_effect.damage_received_percentage_up
            if harmful_effect.blocks_heal:
                self.can_be_healed = True

            if harmful_effect.blocks_passive_skills:
                self.can_use_passive_skills = True
                self.use_passive_skills()

            if harmful_effect.blocks_skills_with_cooltime:
                self.can_use_skills_with_cooltime = True

            self.damage_percentage_per_turn -= harmful_effect.damage_percentage_per_turn
            if harmful_effect.prevents_moves:
                self.can_move = True

            self.__harmful_effects.remove(harmful_effect)
            return True
        return False

    def get_skills(self):
        # type: () -> list
        return self.__skills

    def add_skill(self, skill):
        # type: (Skill) -> None
        self.__skills.append(skill)

    def get_runes(self):
        # type: () -> dict
        return self.__runes

    def place_rune(self, rune):
        # type: (Rune) -> bool
        if rune.already_placed:
            return False

        if rune.slot_number in self.__runes.keys():
            self.remove_rune(rune.slot_number)

        self.__runes[rune.slot_number] = rune
        self.max_hp *= 1 + (rune.stat_increase.max_hp_percentage_up / 100)
        self.max_hp += rune.stat_increase.max_hp_up
        self.max_magic_points *= 1 + (rune.stat_increase.max_magic_points_percentage_up / 100)
        self.max_magic_points += rune.stat_increase.max_magic_points_up
        self.attack_power *= 1 + (rune.stat_increase.attack_percentage_up / 100)
        self.attack_power += rune.stat_increase.attack_up
        self.defense *= 1 + (rune.stat_increase.defense_percentage_up / 100)
        self.defense += rune.stat_increase.defense_up
        self.attack_speed += rune.stat_increase.attack_speed_up
        self.crit_rate += rune.stat_increase.crit_rate_up
        self.crit_damage += rune.stat_increase.crit_damage_up
        self.resistance += rune.stat_increase.resistance_up
        if self.resistance >= self.MAX_RESISTANCE:
            self.resistance = self.MAX_RESISTANCE

        self.accuracy += rune.stat_increase.accuracy_up
        if self.accuracy >= self.MAX_ACCURACY:
            self.accuracy = self.MAX_ACCURACY

        # Try to activate the set effect of the rune if possible.
        matching_runes: int = sum(1 for curr_rune in self.__runes.values() if curr_rune.set_name == rune.set_name)
        if matching_runes >= rune.set_size and not rune.set_effect_is_active:
            self.max_hp *= 1 + (rune.set_effect.max_hp_percentage_up / 100)
            self.max_magic_points *= 1 + (rune.set_effect.max_magic_points_percentage_up / 100)
            self.attack_power *= 1 + (rune.set_effect.attack_percentage_up / 100)
            self.defense *= 1 + (rune.set_effect.defense_percentage_up / 100)
            self.attack_speed *= 1 + (rune.set_effect.attack_speed_percentage_up / 100)
            self.crit_rate += rune.set_effect.crit_rate_up
            self.crit_damage += rune.set_effect.crit_damage_up
            self.resistance += rune.set_effect.resistance_up
            if self.resistance >= self.MAX_RESISTANCE:
                self.resistance = self.MAX_RESISTANCE

            self.accuracy += rune.set_effect.accuracy_up
            if self.accuracy >= self.MAX_ACCURACY:
                self.accuracy = self.MAX_ACCURACY

            self.extra_turn_chance += rune.set_effect.extra_turn_chance_up
            if self.extra_turn_chance >= self.MAX_EXTRA_TURN_CHANCE:
                self.extra_turn_chance = self.MAX_EXTRA_TURN_CHANCE

            self.counterattack_chance += rune.set_effect.counterattack_chance_up
            if self.counterattack_chance >= self.MAX_COUNTERATTACK_CHANCE:
                self.counterattack_chance = self.MAX_COUNTERATTACK_CHANCE

            self.reflected_damage_percentage += rune.set_effect.reflected_damage_percentage_up
            self.life_drain_percentage += rune.set_effect.life_drain_percentage_up
            self.crit_resist += rune.set_effect.crit_resist_up
            if self.crit_resist >= self.MAX_CRIT_RESIST:
                self.crit_resist = self.MAX_CRIT_RESIST

            self.stun_rate += rune.set_effect.stun_rate_up
            rune.set_effect_is_active = True
            count: int = 0
            while count < rune.set_size:
                for other_rune in self.__runes.values():
                    if other_rune.set_name == rune.set_name:
                        other_rune.set_effect_is_active = True
                        count += 1

        self.restore()
        rune.already_placed = True
        return True

    def level_up(self):
        # type: () -> None
        while self.exp >= self.required_exp and self.level < self.max_level:
            self.level += 1
            self.required_exp *= mpf("10") ** self.level
            temp_runes: dict = self.__runes
            for slot_number in self.__runes.keys():
                self.remove_rune(slot_number)

            self.attack_power *= triangular(self.level)
            self.max_hp *= triangular(self.level)
            self.player_gold_per_second *= triangular(self.level)
            self.max_magic_points *= triangular(self.level)
            self.defense *= triangular(self.level)
            self.attack_speed += 2
            for rune in temp_runes.values():
                self.place_rune(rune)

            self.restore()

    def level_up_rune(self, slot_number):
        # type: (int) -> bool
        if slot_number not in self.__runes.keys():
            return False

        current_rune: Rune = self.__runes[slot_number]
        self.remove_rune(slot_number)
        success: bool = current_rune.level_up()
        self.place_rune(current_rune)
        return success

    def remove_rune(self, slot_number):
        # type: (int) -> bool
        if slot_number in self.__runes.keys():
            # Remove the rune at slot number 'slot_number'
            current_rune: Rune = self.__runes[slot_number]
            self.max_hp -= current_rune.stat_increase.max_hp_up
            self.max_hp /= 1 + (current_rune.stat_increase.max_hp_percentage_up / 100)
            self.max_magic_points -= current_rune.stat_increase.max_magic_points_up
            self.max_magic_points /= 1 + (current_rune.stat_increase.max_magic_points_percentage_up / 100)
            self.attack_power -= current_rune.stat_increase.attack_up
            self.attack_power /= 1 + (current_rune.stat_increase.attack_percentage_up / 100)
            self.defense -= current_rune.stat_increase.defense_up
            self.defense /= 1 + (current_rune.stat_increase.defense_percentage_up / 100)
            self.attack_speed -= current_rune.stat_increase.attack_speed_up
            self.crit_rate -= current_rune.stat_increase.crit_rate_up
            if self.crit_rate <= self.MIN_CRIT_RATE:
                self.crit_rate = self.MIN_CRIT_RATE

            self.crit_damage -= current_rune.stat_increase.crit_damage_up
            if self.crit_damage <= self.MIN_CRIT_DAMAGE:
                self.crit_damage = self.MIN_CRIT_DAMAGE

            self.resistance -= current_rune.stat_increase.resistance_up
            if self.resistance <= self.MIN_RESISTANCE:
                self.resistance = self.MIN_RESISTANCE

            self.accuracy -= current_rune.stat_increase.accuracy_up
            if self.accuracy <= self.MIN_ACCURACY:
                self.accuracy = self.MIN_ACCURACY

            # Try to deactivate the set effect of the rune if possible.
            matching_runes: int = sum(1 for rune in self.__runes.values() if rune.set_name == current_rune.set_name)
            if matching_runes >= current_rune.set_size and current_rune.set_effect_is_active:
                self.max_hp /= 1 + (current_rune.stat_increase.max_hp_percentage_up / 100)
                self.max_magic_points /= 1 + (current_rune.set_effect.max_magic_points_percentage_up / 100)
                self.attack_power /= 1 + (current_rune.set_effect.attack_percentage_up / 100)
                self.defense /= 1 + (current_rune.set_effect.defense_percentage_up / 100)
                self.attack_speed /= 1 + (current_rune.set_effect.attack_speed_percentage_up / 100)
                self.crit_rate -= current_rune.set_effect.crit_rate_up
                if self.crit_rate <= self.MIN_CRIT_RATE:
                    self.crit_rate = self.MIN_CRIT_RATE

                self.crit_damage -= current_rune.set_effect.crit_damage_up
                if self.crit_damage <= self.MIN_CRIT_DAMAGE:
                    self.crit_damage = self.MIN_CRIT_DAMAGE

                self.resistance -= current_rune.set_effect.resistance_up
                if self.resistance <= self.MIN_RESISTANCE:
                    self.resistance = self.MIN_RESISTANCE

                self.accuracy -= current_rune.set_effect.accuracy_up
                if self.accuracy <= self.MIN_ACCURACY:
                    self.accuracy = self.MIN_ACCURACY

                self.extra_turn_chance -= current_rune.set_effect.extra_turn_chance_up
                if self.extra_turn_chance <= self.MIN_EXTRA_TURN_CHANCE:
                    self.extra_turn_chance = self.MIN_EXTRA_TURN_CHANCE

                self.counterattack_chance -= current_rune.set_effect.counterattack_chance_up
                if self.counterattack_chance <= self.MIN_COUNTERATTACK_CHANCE:
                    self.counterattack_chance = self.MIN_COUNTERATTACK_CHANCE

                self.reflected_damage_percentage -= current_rune.set_effect.reflected_damage_percentage_up
                self.life_drain_percentage -= current_rune.set_effect.life_drain_percentage_up
                self.crit_resist -= current_rune.set_effect.crit_resist_up
                if self.crit_resist <= self.MIN_CRIT_RESIST:
                    self.crit_resist = self.MIN_CRIT_RESIST

                self.stun_rate -= current_rune.set_effect.stun_rate_up
                current_rune.set_effect_is_active = False
                count: int = 0
                while count < current_rune.set_size:
                    for other_rune in self.__runes.values():
                        if other_rune.set_name == current_rune.set_name:
                            other_rune.set_effect_is_active = False
                            count += 1

            self.restore()
            self.__runes.pop(current_rune.slot_number)
            current_rune.already_placed = False
            return True
        return False

    def have_turn(self, other, active_skill, action_name):
        # type: (LegendaryCreature, ActiveSkill or None, str) -> bool
        if self.can_use_passive_skills and not self.passive_skills_activated:
            self.use_passive_skills()

        for beneficial_effect in self.get_beneficial_effects():
            beneficial_effect.number_of_turns -= 1
            if beneficial_effect.number_of_turns <= 0:
                self.remove_beneficial_effect(beneficial_effect)

        for harmful_effect in self.get_harmful_effects():
            harmful_effect.number_of_turns -= 1
            if harmful_effect.number_of_turns <= 0:
                self.remove_harmful_effect(harmful_effect)

        if self.can_move:
            if action_name == "NORMAL ATTACK":
                self.normal_attack(other)
            elif action_name == "NORMAL HEAL":
                self.normal_heal(other)
            elif action_name == "USE SKILL" and isinstance(active_skill, ActiveSkill):
                self.use_skill(other, active_skill)
            else:
                pass

            return True
        return False

    def counterattack(self, other):
        # type: (LegendaryCreature) -> bool
        if self.can_move:
            first_attacking_active_skill: ActiveSkill or None = None  # initial value
            for skill in self.get_skills():
                if isinstance(skill, ActiveSkill):
                    if skill.active_skill_type == "ATTACK":
                        first_attacking_active_skill = skill

            if first_attacking_active_skill is None:
                self.normal_attack(other)
            else:
                assert isinstance(first_attacking_active_skill, ActiveSkill)
                if self.curr_magic_points < first_attacking_active_skill.magic_points_cost:
                    self.normal_attack(other)
                else:
                    self.use_skill(other, first_attacking_active_skill)
            return True
        else:
            return False

    def normal_attack(self, other):
        # type: (LegendaryCreature) -> None
        action: Action = Action("NORMAL ATTACK")
        action.execute(self, other)

    def normal_heal(self, other):
        # type: (LegendaryCreature) -> None
        action: Action = Action("NORMAL HEAL")
        action.execute(self, other)

    def use_skill(self, other, active_skill):
        # type: (LegendaryCreature, ActiveSkill) -> bool
        if active_skill not in self.__skills:
            return False

        if self.curr_magic_points < active_skill.magic_points_cost:
            return False

        action: Action = Action("USE SKILL")
        action.execute(self, other, active_skill)
        self.curr_magic_points -= active_skill.magic_points_cost
        return True

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

    def __init__(self, name, description, gold_cost, gem_cost):
        # type: (str, str, mpf, mpf) -> None
        self.name: str = name
        self.description: str = description
        self.gold_cost: mpf = gold_cost
        self.gem_cost: mpf = gem_cost
        self.sell_gold_gain: mpf = gold_cost / 5
        self.sell_gem_gain: mpf = gem_cost / 5

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
        # type: () -> Item
        return copy.deepcopy(self)


class Egg(Item):
    """
    This class contains attributes of an egg which can be hatched for legendary creatures to come out.
    """

    POTENTIAL_ELEMENTS: list = ["TERRA", "FLAME", "SEA", "NATURE", "ELECTRIC", "ICE", "METAL", "DARK", "LIGHT", "WAR",
                                "PURE", "LEGEND", "PRIMAL", "WIND", "BEAUTY", "MAGIC", "CHAOS", "HAPPY", "DREAM",
                                "SOUL"]

    def __init__(self, gold_cost, gem_cost, element):
        # type: (mpf, mpf, str) -> None
        Item.__init__(self, str(element if element in self.POTENTIAL_ELEMENTS else self.POTENTIAL_ELEMENTS[0]).upper() +
                      " EGG", "An egg which can be hatched for legendary creatures to come out.",
                      gold_cost, gem_cost)
        self.hatch_time: datetime or None = None  # initial value
        self.element: str = element
        self.already_placed: bool = False


class Rune(Item):
    """
    This class contains attributes of a rune used to strengthen legendary creatures.
    """

    MIN_SLOT_NUMBER: int = 1
    MAX_SLOT_NUMBER: int = 6
    MIN_RATING: int = 1
    MAX_RATING: int = 6
    POTENTIAL_SET_NAMES: list = ["ENERGY", "MAGIC", "FATAL", "BLADE", "SWIFT", "FOCUS", "GUARD", "ENDURE", "REVENGE",
                                 "VAMPIRE", "RAGE", "VIOLENT", "REFLECT", "RESIST", "DESPAIR"]
    POTENTIAL_MAIN_STATS: list = ["HP", "HP%", "MP", "MP%", "ATK", "ATK%", "DEF", "DEF%", "SPD", "CR", "CD", "RES",
                                  "ACC"]
    MAX_SUB_STATS: int = 4

    def __init__(self, name, description, gold_cost, gem_cost, rating, slot_number, set_name, main_stat):
        # type: (str, str, mpf, mpf, int, int, str, str) -> None
        Item.__init__(self, name, description, gold_cost, gem_cost)
        self.rating: int = rating if self.MIN_RATING <= rating <= self.MAX_RATING else self.MIN_RATING
        self.slot_number: int = slot_number if self.MIN_SLOT_NUMBER <= slot_number <= self.MAX_SLOT_NUMBER else \
            self.MIN_SLOT_NUMBER
        self.set_name: str = set_name if set_name in self.POTENTIAL_SET_NAMES else self.POTENTIAL_SET_NAMES[0]
        self.set_size: int = 4 if self.set_name in ["FATAL", "SWIFT", "VAMPIRE", "RAGE", "VIOLENT", "REFLECT",
                                                    "DESPAIR"] else 2
        self.main_stat: str = main_stat if main_stat in self.POTENTIAL_MAIN_STATS else self.POTENTIAL_MAIN_STATS[0]
        self.__sub_stats: list = []  # initial value
        self.set_effect_is_active: bool = False
        self.stat_increase: StatIncrease = self.__get_stat_increase()
        self.set_effect: SetEffect = self.__get_set_effect()
        self.level: int = 1
        self.level_up_gold_cost: mpf = gold_cost
        self.level_up_success_rate: mpf = mpf("1")
        self.already_placed: bool = False  # initial value

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

    def get_sub_stats(self):
        # type: () -> list
        return self.__sub_stats

    def __get_stat_increase(self):
        # type: () -> StatIncrease
        if self.main_stat == "HP":
            return StatIncrease(max_hp_up=mpf("10") ** (6 * self.rating))
        elif self.main_stat == "HP%":
            return StatIncrease(max_hp_percentage_up=mpf(2 * self.rating))
        elif self.main_stat == "MP":
            return StatIncrease(max_magic_points_up=mpf("10") ** (6 * self.rating))
        elif self.main_stat == "MP%":
            return StatIncrease(max_magic_points_percentage_up=mpf(2 * self.rating))
        elif self.main_stat == "ATK":
            return StatIncrease(attack_up=mpf("10") ** (5 * self.rating))
        elif self.main_stat == "ATK%":
            return StatIncrease(attack_percentage_up=mpf(2 * self.rating))
        elif self.main_stat == "DEF":
            return StatIncrease(defense_up=mpf("10") ** (5 * self.rating))
        elif self.main_stat == "DEF%":
            return StatIncrease(defense_percentage_up=mpf(2 * self.rating))
        elif self.main_stat == "SPD":
            return StatIncrease(attack_speed_up=mpf(2 * self.rating))
        elif self.main_stat == "CR":
            return StatIncrease(crit_rate_up=mpf(0.01 * self.rating))
        elif self.main_stat == "CD":
            return StatIncrease(crit_damage_up=mpf(0.05 * self.rating))
        elif self.main_stat == "RES":
            return StatIncrease(resistance_up=mpf(0.01 * self.rating))
        elif self.main_stat == "ACC":
            return StatIncrease(accuracy_up=mpf(0.01 * self.rating))
        return StatIncrease()

    def __get_set_effect(self):
        # type: () -> SetEffect
        if self.set_name == "ENERGY":
            return SetEffect(max_hp_percentage_up=mpf("15"))
        elif self.set_name == "MAGIC":
            return SetEffect(max_magic_points_percentage_up=mpf("15"))
        elif self.set_name == "FATAL":
            return SetEffect(attack_percentage_up=mpf("35"))
        elif self.set_name == "BLADE":
            return SetEffect(crit_rate_up=mpf("0.12"))
        elif self.set_name == "SWIFT":
            return SetEffect(attack_speed_percentage_up=mpf("25"))
        elif self.set_name == "FOCUS":
            return SetEffect(accuracy_up=mpf("0.2"))
        elif self.set_name == "GUARD":
            return SetEffect(defense_percentage_up=mpf("20"))
        elif self.set_name == "ENDURE":
            return SetEffect(resistance_up=mpf("0.2"))
        elif self.set_name == "REVENGE":
            return SetEffect(counterattack_chance_up=mpf("0.15"))
        elif self.set_name == "VAMPIRE":
            return SetEffect(life_drain_percentage_up=mpf("35"))
        elif self.set_name == "RAGE":
            return SetEffect(crit_damage_up=mpf("0.4"))
        elif self.set_name == "VIOLENT":
            return SetEffect(extra_turn_chance_up=mpf("0.22"))
        elif self.set_name == "REFLECT":
            return SetEffect(reflected_damage_percentage_up=mpf("35"))
        elif self.set_name == "RESIST":
            return SetEffect(crit_resist_up=mpf("0.15"))
        elif self.set_name == "DESPAIR":
            return SetEffect(stun_rate_up=mpf("0.25"))
        return SetEffect()

    def level_up(self):
        # type: () -> bool
        # Check whether levelling up is successful or not
        if random.random() > self.level_up_success_rate:
            return False

        # Increase the level of the rune
        self.level += 1

        # Update the cost and success rate of levelling up the rune
        self.level_up_gold_cost *= mpf("10") ** (self.level + self.rating)
        self.level_up_success_rate *= mpf("0.95")

        # Increase main stat attribute
        if self.main_stat == "HP":
            self.stat_increase.max_hp_up += mpf("10") ** (6 * self.rating + self.level)
        elif self.main_stat == "HP%":
            self.stat_increase.max_hp_percentage_up += self.rating
        elif self.main_stat == "MP":
            self.stat_increase.max_magic_points_up += mpf("10") ** (6 * self.rating + self.level)
        elif self.main_stat == "MP%":
            self.stat_increase.max_magic_points_percentage_up += self.rating
        elif self.main_stat == "ATK":
            self.stat_increase.attack_up += mpf("10") ** (5 * self.rating + 1)
        elif self.main_stat == "ATK%":
            self.stat_increase.attack_percentage_up += self.rating
        elif self.main_stat == "DEF":
            self.stat_increase.defense_up += mpf("10") ** (5 * self.rating + 1)
        elif self.main_stat == "DEF%":
            self.stat_increase.defense_percentage_up += self.rating
        elif self.main_stat == "SPD":
            self.stat_increase.attack_speed_up += 2 * self.rating
        elif self.main_stat == "CR":
            self.stat_increase.crit_rate_up += 0.01 * self.rating
        elif self.main_stat == "CD":
            self.stat_increase.crit_damage_up += 0.05 * self.rating
        elif self.main_stat == "RES":
            self.stat_increase.resistance_up += 0.01 * self.rating
        elif self.main_stat == "ACC":
            self.stat_increase.accuracy_up += 0.01 * self.rating
        else:
            print("Cannot increase rune main stat: " + str(self.main_stat) + "\n")

        # Add new sub-stat if possible.
        new_sub_stat: str = self.POTENTIAL_MAIN_STATS[random.randint(0, len(self.POTENTIAL_MAIN_STATS) - 1)]
        if new_sub_stat not in self.__sub_stats and len(self.__sub_stats) < self.MAX_SUB_STATS and \
                new_sub_stat != self.main_stat:
            self.__sub_stats.append(new_sub_stat)

        # Increase value of sub-stat attribute
        self.increase_substat_attribute(new_sub_stat)
        return True

    def increase_substat_attribute(self, substat_name):
        # type: (str) -> None
        if substat_name == "HP":
            self.stat_increase.max_hp_up += mpf("10") ** (6 * self.rating + self.level)
        elif substat_name == "HP%":
            self.stat_increase.max_hp_percentage_up += self.rating
        elif substat_name == "MP":
            self.stat_increase.max_magic_points_up += mpf("10") ** (6 * self.rating + self.level)
        elif substat_name == "MP%":
            self.stat_increase.max_magic_points_percentage_up += self.rating
        elif substat_name == "ATK":
            self.stat_increase.attack_up += mpf("10") ** (5 * self.rating + 1)
        elif substat_name == "ATK%":
            self.stat_increase.attack_percentage_up += self.rating
        elif substat_name == "DEF":
            self.stat_increase.defense_up += mpf("10") ** (5 * self.rating + 1)
        elif substat_name == "DEF%":
            self.stat_increase.defense_percentage_up += self.rating
        elif substat_name == "SPD":
            self.stat_increase.attack_speed_up += 2 * self.rating
        elif substat_name == "CR":
            self.stat_increase.crit_rate_up += 0.01 * self.rating
        elif substat_name == "CD":
            self.stat_increase.crit_damage_up += 0.05 * self.rating
        elif substat_name == "RES":
            self.stat_increase.resistance_up += 0.01 * self.rating
        elif substat_name == "ACC":
            self.stat_increase.accuracy_up += 0.01 * self.rating
        else:
            print("No such sub-stat: " + str(substat_name) + "\n")


class SetEffect:
    """
    This class contains attributes of the set effect of a rune.
    """

    def __init__(self, max_hp_percentage_up=mpf("0"), max_magic_points_percentage_up=mpf("0"),
                 attack_percentage_up=mpf("0"), defense_percentage_up=mpf("0"), attack_speed_percentage_up=mpf("0"),
                 crit_rate_up=mpf("0"), crit_damage_up=mpf("0"), resistance_up=mpf("0"), accuracy_up=mpf("0"),
                 extra_turn_chance_up=mpf("0"), counterattack_chance_up=mpf("0"),
                 reflected_damage_percentage_up=mpf("0"), life_drain_percentage_up=mpf("0"), crit_resist_up=mpf("0"),
                 stun_rate_up=mpf("0")):
        # type: (mpf, mpf, mpf, mpf, mpf, mpf, mpf, mpf, mpf, mpf, mpf, mpf, mpf, mpf, mpf) -> None
        self.max_hp_percentage_up: mpf = max_hp_percentage_up
        self.max_magic_points_percentage_up: mpf = max_magic_points_percentage_up
        self.attack_percentage_up: mpf = attack_percentage_up
        self.defense_percentage_up: mpf = defense_percentage_up
        self.attack_speed_percentage_up: mpf = attack_speed_percentage_up
        self.crit_rate_up: mpf = crit_rate_up
        self.crit_damage_up: mpf = crit_damage_up
        self.resistance_up: mpf = resistance_up
        self.accuracy_up: mpf = accuracy_up
        self.extra_turn_chance_up: mpf = extra_turn_chance_up
        self.counterattack_chance_up: mpf = counterattack_chance_up
        self.reflected_damage_percentage_up: mpf = reflected_damage_percentage_up
        self.life_drain_percentage_up: mpf = life_drain_percentage_up
        self.crit_resist_up: mpf = crit_resist_up
        self.stun_rate_up: mpf = stun_rate_up

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
        # type: () -> SetEffect
        return copy.deepcopy(self)


class StatIncrease:
    """
    This class contains attributes of the increase in stats of a rune.
    """

    def __init__(self, max_hp_up=mpf("0"), max_hp_percentage_up=mpf("0"), max_magic_points_up=mpf("0"),
                 max_magic_points_percentage_up=mpf("0"), attack_up=mpf("0"), attack_percentage_up=mpf("0"),
                 defense_up=mpf("0"), defense_percentage_up=mpf("0"), attack_speed_up=mpf("0"), crit_rate_up=mpf("0"),
                 crit_damage_up=mpf("0"), resistance_up=mpf("0"), accuracy_up=mpf("0")):
        # type: (mpf, mpf, mpf, mpf, mpf, mpf, mpf, mpf, mpf, mpf, mpf, mpf, mpf) -> None
        self.max_hp_up: mpf = max_hp_up
        self.max_hp_percentage_up: mpf = max_hp_percentage_up
        self.max_magic_points_up: mpf = max_magic_points_up
        self.max_magic_points_percentage_up: mpf = max_magic_points_percentage_up
        self.attack_up: mpf = attack_up
        self.attack_percentage_up: mpf = attack_percentage_up
        self.defense_up: mpf = defense_up
        self.defense_percentage_up: mpf = defense_percentage_up
        self.attack_speed_up: mpf = attack_speed_up
        self.crit_rate_up: mpf = crit_rate_up
        self.crit_damage_up: mpf = crit_damage_up
        self.resistance_up: mpf = resistance_up
        self.accuracy_up: mpf = accuracy_up

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
        # type: () -> StatIncrease
        return copy.deepcopy(self)


class AwakenShard(Item):
    """
    This class contains attributes of a shard used to awaken a legendary creature.
    """

    def __init__(self, gold_cost, gem_cost, legendary_creature_element):
        # type: (mpf, mpf, str) -> None
        Item.__init__(self, "AWAKEN SHARD", "A shard used to immediately awaken a legendary creature.", gold_cost,
                      gem_cost)
        self.legendary_creature_element: str = legendary_creature_element  # the element of the legendary creature
        # to be awakened


class EXPShard(Item):
    """
    This class contains attributes of a shard used to increase the EXP of legendary creatures.
    """

    def __init__(self, gold_cost, gem_cost, exp_granted):
        # type: (mpf, mpf, mpf) -> None
        Item.__init__(self, "EXP SHARD", "A shard used to immediately increase the EXP of a legendary creature.",
                      gold_cost, gem_cost)
        self.exp_granted: mpf = exp_granted


class LevelUpShard(Item):
    """
    This class contains attributes of a level up shard used to immediately level up a legendary creature.
    """

    def __init__(self, gold_cost, gem_cost):
        # type: (mpf, mpf) -> None
        Item.__init__(self, "LEVEL UP SHARD", "A shard used to immediately increase the level of a legendary creature.",
                      gold_cost, gem_cost)


class SkillLevelUpShard(Item):
    """
    This class contains attributes of a skill level up shard to level up skills owned by legendary creatures.
    """

    def __init__(self, gold_cost, gem_cost):
        # type: (mpf, mpf) -> None
        Item.__init__(self, "SKILL LEVEL UP SHARD", "A shard used to immediately increase the level of a "
                                                    "legendary creature' s skill.", gold_cost, gem_cost)


class Skill:
    """
    This class contains attributes of a skill legendary creatures have.
    """

    def __init__(self, name, description, magic_points_cost):
        # type: (str, str, mpf) -> None
        self.name: str = name
        self.description: str = description
        self.magic_points_cost: mpf = magic_points_cost
        self.level: int = 1
        self.is_active: bool = True

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

    def level_up(self):
        # type: () -> None
        pass

    def clone(self):
        # type: () -> Skill
        return copy.deepcopy(self)


class ActiveSkill(Skill):
    """
    This class contains attributes of an active skill legendary creatures have.
    """

    POSSIBLE_ACTIVE_SKILL_TYPES: list = ["ATTACK", "HEAL", "ALLIES EFFECT", "ENEMIES EFFECT"]

    def __init__(self, name, description, active_skill_type, is_aoe, magic_points_cost, max_cooltime, damage_multiplier,
                 beneficial_effects_to_allies, harmful_effects_to_enemies, allies_attack_gauge_up,
                 enemies_attack_gauge_down, heal_amount_to_allies, does_ignore_enemies_defense, does_ignore_shield,
                 does_ignore_invincibility):
        # type: (str, str, str, bool, mpf, int, DamageMultiplier, list, list, mpf, mpf, mpf, bool, bool, bool) -> None
        Skill.__init__(self, name, description, magic_points_cost)
        self.active_skill_type: str = active_skill_type if active_skill_type in self.POSSIBLE_ACTIVE_SKILL_TYPES \
            else self.POSSIBLE_ACTIVE_SKILL_TYPES[0]
        self.is_aoe: bool = is_aoe
        self.cooltime: int = max_cooltime
        self.max_cooltime: int = max_cooltime
        self.damage_multiplier: DamageMultiplier = damage_multiplier if self.active_skill_type == "ATTACK" else \
            DamageMultiplier()
        self.__beneficial_effects_to_allies: list = beneficial_effects_to_allies if self.active_skill_type == \
                                                                                    "ATTACK" or \
                                                                                    self.active_skill_type == \
                                                                                    "ALLIES EFFECT" else []
        self.__harmful_effects_to_enemies: list = harmful_effects_to_enemies if self.active_skill_type == "ATTACK" or \
                                                                                self.active_skill_type == \
                                                                                "ENEMIES EFFECT" else []
        self.allies_attack_gauge_up: mpf = allies_attack_gauge_up if self.active_skill_type == \
                                                                     "ALLIES EFFECT" else mpf("0")
        self.enemies_attack_gauge_down: mpf = enemies_attack_gauge_down if self.active_skill_type == "ATTACK" or \
                                                                           self.active_skill_type == "ENEMIES EFFECT" \
            else mpf("0")
        self.heal_amount_to_allies: mpf = heal_amount_to_allies if self.active_skill_type == \
                                                                   "HEAL" else mpf("0")
        self.does_ignore_enemies_defense: bool = does_ignore_enemies_defense
        self.does_ignore_shield: bool = does_ignore_shield
        self.does_ignore_invincibility: bool = does_ignore_invincibility

    def get_beneficial_effects_to_allies(self):
        # type: () -> list
        return self.__beneficial_effects_to_allies

    def get_harmful_effects_to_enemies(self):
        # type: () -> list
        return self.__harmful_effects_to_enemies

    def level_up(self):
        # type: () -> None
        self.level += 1
        self.damage_multiplier.multiplier_to_self_max_hp *= mpf("1.25")
        self.damage_multiplier.multiplier_to_enemy_max_hp *= mpf("1.25")
        self.damage_multiplier.multiplier_to_self_attack_power *= mpf("1.25")
        self.damage_multiplier.multiplier_to_enemy_attack_power *= mpf("1.25")
        self.damage_multiplier.multiplier_to_self_defense *= mpf("1.25")
        self.damage_multiplier.multiplier_to_enemy_defense *= mpf("1.25")
        self.damage_multiplier.multiplier_to_self_max_magic_points *= mpf("1.25")
        self.damage_multiplier.multiplier_to_enemy_max_magic_points *= mpf("1.25")
        self.damage_multiplier.multiplier_to_self_attack_speed *= mpf("1.25")
        self.damage_multiplier.multiplier_to_enemy_attack_speed *= mpf("1.25")
        self.damage_multiplier.multiplier_to_self_current_hp_percentage *= mpf("1.25")
        self.damage_multiplier.multiplier_to_self_hp_percentage_loss *= mpf("1.25")
        self.damage_multiplier.multiplier_to_enemy_current_hp_percentage *= mpf("1.25")


class PassiveSkill(Skill):
    """
    This class contains attributes of a passive skill legendary creatures have.
    """

    def __init__(self, name, description, passive_skill_effect):
        # type: (str, str, PassiveSkillEffect) -> None
        Skill.__init__(self, name, description, mpf("0"))
        self.passive_skill_effect: PassiveSkillEffect = passive_skill_effect


class PassiveSkillEffect:
    """
    This class contains attributes of the effect of a passive skill.
    """

    def __init__(self, max_hp_percentage_up=mpf("0"), max_magic_points_percentage_up=mpf("0"),
                 attack_power_percentage_up=mpf("0"), defense_percentage_up=mpf("0"),
                 attack_speed_percentage_up=mpf("0"), crit_rate_up=mpf("0"), crit_damage_up=mpf("0"),
                 resistance_up=mpf("0"), accuracy_up=mpf("0"), extra_turn_chance_up=mpf("0"),
                 beneficial_effects_to_allies=mpf("0"), harmful_effects_to_enemies=mpf("0"),
                 allies_attack_gauge_up=mpf("0"), enemies_attack_gauge_down=mpf("0"), heal_amount_to_allies=mpf("0")):
        # type: (mpf, mpf, mpf, mpf, mpf, mpf, mpf, mpf, mpf, mpf, list, list, mpf, mpf, mpf) -> None
        self.max_hp_percentage_up: mpf = max_hp_percentage_up
        self.max_magic_points_percentage_up: mpf = max_magic_points_percentage_up
        self.attack_power_percentage_up: mpf = attack_power_percentage_up
        self.defense_percentage_up: mpf = defense_percentage_up
        self.attack_speed_percentage_up: mpf = attack_speed_percentage_up
        self.crit_rate_up: mpf = crit_rate_up
        self.crit_damage_up: mpf = crit_damage_up
        self.resistance_up: mpf = resistance_up
        self.accuracy_up: mpf = accuracy_up
        self.extra_turn_chance_up: mpf = extra_turn_chance_up
        self.__beneficial_effects_to_allies: list = beneficial_effects_to_allies
        self.__harmful_effects_to_enemies: list = harmful_effects_to_enemies
        self.allies_attack_gauge_up: mpf = allies_attack_gauge_up
        self.enemies_attack_gauge_down: mpf = enemies_attack_gauge_down
        self.heal_amount_to_allies: mpf = heal_amount_to_allies

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

    def get_beneficial_effects_to_allies(self):
        # type: () -> list
        return self.__beneficial_effects_to_allies

    def get_harmful_effects_to_enemies(self):
        # type: () -> list
        return self.__harmful_effects_to_enemies

    def clone(self):
        # type: () -> PassiveSkillEffect
        return copy.deepcopy(self)


class LeaderSkill(Skill):
    """
    This class contains attributes of a leader skill legendary creatures have.
    """

    def __init__(self, name, description, magic_points_cost, leader_skill_effect):
        # type: (str, str, mpf, LeaderSkillEffect) -> None
        Skill.__init__(self, name, description, magic_points_cost)
        self.leader_skill_effect: LeaderSkillEffect = leader_skill_effect


class LeaderSkillEffect:
    """
    This class contains attributes of the effect of a leader skill.
    """

    def __init__(self, max_hp_percentage_up=mpf("0"), max_magic_points_percentage_up=mpf("0"),
                 attack_power_percentage_up=mpf("0"), defense_percentage_up=mpf("0"),
                 attack_speed_percentage_up=mpf("0"), crit_rate_up=mpf("0"), crit_damage_up=mpf("0"),
                 resistance_up=mpf("0"), accuracy_up=mpf("0")):
        # type: (mpf, mpf, mpf, mpf, mpf, mpf, mpf, mpf, mpf) -> None
        self.max_hp_percentage_up: mpf = max_hp_percentage_up
        self.max_magic_points_percentage_up: mpf = max_magic_points_percentage_up
        self.attack_power_percentage_up: mpf = attack_power_percentage_up
        self.defense_percentage_up: mpf = defense_percentage_up
        self.attack_speed_percentage_up: mpf = attack_speed_percentage_up
        self.crit_rate_up: mpf = crit_rate_up
        self.crit_damage_up: mpf = crit_damage_up
        self.resistance_up: mpf = resistance_up
        self.accuracy_up: mpf = accuracy_up

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
        # type: () -> LeaderSkillEffect
        return copy.deepcopy(self)


class DamageMultiplier:
    """
    This class contains attributes of the damage multiplier of a skill.
    """

    def __init__(self, multiplier_to_self_max_hp=mpf("0"), multiplier_to_enemy_max_hp=mpf("0"),
                 multiplier_to_self_attack_power=mpf("0"), multiplier_to_enemy_attack_power=mpf("0"),
                 multiplier_to_self_defense=mpf("0"), multiplier_to_enemy_defense=mpf("0"),
                 multiplier_to_self_max_magic_points=mpf("0"), multiplier_to_enemy_max_magic_points=mpf("0"),
                 multiplier_to_self_attack_speed=mpf("0"), multiplier_to_enemy_attack_speed=mpf("0"),
                 multiplier_to_self_current_hp_percentage=mpf("0"), multiplier_to_self_hp_percentage_loss=mpf("0"),
                 multiplier_to_enemy_current_hp_percentage=mpf("0")):
        # type: (mpf, mpf, mpf, mpf, mpf, mpf, mpf, mpf, mpf, mpf, mpf, mpf, mpf) -> None
        self.multiplier_to_self_max_hp: mpf = multiplier_to_self_max_hp
        self.multiplier_to_enemy_max_hp: mpf = multiplier_to_enemy_max_hp
        self.multiplier_to_self_attack_power: mpf = multiplier_to_self_attack_power
        self.multiplier_to_enemy_attack_power: mpf = multiplier_to_enemy_attack_power
        self.multiplier_to_self_defense: mpf = multiplier_to_self_defense
        self.multiplier_to_enemy_defense: mpf = multiplier_to_enemy_defense
        self.multiplier_to_self_max_magic_points: mpf = multiplier_to_self_max_magic_points
        self.multiplier_to_enemy_max_magic_points: mpf = multiplier_to_enemy_max_magic_points
        self.multiplier_to_self_attack_speed: mpf = multiplier_to_self_attack_speed
        self.multiplier_to_enemy_attack_speed: mpf = multiplier_to_enemy_attack_speed
        self.multiplier_to_self_current_hp_percentage: mpf = multiplier_to_self_current_hp_percentage
        self.multiplier_to_self_hp_percentage_loss: mpf = multiplier_to_self_hp_percentage_loss
        self.multiplier_to_enemy_current_hp_percentage: mpf = multiplier_to_enemy_current_hp_percentage

    def calculate_raw_damage_without_enemy_defense_invincibility_shield(self, user, target):
        # type: (LegendaryCreature, LegendaryCreature) -> mpf
        self_current_hp_percentage: mpf = (user.curr_hp / user.max_hp) * 100
        self_hp_percentage_loss: mpf = 100 - self_current_hp_percentage
        target_current_hp_percentage: mpf = (target.curr_hp / target.max_hp) * 100
        return (user.max_hp * (1 + user.max_hp_percentage_up / 100) * self.multiplier_to_self_max_hp +
                target.max_hp * self.multiplier_to_enemy_max_hp * (1 + target.max_hp_percentage_up / 100) +
                user.attack_power * (1 + user.attack_power_percentage_up / 100 -
                                     user.attack_power_percentage_down / 100) *
                (self.multiplier_to_self_attack_speed * user.attack_speed * (1 + user.attack_speed_percentage_up / 100 -
                                                                             user.attack_speed_percentage_down / 100))
                * self.multiplier_to_self_attack_power + target.attack_power * (
                        1 + target.attack_power_percentage_up / 100
                        - target.attack_power_percentage_down / 100) + target.attack_power * (1 +
                                                                                              target.attack_power_percentage_up / 100 - target.attack_power_percentage_down / 100) *
                (self.multiplier_to_enemy_attack_speed * target.attack_speed * (1 + target.attack_speed_percentage_up /
                                                                                100 - target.attack_speed_percentage_down / 100)) * self.multiplier_to_enemy_attack_power
                + user.defense * (1 + user.defense_percentage_up / 100 -
                                  user.defense_percentage_down / 100) * self.multiplier_to_self_defense +
                target.defense * (1 + target.defense_percentage_up / 100 - target.defense_percentage_down / 100) *
                self.multiplier_to_enemy_defense + user.max_magic_points * (1 + user.max_magic_points_percentage_up
                                                                            / 100) *
                self.multiplier_to_self_max_magic_points + target.max_magic_points * (1 +
                                                                                      target.max_magic_points_percentage_up / 100) *
                self.multiplier_to_enemy_max_magic_points) * (1 + self_current_hp_percentage *
                                                              self.multiplier_to_self_current_hp_percentage) * (
                       1 + self_hp_percentage_loss *
                       self.multiplier_to_self_hp_percentage_loss) * (1 + target_current_hp_percentage *
                                                                      self.multiplier_to_enemy_current_hp_percentage) * (
                       1 + target.damage_received_percentage_up / 100)

    def calculate_raw_damage(self, user, target, does_ignore_defense=False, does_ignore_shield=False,
                             does_ignore_invincibility=False):
        # type: (LegendaryCreature, LegendaryCreature, bool, bool, bool) -> mpf
        damage_reduction_factor: mpf = mpf("1") if does_ignore_defense else mpf("1e8") / (mpf("1e8") +
                                                                                          3.5 * target.defense)
        raw_damage: mpf = self.calculate_raw_damage_without_enemy_defense_invincibility_shield(user, target)
        if not does_ignore_shield and target.shield_percentage > 0:
            raw_damage *= (1 - target.shield_percentage / 100)

        if not (does_ignore_invincibility or target.can_receive_damage):
            return mpf("0")

        # Checking for damage multiplier by element
        damage_multiplier_by_element: mpf = mpf("0")  # initial value
        for element in user.get_elements():
            curr_multiplier: mpf = get_elemental_damage_multiplier(element, target.get_elements()[0])
            if curr_multiplier > damage_multiplier_by_element:
                damage_multiplier_by_element = curr_multiplier

        # Checking for critical hits
        crit_chance: mpf = user.crit_rate + user.crit_rate_up - target.crit_resist - target.crit_resist_up
        if crit_chance < LegendaryCreature.MIN_CRIT_RATE:
            crit_chance = LegendaryCreature.MIN_CRIT_RATE

        is_crit: bool = random.random() < crit_chance
        return raw_damage * damage_reduction_factor if not is_crit else raw_damage * (user.crit_damage +
                                                                                      user.crit_damage_up) * \
                                                                        damage_reduction_factor * \
                                                                        damage_multiplier_by_element

    def clone(self):
        # type: () -> DamageMultiplier
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


class BeneficialEffect:
    """
    This class contains attributes of a beneficial effect a legendary creature has.
    """

    POSSIBLE_NAMES: list = ["INCREASE_ATK", "INCREASE_DEF", "INCREASE_SPD", "INCREASE_CRIT_RATE", "IMMUNITY",
                            "INVINCIBILITY", "HEAL_OVER_TIME", "COUNTER", "REFLECT", "VAMPIRE",
                            "INCREASE_CRIT_RESIST", "SHIELD", "ENDURE"]

    def __init__(self, name, number_of_turns):
        # type: (str, int) -> None
        self.name: str = name if name in self.POSSIBLE_NAMES else self.POSSIBLE_NAMES[0]
        self.number_of_turns: int = number_of_turns
        self.attack_power_percentage_up: mpf = mpf("50") if self.name == "INCREASE_ATK" else mpf("0")
        self.attack_speed_percentage_up: mpf = mpf("33") if self.name == "INCREASE_SPD" else mpf("0")
        self.defense_percentage_up: mpf = mpf("50") if self.name == "INCREASE_DEF" else mpf("0")
        self.crit_rate_up: mpf = mpf("0.3") if self.name == "INCREASE_CRIT_RATE" else mpf("0")
        self.prevents_damage: bool = self.name == "INVINCIBILITY"
        self.blocks_debuffs: bool = self.name == "IMMUNITY"
        self.prevents_death: bool = self.name == "ENDURE"
        self.heal_percentage_per_turn: mpf = mpf("15") if self.name == "HEAL_OVER_TIME" else mpf("0")
        self.counterattack_chance_up: mpf = mpf("1") if self.name == "COUNTER" else mpf("0")
        self.reflected_damage_percentage_up: mpf = mpf("33") if self.name == "REFLECT" else mpf("0")
        self.life_drain_percentage_up: mpf = mpf("33") if self.name == "VAMPIRE" else mpf("0")
        self.crit_resist_up: mpf = mpf("0.5") if self.name == "INCREASE_CRIT_RESIST" else mpf("0")
        self.shield_percentage_up: mpf = mpf("15") if self.name == "SHIELD" else mpf("0")
        self.can_be_stacked: bool = self.name == "HEAL_OVER_TIME"

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
        # type: () -> BeneficialEffect
        return copy.deepcopy(self)


class HarmfulEffect:
    """
    This class contains attributes of a harmful effect a legendary creature has.
    """

    POSSIBLE_NAMES: list = ["DECREASE_ATK", "DECREASE_DEF", "DECREASE_SPD", "BLOCK_BENEFICIAL_EFFECTS",
                            "BRAND", "UNRECOVERABLE", "OBLIVION", "SILENCE", "DAMAGE_OVER_TIME", "STUN"]

    def __init__(self, name, number_of_turns):
        # type: (str, int) -> None
        self.name: str = name if name in self.POSSIBLE_NAMES else self.POSSIBLE_NAMES[0]
        self.number_of_turns: int = number_of_turns
        self.attack_power_percentage_down: mpf = mpf("50") if self.name == "DECREASE_ATK" else mpf("0")
        self.attack_speed_percentage_down: mpf = mpf("33") if self.name == "DECREASE_SPD" else mpf("0")
        self.defense_percentage_down: mpf = mpf("50") if self.name == "DECREASE_DEF" else mpf("0")
        self.blocks_beneficial_effects: bool = self.name == "BLOCK_BENEFICIAL_EFFECTS"
        self.damage_received_percentage_up: mpf = mpf("25") if self.name == "BRAND" else mpf("0")
        self.blocks_heal: bool = self.name == "UNRECOVERABLE"
        self.blocks_passive_skills: bool = self.name == "OBLIVION"
        self.blocks_skills_with_cooltime: bool = self.name == "SILENCE"
        self.damage_percentage_per_turn: mpf = mpf("5") if self.name == "DAMAGE_OVER_TIME" else mpf("0")
        self.prevents_moves: bool = self.name == "STUN"
        self.can_be_stacked: bool = self.name == "DAMAGE_OVER_TIME"

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
        # type: () -> HarmfulEffect
        return copy.deepcopy(self)


class Building:
    """
    This class contains attributes of a building which can be built on a city tile.
    """

    def __init__(self, name, description, gold_cost, gem_cost):
        # type: (str, str, mpf, mpf) -> None
        self.name: str = name
        self.description: str = description
        self.gold_cost: mpf = gold_cost
        self.gem_cost: mpf = gem_cost
        self.sell_gold_gain: mpf = gold_cost / 5
        self.sell_gem_gain: mpf = gem_cost / 5
        self.upgrade_gold_cost: mpf = gold_cost
        self.upgrade_gem_cost: mpf = gem_cost
        self.level: int = 1

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

    def level_up(self):
        # type: () -> None
        pass

    def clone(self):
        # type: () -> Building
        return copy.deepcopy(self)


class Hatchery(Building):
    """
    This class contains attributes of a hatchery used to hatch eggs of legendary creatures.
    """

    MAX_EGGS: int = 5

    def __init__(self, gold_cost, gem_cost):
        # type: (mpf, mpf) -> None
        Building.__init__(self, "HATCHERY", "A hatchery to hatch eggs and gain new legendary creatures.",
                          gold_cost, gem_cost)
        self.__eggs_placed: list = []  # initial value
        self.upgrade_gold_cost = mpf("0")
        self.upgrade_gem_cost = mpf("0")

    def get_eggs_placed(self):
        # type: () -> list
        return self.__eggs_placed

    def add_egg(self, egg):
        # type: (Egg) -> bool
        if len(self.__eggs_placed) < self.MAX_EGGS:
            self.__eggs_placed.append(egg)
            return True
        return False

    def remove_egg(self, egg):
        # type: (Egg) -> bool
        if egg in self.__eggs_placed:
            self.__eggs_placed.remove(egg)
            return True
        return False


class TrainingArea(Building):
    """
    This class contains attributes of a training area to automatically increase the EXP of legendary creatures.
    """

    MAX_LEGENDARY_CREATURES: int = 5

    def __init__(self, gold_cost, gem_cost):
        # type: (mpf, mpf) -> None
        Building.__init__(self, "TRAINING AREA", "A training area to increase the EXP of legendary creatures.",
                          gold_cost, gem_cost)
        self.legendary_creature_exp_per_second: mpf = self.gold_cost / mpf("1e5")
        self.__legendary_creatures_placed: list = []  # initial value

    def level_up(self):
        # type: () -> None
        self.level += 1
        self.legendary_creature_exp_per_second *= mpf("10") ** self.level
        self.upgrade_gold_cost *= mpf("10") ** self.level
        self.upgrade_gem_cost *= mpf("10") ** self.level

    def get_legendary_creatures_placed(self):
        # type: () -> list
        return self.__legendary_creatures_placed

    def add_legendary_creature(self, legendary_creature):
        # type: (LegendaryCreature) -> bool
        if len(self.__legendary_creatures_placed) < self.MAX_LEGENDARY_CREATURES:
            self.__legendary_creatures_placed.append(legendary_creature)
            return True
        return False

    def remove_legendary_creature(self, legendary_creature):
        # type: (LegendaryCreature) -> bool
        if legendary_creature in self.__legendary_creatures_placed:
            self.__legendary_creatures_placed.remove(legendary_creature)
            return True
        return False


class Tree(Building):
    """
    This class contains attributes of a tree used to decorate a section.
    """

    def __init__(self, gold_cost, gem_cost):
        # type: (mpf, mpf) -> None
        Building.__init__(self, "TREE", "A tree.", gold_cost, gem_cost)


class Guardstone(Building):
    """
    This class contains attributes of a building used to increase the defense of all legendary creatures.
    """

    def __init__(self, gold_cost, gem_cost):
        # type: (mpf, mpf) -> None
        Building.__init__(self, "GUARDSTONE", "A building used to increase the defense of all legendary creatures.",
                          gold_cost, gem_cost)
        self.legendary_creature_defense_percentage_up: mpf = mpf("3")

    def level_up(self):
        # type: () -> None
        self.level += 1
        self.legendary_creature_defense_percentage_up += mpf("3")
        self.upgrade_gold_cost *= mpf("10") ** self.level
        self.upgrade_gem_cost *= mpf("10") ** self.level


class LegendaryCreatureSanctuary(Building):
    """
    This class contains attributes of a building used to increase the attack power of all legendary creatures.
    """

    def __init__(self, gold_cost, gem_cost):
        # type: (mpf, mpf) -> None
        Building.__init__(self, "LEGENDARY CREATURE SANCTUARY", "A building used to increase the attack power of all "
                                                                "legendary creatures.",
                          gold_cost, gem_cost)
        self.legendary_creature_attack_power_percentage_up: mpf = mpf("3")

    def level_up(self):
        # type: () -> None
        self.level += 1
        self.legendary_creature_attack_power_percentage_up += mpf("3")
        self.upgrade_gold_cost *= mpf("10") ** self.level
        self.upgrade_gem_cost *= mpf("10") ** self.level


class SurvivalAltar(Building):
    """
    This class contains attributes of a building used to increase the maximum HP of all legendary creatures.
    """

    def __init__(self, gold_cost, gem_cost):
        # type: (mpf, mpf) -> None
        Building.__init__(self, "SURVIVAL ALTAR", "A building used to increase the maximum HP of all legendary "
                                                  "creatures.", gold_cost, gem_cost)
        self.legendary_creature_max_hp_percentage_up: mpf = mpf("3")

    def level_up(self):
        # type: () -> None
        self.level += 1
        self.legendary_creature_max_hp_percentage_up += mpf("3")
        self.upgrade_gold_cost *= mpf("10") ** self.level
        self.upgrade_gem_cost *= mpf("10") ** self.level


class MagicAltar(Building):
    """
    This class contains attributes of a building used to increase the maximum magic points of all legendary creatures.
    """

    def __init__(self, gold_cost, gem_cost):
        # type: (mpf, mpf) -> None
        Building.__init__(self, "MAGIC ALTAR", "A building used to increase the maximum magic points of all "
                                               "legendary creatures.", gold_cost, gem_cost)
        self.legendary_creature_max_magic_points_percentage_up: mpf = mpf("3")

    def level_up(self):
        # type: () -> None
        self.level += 1
        self.legendary_creature_max_magic_points_percentage_up += mpf("3")
        self.upgrade_gold_cost *= mpf("10") ** self.level
        self.upgrade_gem_cost *= mpf("10") ** self.level


class BoosterTower(Building):
    """
    This class contains attributes of a building used to increase the attack speed of all legendary creatures.
    """

    def __init__(self, gold_cost, gem_cost):
        # type: (mpf, mpf) -> None
        Building.__init__(self, "BOOSTER TOWER", "A building used to increase the attack speed of all legendary "
                                                 "creatures.", gold_cost, gem_cost)
        self.legendary_creature_attack_speed_percentage_up: mpf = mpf("3")

    def level_up(self):
        # type: () -> None
        self.level += 1
        self.legendary_creature_attack_speed_percentage_up += mpf("3")
        self.upgrade_gold_cost *= mpf("10") ** self.level
        self.upgrade_gem_cost *= mpf("10") ** self.level


class PlayerEXPTower(Building):
    """
    This class contains attributes of a tower producing EXP for the player.
    """

    def __init__(self, gold_cost, gem_cost):
        # type: (mpf, mpf) -> None
        Building.__init__(self, "PLAYER EXP TOWER", "A tower producing EXP for the player.", gold_cost, gem_cost)
        self.exp_per_second: mpf = self.gold_cost / mpf("1e5")

    def level_up(self):
        # type: () -> None
        self.level += 1
        self.exp_per_second *= mpf("10") ** self.level
        self.upgrade_gold_cost *= mpf("10") ** self.level
        self.upgrade_gem_cost *= mpf("10") ** self.level


class FoodFarm(Building):
    """
    This class contains attributes of a food farm producing food.
    """

    def __init__(self, gold_cost, gem_cost):
        # type: (mpf, mpf) -> None
        Building.__init__(self, "FOOD FARM", "A farm producing food.", gold_cost, gem_cost)
        self.food_per_second: mpf = self.gold_cost / mpf("1e5")

    def level_up(self):
        # type: () -> None
        self.level += 1
        self.food_per_second *= mpf("10") ** self.level
        self.upgrade_gold_cost *= mpf("10") ** self.level
        self.upgrade_gem_cost *= mpf("10") ** self.level


class GoldMine(Building):
    """
    This class contains attributes of a gold mine producing gold.
    """

    def __init__(self, gold_cost, gem_cost):
        # type: (mpf, mpf) -> None
        Building.__init__(self, "GOLD MINE", "A mine producing gold.", gold_cost, gem_cost)
        self.gold_per_second: mpf = self.gold_cost / mpf("1e5")

    def level_up(self):
        # type: () -> None
        self.level += 1
        self.gold_per_second *= mpf("10") ** self.level
        self.upgrade_gold_cost *= mpf("10") ** self.level
        self.upgrade_gem_cost *= mpf("10") ** self.level


class GemMine(Building):
    """
    This class contains attributes of a gem mine producing gems.
    """

    def __init__(self, gold_cost, gem_cost):
        # type: (mpf, mpf) -> None
        Building.__init__(self, "GEM MINE", "A mine producing gems.", gold_cost, gem_cost)
        self.gem_per_second: mpf = self.gold_cost / mpf("1e7")

    def level_up(self):
        # type: () -> None
        self.level += 1
        self.gem_per_second *= mpf("10") ** self.level
        self.upgrade_gold_cost *= mpf("10") ** self.level
        self.upgrade_gem_cost *= mpf("10") ** self.level


class PowerUpCircle(Building):
    """
    This class contains attributes of a power-up circle used to power up and evolve legendary creatures.
    """

    MAX_MATERIAL_LEGENDARY_CREATURES: int = 5

    def __init__(self, gold_cost, gem_cost):
        # type: (mpf, mpf) -> None
        Building.__init__(self, "POWER UP CIRCLE", "A building used to power up and evolve legendary creatures.",
                          gold_cost, gem_cost)
        self.legendary_creature_to_power_up: LegendaryCreature or None = None
        self.__material_legendary_creatures: list = []  # initial value
        self.upgrade_gold_cost = mpf("0")
        self.upgrade_gem_cost = mpf("0")

    def execute_power_up(self):
        # type: () -> LegendaryCreature or None
        if isinstance(self.legendary_creature_to_power_up, LegendaryCreature):
            curr_legendary_creature: LegendaryCreature = self.legendary_creature_to_power_up
            for legendary_creature in self.__material_legendary_creatures:
                curr_legendary_creature.exp += legendary_creature.rating * legendary_creature.exp
                curr_legendary_creature.level_up()

            self.deselect_legendary_creature_to_power_up()
            self.set_material_legendary_creatures([])
            return curr_legendary_creature
        return None

    def execute_evolution(self):
        # type: () -> LegendaryCreature or None
        if isinstance(self.legendary_creature_to_power_up, LegendaryCreature):
            curr_legendary_creature: LegendaryCreature = self.legendary_creature_to_power_up

            # Evolve the legendary creature if there are sufficient material legendary creatures of the
            # same or higher rating as the legendary creature to be evolved
            num_materials: int = sum(1 for legendary_creature in self.__material_legendary_creatures if
                                     legendary_creature.rating >= curr_legendary_creature.rating)
            if len(self.__material_legendary_creatures) == curr_legendary_creature.rating - 1 and \
                    num_materials == curr_legendary_creature.rating - 1:
                curr_legendary_creature.evolve()

            self.deselect_legendary_creature_to_power_up()
            self.set_material_legendary_creatures([])
            return curr_legendary_creature
        return None

    def get_material_legendary_creatures(self):
        # type: () -> list
        return self.__material_legendary_creatures

    def set_material_legendary_creatures(self, material_legendary_creatures):
        # type: (list) -> None
        self.__material_legendary_creatures = material_legendary_creatures

    def select_legendary_creature_to_power_up(self, legendary_creature):
        # type: (LegendaryCreature) -> bool
        if self.legendary_creature_to_power_up is None:
            self.legendary_creature_to_power_up = legendary_creature
            return True
        return False

    def deselect_legendary_creature_to_power_up(self):
        # type: () -> bool
        if isinstance(self.legendary_creature_to_power_up, LegendaryCreature):
            self.legendary_creature_to_power_up = None
            return True
        return False

    def add_legendary_creature(self, legendary_creature):
        # type: (LegendaryCreature) -> bool
        if len(self.__material_legendary_creatures) < self.MAX_MATERIAL_LEGENDARY_CREATURES:
            self.__material_legendary_creatures.append(legendary_creature)
            return True
        return False

    def remove_legendary_creature(self, legendary_creature):
        # type: (LegendaryCreature) -> bool
        if legendary_creature in self.__material_legendary_creatures:
            self.__material_legendary_creatures.remove(legendary_creature)
            return True
        return False


class Habitat(Building):
    """
    This class contains attributes of a habitat where legendary creatures live.
    """

    POTENTIAL_ELEMENTS: list = ["TERRA", "FLAME", "SEA", "NATURE", "ELECTRIC", "ICE", "METAL", "DARK", "LIGHT", "WAR",
                                "PURE", "LEGEND", "PRIMAL", "WIND", "BEAUTY", "MAGIC", "CHAOS", "HAPPY", "DREAM",
                                "SOUL"]
    MAX_LEGENDARY_CREATURES: int = 10

    def __init__(self, gold_cost, gem_cost, element, player_gold_per_second_increase):
        # type: (mpf, mpf, str, mpf) -> None
        Building.__init__(self, str(element if element in self.POTENTIAL_ELEMENTS else
                                    self.POTENTIAL_ELEMENTS[0]).upper() +
                          " HABITAT", "A habitat for " + str(element) +
                          " legendary creatures.", gold_cost, gem_cost)
        self.element: str = element if element in self.POTENTIAL_ELEMENTS else self.POTENTIAL_ELEMENTS[0]
        self.player_gold_per_second_increase: mpf = player_gold_per_second_increase
        self.__legendary_creatures_placed: list = []  # initial value

    def get_legendary_creatures_placed(self):
        # type: () -> list
        return self.__legendary_creatures_placed

    def add_legendary_creature(self, legendary_creature):
        # type: (LegendaryCreature) -> bool
        if len(self.__legendary_creatures_placed) < self.MAX_LEGENDARY_CREATURES:
            self.__legendary_creatures_placed.append(legendary_creature)
            return True
        return False

    def remove_legendary_creature(self, legendary_creature):
        # type: (LegendaryCreature) -> bool
        if legendary_creature in self.__legendary_creatures_placed:
            self.__legendary_creatures_placed.remove(legendary_creature)
            return True
        return False

    def level_up(self):
        # type: () -> None
        self.level += 1
        self.player_gold_per_second_increase *= mpf("10") ** (self.level / 2)
        self.upgrade_gold_cost *= mpf("10") ** self.level
        self.upgrade_gem_cost *= mpf("10") ** self.level


class Obstacle(Building):
    """
    This class contains attributes of an obstacle to be removed by the player.
    """

    def __init__(self):
        # type: () -> None
        Building.__init__(self, "OBSTACLE", "A removable obstacle.", mpf("0"), mpf("0"))
        self.remove_gold_gain: mpf = mpf("10") ** random.randint(5, 10)
        self.remove_gem_gain: mpf = mpf("10") ** random.randint(2, 6)


class TempleOfWishes(Building):
    """
    This class contains attributes of a temple of wishes where the player can make wishes to get random rewards.
    """

    def __init__(self, gold_cost, gem_cost, obtainable_objects):
        # type: (mpf, mpf, list) -> None
        Building.__init__(self, "TEMPLE OF WISHES", "A building where the player can make wishes to get random rewards",
                          gold_cost, gem_cost)
        self.__obtainable_objects: list = obtainable_objects
        self.wishes_left: int = 3  # The number of wishes a player can make in a day.
        self.already_reset: bool = False
        self.upgrade_gold_cost = mpf("0")
        self.upgrade_gem_cost = mpf("0")

    def reset_wishes_left(self):
        # type: () -> bool
        time_now: datetime = datetime.now()
        if not self.already_reset and time_now.hour > 0:
            self.already_reset = True
            self.wishes_left = 3
            return True
        return False

    def restore(self):
        # type: () -> None
        self.already_reset = False

    def get_obtainable_objects(self):
        # type: () -> list
        return self.__obtainable_objects


class FusionCenter(Building):
    """
    This class contains attributes of a building used to fuse legendary creatures.
    """

    def __init__(self, gold_cost, gem_cost):
        # type: (mpf, mpf) -> None
        Building.__init__(self, "FUSION CENTER", "A building used to fuse legendary creatures into a stronger one.",
                          gold_cost, gem_cost)
        self.upgrade_gold_cost = mpf("0")
        self.upgrade_gem_cost = mpf("0")


class ItemShop:
    """
    This class contains attributes of a shop selling items.
    """

    def __init__(self, items_sold):
        # type: (list) -> None
        self.name: str = "ITEM SHOP"
        self.__items_sold: list = items_sold

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

    def get_items_sold(self):
        # type: () -> list
        return self.__items_sold

    def clone(self):
        # type: () -> ItemShop
        return copy.deepcopy(self)


class BuildingShop:
    """
    This class contains attributes of a shop selling buildings.
    """

    def __init__(self, buildings_sold):
        # type: (list) -> None
        self.name: str = "BUILDING SHOP"
        self.__buildings_sold: list = buildings_sold

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

    def get_buildings_sold(self):
        # type: () -> list
        return self.__buildings_sold

    def clone(self):
        # type: () -> BuildingShop
        return copy.deepcopy(self)


class Reward:
    """
    This class contains attributes of the rewards gained for doing something in this game.
    """

    def __init__(self, player_reward_exp=mpf("0"), player_reward_gold=mpf("0"), player_reward_gems=mpf("0"),
                 legendary_creature_reward_exp=mpf("0"), player_reward_items=None):
        # type: (mpf, mpf, mpf, mpf, list) -> None
        if player_reward_items is None:
            player_reward_items = []

        self.player_reward_exp: mpf = player_reward_exp
        self.player_reward_gold: mpf = player_reward_gold
        self.player_reward_gems: mpf = player_reward_gems
        self.legendary_creature_reward_exp: mpf = legendary_creature_reward_exp
        self.__player_reward_items: list = player_reward_items

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

    def get_player_reward_items(self):
        # type: () -> list
        return self.__player_reward_items

    def clone(self):
        # type: () -> Reward
        return copy.deepcopy(self)


class Game:
    """
    This class contains attributes of the saved game data.
    """

    def __init__(self, player_data, item_shop, building_shop, battle_arena, minigames):
        # type: (Player, ItemShop, BuildingShop, Arena, list) -> None
        self.player_data: Player = player_data
        self.item_shop: ItemShop = item_shop
        self.building_shop: BuildingShop = building_shop
        self.battle_arena: Arena = battle_arena
        self.__minigames: list = minigames

    def get_minigames(self):
        # type: () -> list
        return self.__minigames

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
        # type: () -> Game
        return copy.deepcopy(self)


# Initialising global variables for the saved game data
# 1. The item shop
runes: list = []  # initial value
for rating in range(Rune.MIN_RATING, Rune.MAX_RATING + 1):
    for slot_number in range(Rune.MIN_SLOT_NUMBER, Rune.MAX_SLOT_NUMBER + 1):
        for set_name in Rune.POTENTIAL_SET_NAMES:
            for main_stat in Rune.POTENTIAL_MAIN_STATS:
                name: str = str(rating) + "-STAR " + str(set_name).upper() + " RUNE - SLOT " + str(slot_number)
                description: str = str(set_name).upper() + " rune of rating " + str(rating) + " at slot " + \
                                   str(slot_number)
                gold_cost: mpf = mpf("10") ** (6 + 5 * (rating - 1))
                gem_cost: mpf = 0 if rating == 1 else 10 * triangular(rating)
                new_rune: Rune = Rune(name, description, gold_cost, gem_cost, rating, slot_number, set_name,
                                      main_stat)
                runes.append(new_rune)

eggs: list = []  # initial value
for element in Egg.POTENTIAL_ELEMENTS:
    new_egg: Egg = Egg(mpf("8e5"), mpf("8"), element)
    eggs.append(new_egg)

awaken_shards: list = []  # initial value
for element in Egg.POTENTIAL_ELEMENTS:
    new_awaken_shard: AwakenShard = AwakenShard(mpf("1e6"), mpf("10"), element)
    awaken_shards.append(new_awaken_shard)

items: list = [rune for rune in runes] + [egg for egg in eggs] + \
              [awaken_shard for awaken_shard in awaken_shards]
items = items + [EXPShard(mpf("1e6"), mpf("10"), mpf("1e5")),
                 LevelUpShard(mpf("1e6"), mpf("10")),
                 SkillLevelUpShard(mpf("1e6"), mpf("10"))]
item_shop: ItemShop = ItemShop(items)

# 2. The building shop
habitats: list = []  # initial value
for element in Egg.POTENTIAL_ELEMENTS:
    new_habitat: Habitat = Habitat(mpf("1e5"), mpf("1"), element, mpf("1e3"))
    habitats.append(new_habitat)

building_shop: BuildingShop = BuildingShop([
                                               Hatchery(mpf("1e5"), mpf("1")),
                                               TrainingArea(mpf("1e8"), mpf("1000")),
                                               Tree(mpf("1e4"), mpf("0")),
                                               Guardstone(mpf("1e7"), mpf("100")),
                                               LegendaryCreatureSanctuary(mpf("1e7"), mpf("100")),
                                               SurvivalAltar(mpf("1e7"), mpf("100")),
                                               MagicAltar(mpf("1e7"), mpf("100")),
                                               BoosterTower(mpf("1e7"), mpf("100")),
                                               PlayerEXPTower(mpf("1e7"), mpf("100")),
                                               FoodFarm(mpf("1e6"), mpf("10")),
                                               GoldMine(mpf("1e6"), mpf("10")),
                                               GemMine(mpf("1e6"), mpf("10")),
                                               PowerUpCircle(mpf("1e5"), mpf("1")),
                                               FusionCenter(mpf("1e8"), mpf("1000")),
                                               TempleOfWishes(mpf("1e5"), mpf("1"),
                                                              [Reward(player_reward_exp=mpf("1e6")),
                                                               Reward(player_reward_exp=mpf("5e6")),
                                                               Reward(player_reward_gold=mpf("1e5")),
                                                               Reward(player_reward_gold=mpf("5e5")),
                                                               Reward(player_reward_gems=mpf("10")),
                                                               Reward(player_reward_gems=mpf("50")),
                                                               Reward(legendary_creature_reward_exp=mpf("1e6")),
                                                               Reward(legendary_creature_reward_exp=mpf("5e6"))
                                                               ] + [item for item in items])
                                           ] + [habitat for habitat in habitats])

# 3. Initialising potential CPU players the player can face
potential_cpu_players: list = [
    CPU("CPU #1"),
    CPU("CPU #2"),
    CPU("CPU #3"),
    CPU("CPU #4"),
    CPU("CPU #5"),
    CPU("CPU #6"),
    CPU("CPU #7"),
    CPU("CPU #8"),
    CPU("CPU #9"),
    CPU("CPU #10")
]

index: int = 1  # initial value
for cpu_player in potential_cpu_players:
    assert isinstance(cpu_player, CPU), "Invalid argument in list 'potential_cpu_players'!"
    cpu_player.battle_team = Team([generate_random_legendary_creature(
        Egg.POTENTIAL_ELEMENTS[random.randint(0, len(Egg.POTENTIAL_ELEMENTS) - 1)]
    ),
        generate_random_legendary_creature(
            Egg.POTENTIAL_ELEMENTS[random.randint(0, len(Egg.POTENTIAL_ELEMENTS) - 1)]
        ),
        generate_random_legendary_creature(
            Egg.POTENTIAL_ELEMENTS[random.randint(0, len(Egg.POTENTIAL_ELEMENTS) - 1)]
        ),
        generate_random_legendary_creature(
            Egg.POTENTIAL_ELEMENTS[random.randint(0, len(Egg.POTENTIAL_ELEMENTS) - 1)]
        ),
        generate_random_legendary_creature(
            Egg.POTENTIAL_ELEMENTS[random.randint(0, len(Egg.POTENTIAL_ELEMENTS) - 1)]
        )])
    level_ups: int = 5 * index
    for legendary_creature in cpu_player.battle_team.get_legendary_creatures():
        for k in range(level_ups):
            legendary_creature.exp = legendary_creature.required_exp
            legendary_creature.level_up()
            if legendary_creature.level == legendary_creature.max_level:
                legendary_creature.evolve()

    index += 1

# 4. The battle arena
battle_arena: Arena = Arena(potential_cpu_players)

# 5. Minigames the player can play in
minigames: list = [
    Minigame("BOX EATS PLANTS"), Minigame("MATCH WORD PUZZLE"), Minigame("MATCH-3 GAME"), Minigame("DAILY BONUS")
]


# Creating the main function used to run the game.


def main() -> int:
    """
    This main method is used to run the game.
    :return: an integer
    """

    print("Welcome to 'Legendary Creature City Builder' by 'NativeApkDev'.")
    print("This game is an offline strategy RPG where the player raises legendary ")
    print("creatures and brings them for battles.")
    print("Below is the element chart in 'Legendary Creature City Builder'.\n")
    print(str(tabulate_element_chart()) + "\n")
    print("The following elements do not have any elemental strengths nor weaknesses.")
    print("This is because they are ancient world elements. In this case, these elements will always ")
    print("be dealt with normal damage.\n")
    ancient_world_elements: list = ["BEAUTY", "MAGIC", "CHAOS", "HAPPY", "DREAM", "SOUL"]
    for i in range(0, len(ancient_world_elements)):
        print(str(i + 1) + ". " + str(ancient_world_elements[i]))

    # Initialising variable for the saved game data
    # Asking the user to enter his/her name to check whether saved game data exists or not
    player_name: str = input("Please enter your name: ")
    file_name: str = "SAVED LEGENDARY CREATURE CITY BUILDER GAME DATA - " + str(player_name).upper()

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
        new_game = Game(player_data, item_shop, building_shop, battle_arena, minigames)

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

        # Resetting all temple of wishes and minigames if possible
        if new_now.day != old_now.day:
            for section in new_game.player_data.player_city.get_sections():
                for x in range(section.SECTION_WIDTH):
                    for y in range(section.SECTION_HEIGHT):
                        curr_tile: CityTile = section.get_tile_at(x, y)
                        if isinstance(curr_tile.building, TempleOfWishes):
                            temple_of_wishes: TempleOfWishes = curr_tile.building
                            temple_of_wishes.restore()
                            temple_of_wishes.reset_wishes_left()

            for minigame in minigames:
                minigame.reset()

        # Increase player's EXP, gold, and gems
        new_game.player_data.exp += new_game.player_data.exp_per_second * seconds
        new_game.player_data.level_up()
        new_game.player_data.gold += new_game.player_data.gold_per_second * seconds
        new_game.player_data.gems += new_game.player_data.gems_per_second * seconds

        # Increase the exp of all legendary creatures owned by the player
        for legendary_creature in new_game.player_data.legendary_creature_inventory.get_legendary_creatures():
            legendary_creature.exp += legendary_creature.exp_per_second * seconds
            legendary_creature.level_up()

        # Hatching all eggs in hatcheries
        new_game.player_data.hatch_eggs_in_hatcheries()

        # Asking the player what he/she wants to do in the game.
        allowed: list = ["PLAY ADVENTURE MODE", "MANAGE PLAYER CITY", "MANAGE BATTLE TEAM",
                         "MANAGE LEGENDARY CREATURE INVENTORY", "MANAGE ITEM INVENTORY", "MAKE A WISH",
                         "FUSE LEGENDARY CREATURES", "PLACE EGG", "FEED LEGENDARY CREATURE",
                         "GIVE ITEM", "POWER UP LEGENDARY CREATURE", "EVOLVE LEGENDARY CREATURE",
                         "MANAGE HABITAT", "MANAGE TRAINING AREA", "PLACE RUNE", "REMOVE RUNE",
                         "PLAY MINIGAME", "BATTLE ARENA", "BUY ITEM", "VIEW STATS"]
        print("Enter 'PLAY ADVENTURE MODE' to play in adventure mode.")
        print("Enter 'MANAGE PLAYER CITY' to manage your city.")
        print("Enter 'MANAGE BATTLE TEAM' to manage your battle team.")
        print("Enter 'MANAGE LEGENDARY CREATURE INVENTORY' to manage your legendary creature inventory.")
        print("Enter 'MANAGE ITEM INVENTORY' to manage your item inventory.")
        print("Enter 'MAKE A WISH' to make a wish in a temple of wishes.")
        print("Enter 'FUSE LEGENDARY CREATURES' to fuse legendary creatures using a fusion center.")
        print("Enter 'PLACE EGG' to place an egg in the hatchery to get it hatched.")
        print("Enter 'FEED LEGENDARY CREATURE' to feed a legendary creature and increase its EXP.")
        print("Enter 'GIVE ITEM' to give an item to a legendary creature.")
        print("Enter 'POWER UP LEGENDARY CREATURE' to power up legendary creatures.")
        print("Enter 'EVOLVE LEGENDARY CREATURE' to evolve legendary creatures.")
        print("Enter 'MANAGE HABITAT' to manage your habitat.")
        print("Enter 'MANAGE TRAINING AREA' to manage your training area.")
        print("Enter 'PLACE RUNE' to place a rune on a legendary creature.")
        print("Enter 'REMOVE RUNE' to remove a rune from a legendary creature.")
        print("Enter 'PLAY MINIGAME' to play a minigame.")
        print("Enter 'BATTLE ARENA' to battle against a CPU controlled player.")
        print("Enter 'BUY ITEM' to purchase an item from the item shop.")
        print("Enter 'VIEW STATS' to view your stats.")
        action: str = input("What do you want to do? ")
        if action not in allowed:
            # Saving game data and quitting the game
            save_game_data(new_game, file_name)
            sys.exit()
        else:
            if action == "VIEW STATS":
                # Clearing the command line window
                clear()

                # Display player's stats
                print(new_game.player_data)
            elif action == "BUY ITEM":
                # Clearing the command line window
                clear()

                # Show a list of items which the player can buy
                item_list: list = new_game.item_shop.get_items_sold()
                print("Below is a list of items you can buy.\n")
                curr_item_index: int = 1  # initial value
                for item in item_list:
                    print("ITEM #" + str(curr_item_index))
                    print(str(item) + "\n")
                    curr_item_index += 1

                item_index: int = int(input("Please enter the index of the item you want to buy (1 - " +
                                            str(len(item_list)) + "): "))
                while item_index < 1 or item_index > len(item_list):
                    item_index: int = int(input("Sorry, invalid input! Please enter the index of the item you want "
                                                "to buy (1 - " + str(len(item_list)) + "): "))

                item_to_buy: Item = item_list[item_index - 1]
                if new_game.player_data.purchase_item(item_to_buy):
                    print("You have successfully bought " + str(item_to_buy.name))
                else:
                    print("Sorry, you have insufficient gold and/or gems!")
            elif action == "BATTLE ARENA":
                # Clearing the command line window
                clear()

                # Showing a list of CPU players the player can battle against in the arena.
                cpu_index: int = 1
                for opponent in new_game.battle_arena.get_potential_opponents():
                    print("OPPONENT NUMBER #" + str(cpu_index))
                    print(str(opponent) + "\n")
                    cpu_index += 1

                chosen_cpu_index: int = int(input("Please enter the index of the CPU player you "
                                                  "want to attack (1 - " + str(len(new_game.battle_arena.
                                                                                   get_potential_opponents())) +
                                                  "): "))
                while chosen_cpu_index < 1 or chosen_cpu_index > len(new_game.battle_arena.
                                                                             get_potential_opponents()):
                    chosen_cpu_index = int(input("Sorry, invalid input! Please enter the index of "
                                                 "the CPU player you "
                                                 "want to attack (1 - " + str(len(new_game.battle_arena.
                                                                                  get_potential_opponents())) +
                                                 "): "))

                chosen_cpu: CPU = new_game.battle_arena.get_potential_opponents()[chosen_cpu_index - 1]

                # Start the battle and battle until there is a winner
                # Clearing up the command line window
                clear()

                print("--------------------" + str(new_game.player_data.name) + " VS. " + str(chosen_cpu.name) +
                      "--------------------")
                curr_battle: Battle = Battle(new_game.player_data.battle_team, chosen_cpu.battle_team)
                while curr_battle.winner is None:
                    # Printing out the stats of legendary creatures in both teams
                    print("Below are the stats of all legendary creatures in player's team.\n")
                    for legendary_creature in curr_battle.team1.get_legendary_creatures():
                        print(str(legendary_creature) + "\n")

                    print("Below are the stats of all legendary creatures in enemy's team.\n")
                    for legendary_creature in curr_battle.team2.get_legendary_creatures():
                        print(str(legendary_creature) + "\n")

                    # Make a legendary creature move
                    curr_battle.get_someone_to_move()
                    assert isinstance(curr_battle.whose_turn, LegendaryCreature), "Cannot proceed with battle!"

                    if not curr_battle.whose_turn.can_move:
                        # Skip turn
                        curr_battle.whose_turn.have_turn(curr_battle.whose_turn, None, "NORMAL HEAL")

                        # Make another legendary creature move
                        curr_battle.get_someone_to_move()
                        assert isinstance(curr_battle.whose_turn, LegendaryCreature), \
                            "Cannot proceed with battle!"

                    # Checking which legendary creature moves
                    if curr_battle.whose_turn in curr_battle.team1.get_legendary_creatures():
                        moving_legendary_creature: LegendaryCreature = curr_battle.whose_turn
                        # Asking the player what he/she wants to do
                        print("Enter 'NORMAL ATTACK' for normal attack.")
                        print("Enter 'NORMAL HEAL' for normal heal.")
                        print("Enter anything else to use a skill (only applicable if you have usable skills).")
                        usable_skills: list = [skill for skill in curr_battle.whose_turn.get_skills()
                                               if curr_battle.whose_turn.curr_magic_points >=
                                               skill.magic_points_cost and isinstance(skill, ActiveSkill)]
                        possible_actions: list = ["NORMAL ATTACK", "NORMAL HEAL"]
                        trainer_battle_action: str = input("What do you want to do? ")
                        while len(usable_skills) == 0 and trainer_battle_action not in possible_actions:
                            print("Enter 'NORMAL ATTACK' for normal attack.")
                            print("Enter 'NORMAL HEAL' for normal heal.")
                            trainer_battle_action = input("Sorry, invalid input! What do you want to do? ")

                        if trainer_battle_action not in possible_actions:
                            # Use skill
                            trainer_battle_action = "USE SKILL"

                            # Show a list of skills the player can use
                            print("Below is a list of skills you can use.\n")
                            curr_skill_index: int = 1  # initial value
                            for skill in usable_skills:
                                print("SKILL #" + str(curr_skill_index))
                                print(str(skill) + "\n")
                                curr_skill_index += 1

                            skill_index: int = int(input("Please enter the index of the skill "
                                                         "you want to use (1 - " +
                                                         str(len(usable_skills)) + "): "))
                            while skill_index < 1 or skill_index > len(usable_skills):
                                skill_index = int(input("Sorry, invalid input! Please enter the "
                                                        "index of the skill "
                                                        "you want to use (1 - " +
                                                        str(len(usable_skills)) + "): "))

                            skill_to_use: ActiveSkill = usable_skills[skill_index - 1]
                            if skill_to_use.active_skill_type == "ATTACK":
                                # Asking the user to select a target
                                print("Below is a list of enemies you can attack.")
                                enemy_index: int = 1  # initial value
                                for enemy in curr_battle.team2.get_legendary_creatures():
                                    print("ENEMY #" + str(enemy_index))
                                    print(str(enemy) + "\n")
                                    enemy_index += 1

                                chosen_enemy_index: int = int(input("Please enter the index of the "
                                                                    "enemy you want to attack (1 - " +
                                                                    str(len(curr_battle.
                                                                            team2.get_legendary_creatures())) +
                                                                    "): "))
                                while chosen_enemy_index < 1 or chosen_enemy_index > len(curr_battle.
                                                                                                 team2.get_legendary_creatures()):
                                    chosen_enemy_index = int(input("Sorry, invalid input! "
                                                                   "Please enter the index of the "
                                                                   "enemy you want to attack (1 - " +
                                                                   str(len(curr_battle.
                                                                           team2.get_legendary_creatures())) +
                                                                   "): "))

                                chosen_enemy_target: LegendaryCreature = curr_battle.team2. \
                                    get_legendary_creatures()[chosen_enemy_index - 1]
                                curr_battle.whose_turn.have_turn(chosen_enemy_target, skill_to_use,
                                                                 trainer_battle_action)
                                if random.random() < chosen_enemy_target.counterattack_chance + \
                                        chosen_enemy_target.counterattack_chance_up:
                                    chosen_enemy_target.counterattack(curr_battle.whose_turn)

                            elif skill_to_use.active_skill_type == "HEAL":
                                # Asking the user to select who to heal
                                print("Below is a list of allies you can heal.")
                                ally_index: int = 1  # initial value
                                for ally in curr_battle.team1.get_legendary_creatures():
                                    print("ALLY #" + str(ally_index))
                                    print(str(ally) + "\n")
                                    ally_index += 1

                                chosen_ally_index: int = int(input("Please enter the index of the "
                                                                   "ally you want to heal (1 - " +
                                                                   str(len(curr_battle.
                                                                           team1.get_legendary_creatures())) +
                                                                   "): "))
                                while chosen_ally_index < 1 or chosen_ally_index > len(curr_battle.
                                                                                               team1.get_legendary_creatures()):
                                    chosen_ally_index = int(input("Sorry, invalid input! "
                                                                  "Please enter the index of the "
                                                                  "ally you want to heal (1 - " +
                                                                  str(len(curr_battle.
                                                                          team1.get_legendary_creatures())) +
                                                                  "): "))

                                chosen_ally_target: LegendaryCreature = curr_battle.team1. \
                                    get_legendary_creatures()[chosen_ally_index - 1]
                                curr_battle.whose_turn.have_turn(chosen_ally_target, skill_to_use,
                                                                 trainer_battle_action)
                            elif skill_to_use.active_skill_type == "ALLIES EFFECT":
                                # Asking the user to select who to apply ally effect on
                                print("Below is a list of allies you can apply ally effect on.")
                                ally_index: int = 1  # initial value
                                for ally in curr_battle.team1.get_legendary_creatures():
                                    print("ALLY #" + str(ally_index))
                                    print(str(ally) + "\n")
                                    ally_index += 1

                                chosen_ally_index: int = int(input("Please enter the index of the "
                                                                   "ally you want to apply ally effect on (1 - " +
                                                                   str(len(curr_battle.
                                                                           team1.get_legendary_creatures())) +
                                                                   "): "))
                                while chosen_ally_index < 1 or chosen_ally_index > len(curr_battle.
                                                                                               team1.get_legendary_creatures()):
                                    chosen_ally_index = int(input("Sorry, invalid input! "
                                                                  "Please enter the index of the "
                                                                  "ally you want to apply ally effect on (1 - " +
                                                                  str(len(curr_battle.
                                                                          team1.get_legendary_creatures())) +
                                                                  "): "))

                                chosen_ally_target: LegendaryCreature = curr_battle.team1. \
                                    get_legendary_creatures()[chosen_ally_index - 1]
                                curr_battle.whose_turn.have_turn(chosen_ally_target, skill_to_use,
                                                                 trainer_battle_action)
                            elif skill_to_use.active_skill_type == "ENEMIES EFFECT":
                                # Asking the user to select who to apply enemy effect on
                                print("Below is a list of enemies you can apply enemy effect on.")
                                enemy_index: int = 1  # initial value
                                for enemy in curr_battle.team2.get_legendary_creatures():
                                    print("ENEMY #" + str(enemy_index))
                                    print(str(enemy) + "\n")
                                    enemy_index += 1

                                chosen_enemy_index: int = int(input("Please enter the index of the "
                                                                    "enemy you want to apply enemy effect on"
                                                                    " (1 - " +
                                                                    str(len(curr_battle.
                                                                            team2.get_legendary_creatures())) +
                                                                    "): "))
                                while chosen_enemy_index < 1 or chosen_enemy_index > len(curr_battle.
                                                                                                 team2.get_legendary_creatures()):
                                    chosen_enemy_index = int(input("Sorry, invalid input! "
                                                                   "Please enter the index of the "
                                                                   "enemy you want to apply enemy effect on"
                                                                   " (1 - " +
                                                                   str(len(curr_battle.
                                                                           team2.get_legendary_creatures())) +
                                                                   "): "))

                                chosen_enemy_target: LegendaryCreature = curr_battle.team2. \
                                    get_legendary_creatures()[chosen_enemy_index - 1]
                                curr_battle.whose_turn.have_turn(chosen_enemy_target, skill_to_use,
                                                                 trainer_battle_action)

                        elif trainer_battle_action == "NORMAL ATTACK":
                            # Asking the user to select a target
                            print("Below is a list of enemies you can attack.")
                            enemy_index: int = 1  # initial value
                            for enemy in curr_battle.team2.get_legendary_creatures():
                                print("ENEMY #" + str(enemy_index))
                                print(str(enemy) + "\n")
                                enemy_index += 1

                            chosen_enemy_index: int = int(input("Please enter the index of the "
                                                                "enemy you want to attack (1 - " +
                                                                str(len(curr_battle.
                                                                        team2.get_legendary_creatures())) +
                                                                "): "))
                            while chosen_enemy_index < 1 or chosen_enemy_index > len(curr_battle.
                                                                                             team2.get_legendary_creatures()):
                                chosen_enemy_index = int(input("Sorry, invalid input! "
                                                               "Please enter the index of the "
                                                               "enemy you want to attack (1 - " +
                                                               str(len(curr_battle.
                                                                       team2.get_legendary_creatures())) +
                                                               "): "))

                            chosen_enemy_target: LegendaryCreature = curr_battle.team2. \
                                get_legendary_creatures()[chosen_enemy_index - 1]
                            curr_battle.whose_turn.have_turn(chosen_enemy_target, None, trainer_battle_action)
                            if random.random() < chosen_enemy_target.counterattack_chance + \
                                    chosen_enemy_target.counterattack_chance_up:
                                chosen_enemy_target.counterattack(curr_battle.whose_turn)

                        elif trainer_battle_action == "NORMAL HEAL":
                            # Asking the user to select who to heal
                            print("Below is a list of allies you can heal.")
                            ally_index: int = 1  # initial value
                            for ally in curr_battle.team1.get_legendary_creatures():
                                print("ALLY #" + str(ally_index))
                                print(str(ally) + "\n")
                                ally_index += 1

                            chosen_ally_index: int = int(input("Please enter the index of the "
                                                               "ally you want to heal (1 - " +
                                                               str(len(curr_battle.
                                                                       team1.get_legendary_creatures())) +
                                                               "): "))
                            while chosen_ally_index < 1 or chosen_ally_index > len(curr_battle.
                                                                                           team1.get_legendary_creatures()):
                                chosen_ally_index = int(input("Sorry, invalid input! "
                                                              "Please enter the index of the "
                                                              "ally you want to heal (1 - " +
                                                              str(len(curr_battle.
                                                                      team1.get_legendary_creatures())) +
                                                              "): "))

                            chosen_ally_target: LegendaryCreature = curr_battle.team1. \
                                get_legendary_creatures()[chosen_ally_index - 1]
                            curr_battle.whose_turn.have_turn(chosen_ally_target, None,
                                                             trainer_battle_action)
                        else:
                            pass

                        # Checking the case where the moving legendary creature gets an extra turn
                        if random.random() < moving_legendary_creature.extra_turn_chance + \
                                moving_legendary_creature.extra_turn_chance_up and \
                                moving_legendary_creature.can_move:
                            curr_battle.whose_turn = moving_legendary_creature

                            # Recovering magic points
                            curr_battle.whose_turn.recover_magic_points()
                        else:
                            curr_battle.get_someone_to_move()

                    elif curr_battle.whose_turn in curr_battle.team2.get_legendary_creatures():
                        curr_moving_legendary_creature: LegendaryCreature = curr_battle.whose_turn
                        chance: float = random.random()
                        trainer_battle_action: str = "NORMAL ATTACK" if chance <= 1 / 3 else \
                            "NORMAL HEAL" if 1 / 3 < chance <= 2 / 3 else "USE SKILL"
                        usable_skills: list = [skill for skill in curr_battle.whose_turn.get_skills()
                                               if curr_battle.whose_turn.curr_magic_points >=
                                               skill.magic_points_cost and isinstance(skill, ActiveSkill)]

                        # If there are no usable skills and 'trainer_battle_action' is set to "USE SKILL",
                        # change the value of 'trainer_battle_action'
                        if len(usable_skills) == 0:
                            trainer_battle_action = "NORMAL ATTACK" if random.random() < 0.5 else "NORMAL HEAL"

                        if trainer_battle_action == "NORMAL ATTACK":
                            # A normal attack occurs
                            moving_legendary_creature: LegendaryCreature = curr_battle.whose_turn
                            target: LegendaryCreature = curr_battle.team1.get_legendary_creatures() \
                                [random.randint(0, len(curr_battle.team1.get_legendary_creatures()) - 1)]
                            moving_legendary_creature.have_turn(target, None, trainer_battle_action)
                            if random.random() < target.counterattack_chance + \
                                    target.counterattack_chance_up:
                                target.counterattack(moving_legendary_creature)
                        elif trainer_battle_action == "NORMAL HEAL":
                            # A normal heal occurs
                            moving_legendary_creature: LegendaryCreature = curr_battle.whose_turn
                            target: LegendaryCreature = curr_battle.team2.get_legendary_creatures() \
                                [random.randint(0, len(curr_battle.team2.get_legendary_creatures()) - 1)]
                            moving_legendary_creature.have_turn(target, None, trainer_battle_action)
                        elif trainer_battle_action == "USE SKILL":
                            # A skill is used
                            moving_legendary_creature: LegendaryCreature = curr_battle.whose_turn
                            skill_to_use: ActiveSkill = usable_skills[random.randint(0, len(usable_skills) - 1)]
                            if skill_to_use.active_skill_type == "ATTACK" or \
                                    skill_to_use.active_skill_type == "ENEMIES EFFECT":
                                target: LegendaryCreature = curr_battle.team1.get_legendary_creatures() \
                                    [random.randint(0, len(curr_battle.team1.get_legendary_creatures()) - 1)]
                                moving_legendary_creature.have_turn(target, skill_to_use, trainer_battle_action)
                                if skill_to_use.active_skill_type == "ATTACK":
                                    if random.random() < target.counterattack_chance + \
                                            target.counterattack_chance_up:
                                        target.counterattack(moving_legendary_creature)
                            else:
                                target: LegendaryCreature = curr_battle.team2.get_legendary_creatures() \
                                    [random.randint(0, len(curr_battle.team2.get_legendary_creatures()) - 1)]
                                moving_legendary_creature.have_turn(target, skill_to_use, trainer_battle_action)
                        else:
                            pass

                        # Checking the case where the moving legendary creature gets an extra turn
                        if random.random() < curr_moving_legendary_creature.extra_turn_chance + \
                                curr_moving_legendary_creature.extra_turn_chance_up and \
                                curr_moving_legendary_creature.can_move:
                            curr_battle.whose_turn = curr_moving_legendary_creature

                            # Recovering magic points
                            curr_battle.whose_turn.recover_magic_points()
                        else:
                            curr_battle.get_someone_to_move()

                    # Recovering magic points
                    curr_battle.whose_turn.recover_magic_points()

                if curr_battle.winner == curr_battle.team1:
                    print("Congratulations! You won the battle!")
                    new_game.player_data.claim_reward(curr_battle.reward)
                    new_game.player_data.arena_wins += 1
                    chosen_cpu.arena_losses += 1
                    chosen_cpu.times_beaten += 1
                    chosen_cpu.strengthen()
                    if new_game.player_data.arena_points > chosen_cpu.arena_points:
                        new_game.player_data.arena_points += 5
                        chosen_cpu.arena_points -= 2
                    else:
                        new_game.player_data.arena_points += 10
                        chosen_cpu.arena_points -= 5

                elif curr_battle.winner == curr_battle.team2:
                    print("You lost the battle! Please come back stronger!")
                    new_game.player_data.arena_losses += 1
                    chosen_cpu.arena_wins += 1
                    if new_game.player_data.arena_points > chosen_cpu.arena_points:
                        new_game.player_data.arena_points -= 5
                        chosen_cpu.arena_points += 10
                    else:
                        new_game.player_data.arena_points -= 2
                        chosen_cpu.arena_points += 5

                # Restore all legendary creatures
                curr_battle.team1.recover_all()
                curr_battle.team2.recover_all()

            elif action == "PLAY MINIGAME":
                # Clearing the command line window
                clear()

                print("Below is a list of minigames you can play.\n")
                curr_minigame_index: int = 1  # initial value
                for minigame in new_game.get_minigames():
                    print("MINIGAME #" + str(curr_minigame_index))
                    print(str(minigame) + "\n")
                    curr_minigame_index += 1

                minigame_index: int = int(input("Please enter the index of the minigame you want to play (1 - " +
                                                str(len(new_game.get_minigames())) + "): "))
                while minigame_index < 1 or minigame_index > len(new_game.get_minigames()):
                    minigame_index = int(input("Sorry, invalid input! Please enter the index of the minigame "
                                               "you want to play (1 - " +
                                               str(len(new_game.get_minigames())) + "): "))

                chosen_minigame: Minigame = new_game.get_minigames()[minigame_index - 1]

                # Getting the player to play the chosen minigame
                if chosen_minigame.name == "BOX EATS PLANTS":
                    print("Welcome to 'Box Eats Plants'.")
                    print("Your goal in this game is to get the box to eat as many plants as possible ")
                    print("while avoiding rocks.")
                    # Set up the minigame "Box Eats Plants"
                    score: int = 0  # initial value
                    game_over: bool = False  # initial value
                    board: BoxEatsPlantsBoard = BoxEatsPlantsBoard()
                    box: Box = Box(0, 0)  # initial value
                    rocks: list = []
                    plants: list = []
                    while board.num_rocks() < 5:
                        rocks.append(board.spawn_rock())

                    while board.num_plants() < 5:
                        plants.append(board.spawn_plant())

                    while board.num_boxes() < 1:
                        box = board.spawn_box()

                    while not game_over:
                        # Clearing the command line window
                        clear()

                        # Show the current progress of the game
                        print("Below is the current representation of the board.\n" + str(board))
                        print("Current coordinates of box: (" + str(box.x) + ", " + str(box.y) + ").")
                        print("Your score: " + str(score))
                        allowed: list = ["UP", "DOWN", "LEFT", "RIGHT"]
                        print("Enter 'UP' to move box up.")
                        print("Enter 'DOWN' to move box down.")
                        print("Enter 'LEFT' to move box left.")
                        print("Enter 'RIGHT' to move box right.")
                        direction: str = input("Where do you want to move the box to? ")
                        while direction not in allowed:
                            print("Enter 'UP' to move box up.")
                            print("Enter 'DOWN' to move box down.")
                            print("Enter 'LEFT' to move box left.")
                            print("Enter 'RIGHT' to move box right.")
                            direction = input("Sorry, invalid input! Where do you want to move the box to? ")

                        if direction == "UP":
                            box.move_up(board)
                        elif direction == "DOWN":
                            box.move_down(board)
                        elif direction == "LEFT":
                            box.move_left(board)
                        else:
                            box.move_right(board)

                        box_tile: BoxEatsPlantsTile = board.get_tile_at(box.x, box.y)
                        if box_tile.rock is not None:
                            game_over = True

                        if isinstance(box_tile.plant, Plant):
                            score += 1
                            plants.remove(box_tile.plant)
                            box_tile.remove_plant()
                            plants.append(board.spawn_plant())

                        rock_direction: str = allowed[random.randint(0, 3)]
                        if rock_direction == "UP":
                            for rock in rocks:
                                rock.move_up(board)
                                rock_tile: BoxEatsPlantsTile = board.get_tile_at(rock.x, rock.y)
                                if isinstance(rock_tile.box, Box):
                                    game_over = True

                        elif rock_direction == "DOWN":
                            for rock in rocks:
                                rock.move_down(board)
                                rock_tile: BoxEatsPlantsTile = board.get_tile_at(rock.x, rock.y)
                                if isinstance(rock_tile.box, Box):
                                    game_over = True

                        elif rock_direction == "LEFT":
                            for rock in rocks:
                                rock.move_left(board)
                                rock_tile: BoxEatsPlantsTile = board.get_tile_at(rock.x, rock.y)
                                if isinstance(rock_tile.box, Box):
                                    game_over = True

                        else:
                            for rock in rocks:
                                rock.move_right(board)
                                rock_tile: BoxEatsPlantsTile = board.get_tile_at(rock.x, rock.y)
                                if isinstance(rock_tile.box, Box):
                                    game_over = True

                        plant_direction: str = allowed[random.randint(0, 3)]
                        if plant_direction == "UP":
                            for plant in plants:
                                plant.move_up(board)
                                plant_tile: BoxEatsPlantsTile = board.get_tile_at(plant.x, plant.y)
                                if isinstance(plant_tile.box, Box):
                                    score += 1
                                    plants.remove(plant)
                                    plant_tile.remove_plant()
                                    plants.append(board.spawn_plant())

                        elif plant_direction == "DOWN":
                            for plant in plants:
                                plant.move_down(board)
                                plant_tile: BoxEatsPlantsTile = board.get_tile_at(plant.x, plant.y)
                                if isinstance(plant_tile.box, Box):
                                    score += 1
                                    plants.remove(plant)
                                    plant_tile.remove_plant()
                                    plants.append(board.spawn_plant())

                        elif plant_direction == "LEFT":
                            for plant in plants:
                                plant.move_left(board)
                                plant_tile: BoxEatsPlantsTile = board.get_tile_at(plant.x, plant.y)
                                if isinstance(plant_tile.box, Box):
                                    score += 1
                                    plants.remove(plant)
                                    plant_tile.remove_plant()
                                    plants.append(board.spawn_plant())

                        else:
                            for plant in plants:
                                plant.move_right(board)
                                plant_tile: BoxEatsPlantsTile = board.get_tile_at(plant.x, plant.y)
                                if isinstance(plant_tile.box, Box):
                                    score += 1
                                    plants.remove(plant)
                                    plant_tile.remove_plant()
                                    plants.append(board.spawn_plant())

                    # Clearing the command line window
                    clear()

                    # Generate reward for the player
                    print("'BOX EATS PLANTS' GAME OVER! Your score is " + str(score))
                    reward: Reward = Reward(player_reward_exp=mpf("10") ** score,
                                            player_reward_gold=mpf("10") ** (score - 2),
                                            legendary_creature_reward_exp=mpf("10") ** score)
                    new_game.player_data.claim_reward(reward)

                elif chosen_minigame.name == "MATCH WORD PUZZLE":
                    print("Welcome to 'Match Word Puzzle'.")
                    print("Your goal in this game is to match tiles on the board with the same word ")
                    print("as fast as possible.")
                    # Set up the minigame "Match Word Puzzle"
                    start_time: datetime = datetime.now()
                    board: MatchWordPuzzleBoard = MatchWordPuzzleBoard()
                    while not board.all_opened():
                        # Clearing the command line window
                        clear()

                        print("Below is the current representation of the board.\n" + str(board))
                        print("You are required to enter the coordinates of the two tiles you want to "
                              "open (the tiles must be different).")
                        first_x: int = int(input("Please enter the x-coordinates of the first "
                                                 "tile you want to open (1 - " + str(board.BOARD_WIDTH) + "): "))
                        first_y: int = int(input("Please enter the y-coordinates of the first "
                                                 "tile you want to open (1 - " + str(board.BOARD_HEIGHT) + "): "))
                        while board.get_tile_at(first_x, first_y) is None:
                            first_x = int(input("Sorry, invalid input! Please enter the x-coordinates of the first "
                                                "tile you want to open (1 - " + str(board.BOARD_WIDTH) + "): "))
                            first_y = int(input("Sorry, invalid input! Please enter the y-coordinates of the first "
                                                "tile you want to open (1 - " + str(board.BOARD_HEIGHT) + "): "))

                        first_tile: MatchWordPuzzleTile = board.get_tile_at(first_x, first_y)
                        second_x: int = int(input("Please enter the x-coordinates of the second "
                                                  "tile you want to open (1 - " + str(board.BOARD_WIDTH) + "): "))
                        second_y: int = int(input("Please enter the y-coordinates of the second "
                                                  "tile you want to open (1 - " + str(board.BOARD_HEIGHT) + "): "))
                        while board.get_tile_at(second_x, second_y) is None or \
                                (first_x == second_x and first_y == second_y):
                            second_x: int = int(input("Sorry, invalid input! Please enter the x-coordinates "
                                                      "of the second "
                                                      "tile you want to open (1 - " + str(board.BOARD_WIDTH) + "): "))
                            second_y: int = int(input("Sorry, invalid input! Please enter the y-coordinates "
                                                      "of the second "
                                                      "tile you want to open (1 - " + str(board.BOARD_HEIGHT) + "): "))

                        second_tile: MatchWordPuzzleTile = board.get_tile_at(second_x, second_y)

                        # If the contents of both of the tiles selected are equal, open both tiles.
                        if first_tile.contents == second_tile.contents:
                            first_tile.open()
                            second_tile.open()

                    finish_time: datetime = datetime.now()
                    seconds_elapsed: int = (finish_time - start_time).seconds
                    reward: Reward = Reward(player_reward_exp=mpf("1e24") / seconds_elapsed,
                                            player_reward_gold=mpf("1e22") / seconds_elapsed,
                                            legendary_creature_reward_exp=mpf("1e24") / seconds_elapsed)
                    new_game.player_data.claim_reward(reward)

                elif chosen_minigame.name == "MATCH-3 GAME":
                    print("Welcome to 'Match-3 Game'.")
                    print("Your goal in this game is to break at least 60 tiles from 15 moves.")
                    # Set up the minigame "Match-3 Game"
                    max_moves: int = 15
                    min_broken_tiles: int = 60
                    curr_broken_tiles: int = 0  # initial value
                    curr_moves: int = 0  # initial value
                    curr_board: MatchThreeBoard = MatchThreeBoard()

                    # Re-initialise the board if there are no possible moves.
                    while curr_board.no_possible_moves():
                        curr_board = MatchThreeBoard()

                    while curr_moves < max_moves:
                        # Clearing the command line window
                        clear()

                        print("Below is the current representation of the board.\n" + str(curr_board))
                        print("You are required to enter the coordinates of the two tiles you want to "
                              "swap (the tiles must be next to each other).")
                        first_x: int = int(input("Please enter the x-coordinates of the first "
                                                 "tile you want to swap (1 - " + str(curr_board.BOARD_WIDTH) + "): "))
                        first_y: int = int(input("Please enter the y-coordinates of the first "
                                                 "tile you want to swap (1 - " + str(curr_board.BOARD_HEIGHT) + "): "))
                        while curr_board.get_tile_at(first_x, first_y) is None:
                            first_x = int(input("Sorry, invalid input! Please enter the x-coordinates of the first "
                                                "tile you want to swap (1 - " + str(curr_board.BOARD_WIDTH) + "): "))
                            first_y = int(input("Sorry, invalid input! Please enter the y-coordinates of the first "
                                                "tile you want to swap (1 - " + str(curr_board.BOARD_HEIGHT) + "): "))

                        second_x: int = int(input("Please enter the x-coordinates of the second "
                                                  "tile you want to swap (1 - " + str(curr_board.BOARD_WIDTH) + "): "))
                        second_y: int = int(input("Please enter the y-coordinates of the second "
                                                  "tile you want to swap (1 - " + str(curr_board.BOARD_HEIGHT) + "): "))
                        while curr_board.get_tile_at(second_x, second_y) is None or \
                                abs(first_x - second_x) + abs(first_y - second_y) != 1:
                            second_x = int(input("Sorry, invalid input! Please enter the x-coordinates of the second "
                                                 "tile you want to swap (1 - " + str(curr_board.BOARD_WIDTH) + "): "))
                            second_y = int(input("Sorry, invalid input! Please enter the y-coordinates of the second "
                                                 "tile you want to swap (1 - " + str(curr_board.BOARD_HEIGHT) + "): "))

                        new_board: MatchThreeBoard = curr_board.clone()
                        new_board.swap_tiles(first_x, first_y, second_x, second_y)
                        matches: list = new_board.check_matches()
                        if len(matches) > 0:
                            # Update the current representation of the board and remove all matches
                            curr_board = new_board
                            for match in matches:
                                curr_broken_tiles += len(match)

                            curr_moves += 1
                            curr_board.clear_matches()
                            curr_board.fill_board()

                        while len(curr_board.check_matches()) > 0:
                            # Update the current representation of the board and remove all matches
                            matches = curr_board.check_matches()
                            for match in matches:
                                curr_broken_tiles += len(match)

                            curr_board.clear_matches()
                            curr_board.fill_board()

                        # Re-initialise the board if there are no possible moves.
                        while curr_board.no_possible_moves():
                            curr_board = MatchThreeBoard()

                    # Checking whether the number of broken tiles reach the minimum required or not.
                    # If yes, the player gains a reward.
                    if curr_broken_tiles >= min_broken_tiles:
                        print("Congratulations! You won the 'Match-3 Game'!")
                        reward: Reward = Reward(player_reward_exp=mpf("10") **
                                                                  (10 + curr_broken_tiles - min_broken_tiles),
                                                player_reward_gold=mpf("10") **
                                                                   (8 + curr_broken_tiles - min_broken_tiles),
                                                legendary_creature_reward_exp=mpf("10") **
                                                                              (
                                                                                      10 + curr_broken_tiles - min_broken_tiles))
                        new_game.player_data.claim_reward(reward)
                    else:
                        print("You lost! Better luck next time!")

            elif action == "REMOVE RUNE":
                # Clearing up the command line window
                clear()

                # Allow the player to remove a rune if there are legendary creatures in the legendary creature
                # inventory.
                if len(new_game.player_data.legendary_creature_inventory.get_legendary_creatures()) > 0:
                    print("Below is a list of legendary creatures you have.\n")
                    curr_legendary_creature_index: int = 1  # initial value
                    for legendary_creature in new_game.player_data.legendary_creature_inventory.get_legendary_creatures():
                        print("LEGENDARY CREATURE #" + str(curr_legendary_creature_index))
                        print(str(legendary_creature) + "\n")
                        curr_legendary_creature_index += 1

                    legendary_creature_index: int = int(input("Please enter the index of the legendary creature "
                                                              "you want to remove a rune from (1 - " +
                                                              str(len(new_game.player_data.legendary_creature_inventory.
                                                                      get_legendary_creatures())) + "): "))
                    while legendary_creature_index < 1 or legendary_creature_index > \
                            len(new_game.player_data.legendary_creature_inventory.get_legendary_creatures()):
                        legendary_creature_index = int(input("Sorry, invalid input! Please enter the index of the "
                                                             "legendary creature you want to remove a rune from "
                                                             "(1 - " +
                                                             str(len(new_game.player_data.legendary_creature_inventory.
                                                                     get_legendary_creatures())) + "): "))

                    chosen_legendary_creature: LegendaryCreature = \
                        new_game.player_data.legendary_creature_inventory.get_legendary_creatures() \
                            [legendary_creature_index - 1]
                    print(str(chosen_legendary_creature.name) + " has runes placed in slots as below.")
                    for i in chosen_legendary_creature.get_runes().keys():
                        print("SLOT NUMBER #" + str(i))

                    slot_number: int = int(input("Please enter the slot number of the rune you want to remove "
                                                 "(1 - 6): "))
                    while slot_number < 1 or slot_number > 6:
                        slot_number = int(
                            input("Sorry, invalid input! Please enter the slot number of the rune you want to "
                                  "remove (1 - 6): "))

                    chosen_legendary_creature.remove_rune(slot_number)

            elif action == "PLACE RUNE":
                # Clearing up the command line window
                clear()

                # Allow the player to place a rune if there are legendary creatures in the legendary creature
                # inventory.
                if len(new_game.player_data.legendary_creature_inventory.get_legendary_creatures()) > 0:
                    print("Below is a list of legendary creatures you have.\n")
                    curr_legendary_creature_index: int = 1  # initial value
                    for legendary_creature in new_game.player_data.legendary_creature_inventory.get_legendary_creatures():
                        print("LEGENDARY CREATURE #" + str(curr_legendary_creature_index))
                        print(str(legendary_creature) + "\n")
                        curr_legendary_creature_index += 1

                    legendary_creature_index: int = int(input("Please enter the index of the legendary creature "
                                                              "you want to place a rune on (1 - " +
                                                              str(len(new_game.player_data.legendary_creature_inventory.
                                                                      get_legendary_creatures())) + "): "))
                    while legendary_creature_index < 1 or legendary_creature_index > \
                            len(new_game.player_data.legendary_creature_inventory.get_legendary_creatures()):
                        legendary_creature_index = int(input("Sorry, invalid input! Please enter the index of the "
                                                             "legendary creature you want to place a rune on "
                                                             "(1 - " +
                                                             str(len(new_game.player_data.legendary_creature_inventory.
                                                                     get_legendary_creatures())) + "): "))

                    chosen_legendary_creature: LegendaryCreature = \
                        new_game.player_data.legendary_creature_inventory.get_legendary_creatures() \
                            [legendary_creature_index - 1]

                    # Getting a list of runes which can be placed to the legendary creature
                    runes: list = []  # initial value
                    for item in new_game.player_data.item_inventory.get_items():
                        if isinstance(item, Rune):
                            if not item.already_placed:
                                runes.append(item)

                    print("Enter 'Y' for yes.")
                    print("Enter anything else for no.")
                    place_rune: str = input(
                        "Do you want to place a rune to " + str(chosen_legendary_creature.name) + "? ")
                    if place_rune == "Y":
                        if len(runes) > 0:
                            print("Below is a list of runes you have.\n")
                            curr_rune_index: int = 1  # initial value
                            for rune in runes:
                                print("RUNE #" + str(curr_rune_index))
                                print(str(rune) + "\n")
                                curr_rune_index += 1

                            rune_index: int = int(input("Please enter the index of the rune you want to place to "
                                                        "this legendary creature (1 - " + str(len(runes)) + "): "))
                            while rune_index < 1 or rune_index > len(runes):
                                rune_index = int(input(
                                    "Sorry, invalid input! Please enter the index of the rune you want to place to "
                                    "this legendary creature (1 - " + str(len(runes)) + "): "))

                            chosen_rune: Rune = runes[rune_index - 1]
                            chosen_legendary_creature.place_rune(chosen_rune)

            elif action == "MANAGE TRAINING AREA":
                # Clearing up the command line window
                clear()

                # Getting a list of training areas in the player's city
                training_areas: list = []  # initial value
                for section in new_game.player_data.player_city.get_sections():
                    for x in range(section.SECTION_WIDTH):
                        for y in range(section.SECTION_HEIGHT):
                            curr_tile: CityTile = section.get_tile_at(x, y)
                            if isinstance(curr_tile.building, TrainingArea):
                                training_areas.append(curr_tile.building)

                # If there are training areas, ask the player which training area he/she wants to manage.
                if len(training_areas) > 0:
                    print("Below is a list of training areas that you have.\n")
                    curr_training_area_index: int = 1  # initial value
                    for training_area in training_areas:
                        print("TRAINING AREA #" + str(curr_training_area_index))
                        print(str(training_area) + "\n")
                        curr_training_area_index += 1

                    training_area_index: int = int(input("Please enter the index of the training area you want to "
                                                         "manage (1 - " + str(len(training_areas)) + "): "))
                    while training_area_index < 1 or training_area_index > len(training_areas):
                        training_area_index = int(input("Sorry, invalid input! Please enter the index of the training "
                                                        "area "
                                                        "you want to manage (1 - " + str(len(training_areas)) + "): "))

                    chosen_training_area: TrainingArea = training_areas[training_area_index - 1]

                    # Checking whether a legendary creature can be added to the chosen training area or not.
                    if len(chosen_training_area.get_legendary_creatures_placed()) < \
                            chosen_training_area.MAX_LEGENDARY_CREATURES:
                        # Printing a list of legendary creatures the player can add to the training area
                        available_legendary_creatures: list = []  # initial value
                        for legendary_creature in new_game.player_data.legendary_creature_inventory.get_legendary_creatures():
                            if legendary_creature not in new_game.player_data.battle_team.get_legendary_creatures() and \
                                    not legendary_creature.placed_in_training_area and not \
                                    legendary_creature.placed_in_habitat:
                                available_legendary_creatures.append(legendary_creature)

                        if len(available_legendary_creatures) > 0:
                            print("Enter 'Y' for yes.")
                            print("Enter anything else for no.")
                            add_legendary_creature: str = input("Do you want to add a legendary creature to the "
                                                                "training area? ")
                            if add_legendary_creature == "Y":
                                print(
                                    "Below is a list of legendary creatures which you can add to the training area.\n")
                                curr_legendary_creature_index: int = 1  # initial value
                                for legendary_creature in available_legendary_creatures:
                                    print("LEGENDARY CREATURE #" + str(curr_legendary_creature_index))
                                    print(str(legendary_creature) + "\n")
                                    curr_legendary_creature_index += 1

                                legendary_creature_index: int = int(
                                    input("Please enter the index of the legendary creature "
                                          "you want to add to the training area (1 - " +
                                          str(len(available_legendary_creatures)) + "): "))
                                while legendary_creature_index < 1 or legendary_creature_index > \
                                        len(available_legendary_creatures):
                                    legendary_creature_index = int(
                                        input("Sorry, invalid input! Please enter the index of the "
                                              "legendary creature you want to add to the training "
                                              "area (1 - " +
                                              str(len(available_legendary_creatures)) + "): "))

                                legendary_creature_to_add: LegendaryCreature = \
                                    available_legendary_creatures[legendary_creature_index - 1]
                                new_game.player_data.add_legendary_creature_to_training_area(legendary_creature_to_add,
                                                                                             chosen_training_area)

                    # Checking whether a legendary creature can be removed from the chosen training area or not.
                    if len(chosen_training_area.get_legendary_creatures_placed()) > 0:
                        print("Enter 'Y' for yes.")
                        print("Enter anything else for no.")
                        remove_legendary_creature: str = input("Do you want to remove a legendary creature from the "
                                                               "training area? ")
                        if remove_legendary_creature == "Y":
                            # Printing a list of legendary creatures in the chosen training area
                            curr_legendary_creature_index: int = 1
                            for legendary_creature in chosen_training_area.get_legendary_creatures_placed():
                                print("LEGENDARY CREATURE #" + str(curr_legendary_creature_index))
                                print(str(legendary_creature) + "\n")
                                curr_legendary_creature_index += 1

                            legendary_creature_index: int = int(input("Please enter the index of the legendary "
                                                                      "creature "
                                                                      "you want to remove from the training area (1 - " +
                                                                      str(len(chosen_training_area.
                                                                              get_legendary_creatures_placed())) + "): "))
                            while legendary_creature_index < 1 or legendary_creature_index > \
                                    len(chosen_training_area.get_legendary_creatures_placed()):
                                legendary_creature_index = int(input("Sorry, invalid input! Please enter the index of "
                                                                     "the "
                                                                     "legendary creature "
                                                                     "you want to remove from the training area (1 - " +
                                                                     str(len(chosen_training_area.
                                                                             get_legendary_creatures_placed())) + "): "))

                            legendary_creature_to_remove: LegendaryCreature = \
                                chosen_training_area.get_legendary_creatures_placed()[legendary_creature_index - 1]
                            new_game.player_data.remove_legendary_creature_from_training_area \
                                (legendary_creature_to_remove, chosen_training_area)

            elif action == "MANAGE HABITAT":
                # Clearing up the command line window
                clear()

                # Getting a list of habitats in the player's city
                habitats: list = []  # initial value
                for section in new_game.player_data.player_city.get_sections():
                    for x in range(section.SECTION_WIDTH):
                        for y in range(section.SECTION_HEIGHT):
                            curr_tile: CityTile = section.get_tile_at(x, y)
                            if isinstance(curr_tile.building, Habitat):
                                habitats.append(curr_tile.building)

                # If there are habitats, ask the player which training area he/she wants to manage.
                if len(habitats) > 0:
                    print("Below is a list of habitats that you have.\n")
                    curr_habitat_index: int = 1
                    for habitat in habitats:
                        print("HABITAT #" + str(curr_habitat_index))
                        print(str(habitat) + "\n")
                        curr_habitat_index += 1

                    chosen_habitat_index: int = int(input("Please enter the index of the habitat you want "
                                                          "to manage (1 - " + str(len(habitats)) + "): "))
                    while chosen_habitat_index < 1 or chosen_habitat_index > len(habitats):
                        chosen_habitat_index = int(input("Sorry, invalid input! Please enter the index of the "
                                                         "habitat you want "
                                                         "to manage (1 - " + str(len(habitats)) + "): "))

                    chosen_habitat: Habitat = habitats[chosen_habitat_index - 1]

                    # Checking whether legendary creatures can be added to the chosen habitat or not.
                    if len(chosen_habitat.get_legendary_creatures_placed()) < chosen_habitat.MAX_LEGENDARY_CREATURES:
                        # Printing a list of legendary creatures the player can add to the habitat
                        available_legendary_creatures: list = []  # initial value
                        for legendary_creature in new_game.player_data.legendary_creature_inventory.get_legendary_creatures():
                            if legendary_creature not in new_game.player_data.battle_team.get_legendary_creatures() and \
                                    not legendary_creature.placed_in_training_area and not \
                                    legendary_creature.placed_in_habitat and chosen_habitat.element in \
                                    legendary_creature.get_elements():
                                available_legendary_creatures.append(legendary_creature)

                        if len(available_legendary_creatures) > 0:
                            print("Enter 'Y' for yes.")
                            print("Enter anything else for no.")
                            add_legendary_creature: str = input("Do you want to add a legendary creature to the "
                                                                "habitat? ")
                            if add_legendary_creature == "Y":
                                print("Below is a list of legendary creatures which you can add to the habitat.\n")
                                curr_legendary_creature_index: int = 1  # initial value
                                for legendary_creature in available_legendary_creatures:
                                    print("LEGENDARY CREATURE #" + str(curr_legendary_creature_index))
                                    print(str(legendary_creature) + "\n")
                                    curr_legendary_creature_index += 1

                                legendary_creature_index: int = int(input("Please enter the index of the "
                                                                          "legendary creature you want to "
                                                                          "add to the habitat (1 - " +
                                                                          str(len(available_legendary_creatures)) +
                                                                          "): "))
                                while legendary_creature_index < 1 or legendary_creature_index > \
                                        len(available_legendary_creatures):
                                    legendary_creature_index = int(input("Sorry, invalid input! "
                                                                         "Please enter the index of the "
                                                                         "legendary creature you want to "
                                                                         "add to the habitat (1 - " +
                                                                         str(len(available_legendary_creatures)) +
                                                                         "): "))

                                legendary_creature_to_add: LegendaryCreature = \
                                    available_legendary_creatures[legendary_creature_index - 1]
                                new_game.player_data.add_legendary_creature_to_habitat(legendary_creature_to_add,
                                                                                       chosen_habitat)

                    # Checking whether a legendary creature can be removed from the chosen habitat or not.
                    if len(chosen_habitat.get_legendary_creatures_placed()) > 0:
                        print("Enter 'Y' for yes.")
                        print("Enter anything else for no.")
                        remove_legendary_creature: str = input("Do you want to remove a legendary creature from the "
                                                               "habitat? ")
                        if remove_legendary_creature == "Y":
                            # Printing a list of legendary creatures in the chosen habitat
                            curr_legendary_creature_index: int = 1
                            for legendary_creature in chosen_habitat.get_legendary_creatures_placed():
                                print("LEGENDARY CREATURE #" + str(curr_legendary_creature_index))
                                print(str(legendary_creature) + "\n")
                                curr_legendary_creature_index += 1

                            legendary_creature_index: int = int(input("Please enter the index of the legendary "
                                                                      "creature "
                                                                      "you want to remove from the habitat (1 - " +
                                                                      str(len(chosen_habitat.
                                                                              get_legendary_creatures_placed())) + "): "))
                            while legendary_creature_index < 1 or legendary_creature_index > \
                                    len(chosen_habitat.get_legendary_creatures_placed()):
                                legendary_creature_index = int(input("Sorry, invalid input! Please enter the index of "
                                                                     "the "
                                                                     "legendary creature "
                                                                     "you want to remove from the habitat (1 - " +
                                                                     str(len(chosen_habitat.
                                                                             get_legendary_creatures_placed())) + "): "))

                            legendary_creature_to_remove: LegendaryCreature = \
                                chosen_habitat.get_legendary_creatures_placed()[legendary_creature_index - 1]
                            new_game.player_data.remove_legendary_creature_from_habitat \
                                (legendary_creature_to_remove, chosen_habitat)

            elif action == "EVOLVE LEGENDARY CREATURE":
                # Clearing up the command line window
                clear()

                # Getting a list of power-up circles in the player's city
                power_up_circles: list = []  # initial value
                for section in new_game.player_data.player_city.get_sections():
                    for x in range(section.SECTION_WIDTH):
                        for y in range(section.SECTION_HEIGHT):
                            curr_tile: CityTile = section.get_tile_at(x, y)
                            if isinstance(curr_tile.building, PowerUpCircle):
                                power_up_circles.append(curr_tile.building)

                # If there are power up circles, ask the player which power-up circle he/she wants to use
                if len(power_up_circles) > 0:
                    print("Below is a list of power up circles that you have.\n")
                    curr_power_up_circle_index: int = 1  # initial value
                    for power_up_circle in power_up_circles:
                        print("POWER UP CIRCLE #" + str(curr_power_up_circle_index))
                        print(str(power_up_circle) + "\n")
                        curr_power_up_circle_index += 1

                    power_up_circle_index: int = int(input("Please enter the index of the power-up circle you want to "
                                                           "use (1 - " + str(len(power_up_circles)) + "): "))
                    while power_up_circle_index < 1 or power_up_circle_index > len(power_up_circles):
                        power_up_circle_index = int(
                            input("Sorry, invalid input! Please enter the index of the power-up circle you want to "
                                  "use (1 - " + str(len(power_up_circles)) + "): "))

                    chosen_power_up_circle: PowerUpCircle = power_up_circles[power_up_circle_index - 1]

                    # Ask the player to choose the legendary creature to be evolved and the materials used if
                    # possible
                    if len(new_game.player_data.legendary_creature_inventory.get_legendary_creatures()) > 0:
                        # Printing all the legendary creatures the player has.
                        for legendary_creature in \
                                new_game.player_data.legendary_creature_inventory.get_legendary_creatures():
                            print(str(legendary_creature) + "\n")

                        # Ask the player to choose the legendary creature to be evolved
                        to_be_evolved_index: int = int(input("Please enter the index of the legendary creature "
                                                             "you want to evolve (1 - " +
                                                             str(len(new_game.
                                                                     player_data.legendary_creature_inventory.get_legendary_creatures())) +
                                                             "): "))
                        while to_be_evolved_index < 1 or to_be_evolved_index > \
                                len(new_game.player_data.legendary_creature_inventory.get_legendary_creatures()):
                            to_be_evolved_index = int(
                                input("Sorry, invalid input! Please enter the index of the legendary creature "
                                      "you want to evolve (1 - " +
                                      str(len(new_game.
                                              player_data.legendary_creature_inventory.get_legendary_creatures())) +
                                      "): "))

                        to_be_evolved: LegendaryCreature = new_game.player_data.legendary_creature_inventory. \
                            get_legendary_creatures()[to_be_evolved_index - 1]

                        materials_to_use: list = []
                        num_materials: int = int(input("How many material legendary creatures do you want to place "
                                                       "(0-" +
                                                       str(min(5,
                                                               len(new_game.player_data.legendary_creature_inventory.
                                                                   get_legendary_creatures()))) +
                                                       "_: "))

                        while num_materials < 0 or num_materials > 5 or num_materials > \
                                len(new_game.player_data.legendary_creature_inventory.get_legendary_creatures()) - 1:
                            num_materials = int(input("Sorry, invalid input! How many material legendary creatures do "
                                                      "you want to place "
                                                      "(0-" +
                                                      str(min(5,
                                                              len(new_game.player_data.legendary_creature_inventory.
                                                                  get_legendary_creatures()))) +
                                                      "_: "))

                        legendary_creature_options: list = new_game.player_data.legendary_creature_inventory. \
                            get_legendary_creatures()
                        legendary_creature_options.remove(to_be_evolved)
                        for i in range(num_materials):
                            print("Below is a list of legendary creatures you can choose as a material.\n")
                            curr_legendary_creature_index: int = 1  # initial value
                            for legendary_creature in legendary_creature_options:
                                print("LEGENDARY CREATURE #" + str(curr_legendary_creature_index))
                                print(str(legendary_creature) + "\n")
                                curr_legendary_creature_index += 1

                            chosen_legendary_creature_index: int = int(input("Please enter the index of the legendary "
                                                                             "creature you want to use as a material "
                                                                             "(1 - " +
                                                                             str(len(legendary_creature_options)) +
                                                                             ": "))
                            while chosen_legendary_creature_index < 1 or chosen_legendary_creature_index > \
                                    len(legendary_creature_options):
                                chosen_legendary_creature_index = int(
                                    input("Sorry, invalid input! Please enter the index of the legendary "
                                          "creature you want to use as a material "
                                          "(1 - " +
                                          str(len(legendary_creature_options)) +
                                          ": "))

                            chosen_material: LegendaryCreature = legendary_creature_options \
                                [chosen_legendary_creature_index - 1]
                            materials_to_use.append(chosen_material)
                            legendary_creature_options.remove(chosen_material)

                        new_game.player_data.evolve_legendary_creature(to_be_evolved, materials_to_use,
                                                                       chosen_power_up_circle)

            elif action == "POWER UP LEGENDARY CREATURE":
                # Clearing up the command line window
                clear()

                # Getting a list of power-up circles in the player's city
                power_up_circles: list = []  # initial value
                for section in new_game.player_data.player_city.get_sections():
                    for x in range(section.SECTION_WIDTH):
                        for y in range(section.SECTION_HEIGHT):
                            curr_tile: CityTile = section.get_tile_at(x, y)
                            if isinstance(curr_tile.building, PowerUpCircle):
                                power_up_circles.append(curr_tile.building)

                # If there are power up circles, ask the player which power-up circle he/she wants to use
                if len(power_up_circles) > 0:
                    print("Below is a list of power up circles that you have.")
                    curr_power_up_circle_index: int = 1  # initial value
                    for power_up_circle in power_up_circles:
                        print("POWER UP CIRCLE #" + str(curr_power_up_circle_index))
                        print(str(power_up_circle) + "\n")
                        curr_power_up_circle_index += 1

                    power_up_circle_index: int = int(input("Please enter the index of the power-up circle you want to "
                                                           "use (1 - " + str(len(power_up_circles)) + "): "))
                    while power_up_circle_index < 1 or power_up_circle_index > len(power_up_circles):
                        power_up_circle_index = int(
                            input("Sorry, invalid input! Please enter the index of the power-up circle you want to "
                                  "use (1 - " + str(len(power_up_circles)) + "): "))

                    chosen_power_up_circle: PowerUpCircle = power_up_circles[power_up_circle_index - 1]

                    # Ask the player to choose the legendary creature to be powered up and the materials used if
                    # possible
                    if len(new_game.player_data.legendary_creature_inventory.get_legendary_creatures()) > 0:
                        # Printing all the legendary creatures the player has.
                        curr_legendary_creature_index: int = 1  # initial value
                        for legendary_creature in \
                                new_game.player_data.legendary_creature_inventory.get_legendary_creatures():
                            print("LEGENDARY CREATURE #" + str(curr_legendary_creature_index))
                            print(str(legendary_creature) + "\n")
                            curr_legendary_creature_index += 1

                        # Ask the player to choose the legendary creature to be powered up
                        to_be_powered_up_index: int = int(input("Please enter the index of the legendary creature "
                                                                "you want to power-up (1 - " +
                                                                str(len(new_game.
                                                                        player_data.legendary_creature_inventory.get_legendary_creatures())) +
                                                                "): "))
                        while to_be_powered_up_index < 1 or to_be_powered_up_index > \
                                len(new_game.player_data.legendary_creature_inventory.get_legendary_creatures()):
                            to_be_powered_up_index = int(
                                input("Sorry, invalid input! Please enter the index of the legendary creature "
                                      "you want to power-up (1 - " +
                                      str(len(new_game.
                                              player_data.legendary_creature_inventory.get_legendary_creatures())) +
                                      "): "))

                        to_be_powered_up: LegendaryCreature = new_game.player_data.legendary_creature_inventory. \
                            get_legendary_creatures()[to_be_powered_up_index - 1]

                        materials_to_use: list = []
                        num_materials: int = int(input("How many material legendary creatures do you want to place "
                                                       "(0-" +
                                                       str(min(5,
                                                               len(new_game.player_data.legendary_creature_inventory.
                                                                   get_legendary_creatures()))) +
                                                       "_: "))

                        while num_materials < 0 or num_materials > 5 or num_materials > \
                                len(new_game.player_data.legendary_creature_inventory.get_legendary_creatures()) - 1:
                            num_materials = int(input("Sorry, invalid input! How many material legendary creatures do "
                                                      "you want to place "
                                                      "(0-" +
                                                      str(min(5,
                                                              len(new_game.player_data.legendary_creature_inventory.
                                                                  get_legendary_creatures()))) +
                                                      "_: "))

                        legendary_creature_options: list = new_game.player_data.legendary_creature_inventory. \
                            get_legendary_creatures()
                        legendary_creature_options.remove(to_be_powered_up)
                        for i in range(num_materials):
                            print("Below is a list of legendary creatures you can choose as a material.\n")
                            curr_legendary_creature_index: int = 1  # initial value
                            for legendary_creature in legendary_creature_options:
                                print("LEGENDARY CREATURE #" + str(curr_legendary_creature_index))
                                print(str(legendary_creature) + "\n")
                                curr_legendary_creature_index += 1

                            chosen_legendary_creature_index: int = int(input("Please enter the index of the legendary "
                                                                             "creature you want to use as a material "
                                                                             "(1 - " +
                                                                             str(len(legendary_creature_options)) +
                                                                             ": "))
                            while chosen_legendary_creature_index < 1 or chosen_legendary_creature_index > \
                                    len(legendary_creature_options):
                                chosen_legendary_creature_index = int(
                                    input("Sorry, invalid input! Please enter the index of the legendary "
                                          "creature you want to use as a material "
                                          "(1 - " +
                                          str(len(legendary_creature_options)) +
                                          ": "))

                            chosen_material: LegendaryCreature = legendary_creature_options \
                                [chosen_legendary_creature_index - 1]
                            materials_to_use.append(chosen_material)
                            legendary_creature_options.remove(chosen_material)

                        new_game.player_data.power_up_legendary_creature(to_be_powered_up, materials_to_use,
                                                                         chosen_power_up_circle)

            elif action == "GIVE ITEM":
                # Clearing up the command line window
                clear()

                # Getting a list of items which are neither runes nor eggs in the player's item inventory
                neither_rune_nor_egg_items: list = [item for item in new_game.player_data.item_inventory.get_items()
                                                    if not isinstance(item, Rune) and not isinstance(item, Egg)]

                # If items which are neither runes nor eggs exist and there are legendary creatures in the
                # legendary creature inventory, ask the player to choose which item is to be given to a
                # legendary creature.
                if len(neither_rune_nor_egg_items) > 0 and \
                        len(new_game.player_data.legendary_creature_inventory.get_legendary_creatures()) > 0:
                    print("Below is a list of items which are neither runes nor eggs that you have.\n")
                    curr_item_index: int = 1  # initial value
                    for item in neither_rune_nor_egg_items:
                        print("ITEM #" + str(curr_item_index))
                        print(str(item) + "\n")
                        curr_item_index += 1

                    item_index: int = int(input("Please enter the index of the item you want to give (1 - " +
                                                str(len(neither_rune_nor_egg_items)) + "): "))
                    while item_index < 1 or item_index > len(neither_rune_nor_egg_items):
                        item_index = int(input("Sorry, invalid input! Please enter the index of the item you want to "
                                               "give (1 - " +
                                               str(len(neither_rune_nor_egg_items)) + "): "))

                    item_to_give: Item = neither_rune_nor_egg_items[item_index - 1]
                    print("Below is a list of legendary creatures you have.\n")
                    curr_legendary_creature_index: int = 1  # initial value
                    for legendary_creature in new_game.player_data.legendary_creature_inventory. \
                            get_legendary_creatures():
                        print("LEGENDARY CREATURE #" + str(curr_legendary_creature_index))
                        print(str(legendary_creature) + "\n")
                        curr_legendary_creature_index += 1

                    legendary_creature_index: int = int(input("Please enter the index of the legendary creature you "
                                                              "want to give the item to (1 - " +
                                                              str(len(new_game.player_data.legendary_creature_inventory.
                                                                      get_legendary_creatures())) + "): "))
                    while legendary_creature_index < 1 or legendary_creature_index > len(
                            new_game.player_data.legendary_creature_inventory.
                                    get_legendary_creatures()):
                        legendary_creature_index = int(
                            input("Sorry, invalid input! Please enter the index of the legendary creature you "
                                  "want to give the item to (1 - " +
                                  str(len(new_game.player_data.legendary_creature_inventory.
                                          get_legendary_creatures())) + "): "))

                    chosen_legendary_creature: LegendaryCreature = new_game.player_data.legendary_creature_inventory. \
                        get_legendary_creatures()[legendary_creature_index - 1]

                    # Give the item to the chosen legendary creature
                    if new_game.player_data.give_item_to_legendary_creature(item_to_give, chosen_legendary_creature):
                        print("You have successfully given " + str(item_to_give.name) + " to " +
                              str(chosen_legendary_creature.name) + ".")
                    else:
                        print("Sorry! Item " + str(item_to_give.name) + " cannot be given to " +
                              str(chosen_legendary_creature.name) + ".")

            elif action == "FEED LEGENDARY CREATURE":
                # Clearing up the command line window
                clear()

                # Printing a list of legendary creatures the player can feed.
                print("Below is a list of legendary creatures you can feed.\n")
                curr_legendary_creature_index: int = 1  # initial value
                for legendary_creature in new_game.player_data.legendary_creature_inventory.get_legendary_creatures():
                    print("LEGENDARY CREATURE #" + str(curr_legendary_creature_index))
                    print(str(legendary_creature) + "\n")
                    curr_legendary_creature_index += 1

                legendary_creature_index: int = int(input("Please enter the index of the legendary "
                                                          "creature you want to feed (1 - " +
                                                          str(len(new_game.player_data.legendary_creature_inventory.
                                                                  get_legendary_creatures())) + "): "))
                while legendary_creature_index < 1 or legendary_creature_index > \
                        len(new_game.player_data.legendary_creature_inventory.get_legendary_creatures()):
                    legendary_creature_index = int(
                        input("Sorry, invalid input! Please enter the index of the legendary "
                              "creature you want to feed (1 - " +
                              str(len(new_game.player_data.legendary_creature_inventory.
                                      get_legendary_creatures())) + "): "))

                chosen_legendary_creature: LegendaryCreature = new_game.player_data.legendary_creature_inventory. \
                    get_legendary_creatures()[legendary_creature_index - 1]
                food: mpf = mpf(input("Please enter the amount of food you want to feed (0 - " +
                                      str(new_game.player_data.food) + "): "))
                while food < 0 or food > new_game.player_data.food:
                    food: mpf = mpf(input("Sorry, invalid input! Please enter the amount of food "
                                          "you want to feed (0 - " +
                                          str(new_game.player_data.food) + "): "))

                new_game.player_data.feed_legendary_creature(chosen_legendary_creature, food)
                print("You have successfully fed " + str(food) + " food to " + str(chosen_legendary_creature.name) +
                      "!")

            elif action == "PLACE EGG":
                # Clearing up the command line window
                clear()

                # Getting a list of hatcheries the player has.
                hatcheries: list = []  # initial value
                for section in new_game.player_data.player_city.get_sections():
                    for x in range(section.SECTION_WIDTH):
                        for y in range(section.SECTION_HEIGHT):
                            curr_tile: CityTile = section.get_tile_at(x, y)
                            if isinstance(curr_tile.building, Hatchery):
                                hatcheries.append(curr_tile.building)

                # Getting a list of eggs the player can place.
                eggs: list = []  # initial value
                for item in new_game.player_data.item_inventory.get_items():
                    if isinstance(item, Egg):
                        if not item.already_placed:
                            eggs.append(item)

                # If there are hatcheries and eggs, ask the player to choose which egg to be placed at which hatchery
                if len(hatcheries) > 0 and len(eggs) > 0:
                    print("Below is a list of hatcheries you have.\n")
                    curr_hatchery_index: int = 1
                    for hatchery in hatcheries:
                        print("HATCHERY #" + str(curr_hatchery_index))
                        print(str(hatchery) + "\n")
                        curr_hatchery_index += 1

                    hatchery_index: int = int(input("Please enter the index of the hatchery "
                                                    "you want to place an egg at (1 - " +
                                                    str(len(hatcheries)) + "): "))
                    while hatchery_index < 1 or hatchery_index > len(hatcheries):
                        hatchery_index = int(input("Sorry, invalid input! Please enter the index of the hatchery "
                                                   "you want to place an egg at (1 - " +
                                                   str(len(hatcheries)) + "): "))

                    chosen_hatchery: Hatchery = hatcheries[hatchery_index - 1]

                    print("Below is a list of eggs you can place.\n")
                    curr_egg_index: int = 1
                    for egg in eggs:
                        print("EGG #" + str(curr_egg_index))
                        print(str(egg) + "\n")
                        curr_egg_index += 1

                    egg_index: int = int(input("Please enter the index of the egg you want to place (1 - " +
                                               str(len(eggs)) + "): "))
                    while egg_index < 1 or egg_index > len(eggs):
                        egg_index = int(input("Sorry, invalid input! Please enter the index of the egg "
                                              "you want to place (1 - " +
                                              str(len(eggs)) + "): "))

                    chosen_egg: Egg = eggs[egg_index - 1]
                    if new_game.player_data.place_egg_in_hatchery(chosen_egg, chosen_hatchery):
                        print("You have succesfully placed " + str(chosen_egg.name) + " at " +
                              str(chosen_hatchery.name) + "!")
                    else:
                        print("Sorry! You cannot place an egg in " + str(chosen_hatchery.name) + "!")

            elif action == "FUSE LEGENDARY CREATURES":
                # Clearing up the command line window
                clear()

                # Getting a list of fusion centers in the player's city
                fusion_centers: list = []  # initial value
                for section in new_game.player_data.player_city.get_sections():
                    for x in range(section.SECTION_WIDTH):
                        for y in range(section.SECTION_HEIGHT):
                            curr_tile: CityTile = section.get_tile_at(x, y)
                            if isinstance(curr_tile.building, FusionCenter):
                                fusion_centers.append(curr_tile.building)

                potential_material_legendary_creatures: list = [legendary_creature for legendary_creature in
                                                                new_game.player_data.legendary_creature_inventory.
                                                                    get_legendary_creatures() if legendary_creature not
                                                                in new_game.player_data.battle_team.
                                                                    get_legendary_creatures() and
                                                                not legendary_creature.placed_in_training_area and
                                                                not legendary_creature.placed_in_habitat]
                # If there are fusion centers and at least two legendary creatures which can be used as materials,
                # ask the user to choose which fusion center to use.
                if len(fusion_centers) > 0 and len(potential_material_legendary_creatures) >= 2:
                    print("Below is a list of fusion centers that you have.\n")
                    curr_fusion_center_index: int = 1  # initial value
                    for fusion_center in fusion_centers:
                        print("FUSION CENTER #" + str(curr_fusion_center_index))
                        print(str(fusion_center) + "\n")
                        curr_fusion_center_index += 1

                    fusion_center_index: int = int(input("Please enter the index of the fusion center you want "
                                                         "to use (1 - " + str(len(fusion_centers)) + "): "))
                    while fusion_center_index < 1 or fusion_center_index > len(fusion_centers):
                        fusion_center_index: int = int(input("Please enter the index of the fusion center you want "
                                                             "to use (1 - " + str(len(fusion_centers)) + "): "))

                    chosen_fusion_center: FusionCenter = fusion_centers[fusion_center_index - 1]

                    print("Below is a list of legendary creatures you can use as materials.\n")
                    curr_legendary_creature_index: int = 1  # initial value
                    for legendary_creature in potential_material_legendary_creatures:
                        print("LEGENDARY CREATURE #" + str(curr_legendary_creature_index))
                        print(str(legendary_creature) + "\n")
                        curr_legendary_creature_index += 1

                    chosen_indices: list = []  # initial value
                    for i in range(2):
                        legendary_creature_index: int = int(input("Please enter the index of the "
                                                                  "legendary creature you want to use (1 - " +
                                                                  str(len(potential_material_legendary_creatures))))
                        while legendary_creature_index < 1 or legendary_creature_index > \
                                len(potential_material_legendary_creatures) or legendary_creature_index in chosen_indices:
                            legendary_creature_index = int(input("Sorry, invalid input! Please enter the index of the "
                                                                 "legendary creature you want to use (1 - " +
                                                                 str(len(potential_material_legendary_creatures))))

                        chosen_indices.append(legendary_creature_index)

                    first_index: int = chosen_indices[0] - 1
                    second_index: int = chosen_indices[0] - 1
                    first_legendary_creature: LegendaryCreature = potential_material_legendary_creatures[first_index]
                    second_legendary_creature: LegendaryCreature = potential_material_legendary_creatures[second_index]
                    new_game.player_data.fuse_legendary_creatures(first_legendary_creature,
                                                                  second_legendary_creature, chosen_fusion_center)

            elif action == "MAKE A WISH":
                # Clearing up the command line window
                clear()

                # Getting a list of temples of wishes in the player's city
                temples_of_wishes: list = []  # initial value
                for section in new_game.player_data.player_city.get_sections():
                    for x in range(section.SECTION_WIDTH):
                        for y in range(section.SECTION_HEIGHT):
                            curr_tile: CityTile = section.get_tile_at(x, y)
                            if isinstance(curr_tile.building, TempleOfWishes):
                                temples_of_wishes.append(curr_tile.building)

                # If there are temples of wishes, ask the player to choose which temple of wishes he/she wants to use
                if len(temples_of_wishes) > 0:
                    print("Below is a list of temples of wishes you can use.")
                    curr_temple_of_wishes_index: int = 1  # initial value
                    for temple_of_wishes in temples_of_wishes:
                        print("TEMPLE OF WISHES #" + str(curr_temple_of_wishes_index))
                        print(str(temple_of_wishes) + "\n")
                        curr_temple_of_wishes_index += 1

                    temple_of_wishes_index: int = int(input("Please enter the index of the temple of wishes "
                                                            "you want to use (1 - " +
                                                            str(len(temples_of_wishes)) + "): "))
                    while temple_of_wishes_index < 1 or temple_of_wishes_index > len(temples_of_wishes):
                        temple_of_wishes_index = int(input("Sorry, invalid input! Please enter the index of the "
                                                           "temple of wishes "
                                                           "you want to use (1 - " +
                                                           str(len(temples_of_wishes)) + "): "))

                    chosen_temple_of_wishes: TempleOfWishes = temples_of_wishes[temple_of_wishes_index - 1]
                    new_game.player_data.make_a_wish(chosen_temple_of_wishes)

            elif action == "MANAGE ITEM INVENTORY":
                # Clearing up the command line window
                clear()
                if len(new_game.player_data.item_inventory.get_items()) > 0:
                    print("Below is a list of items in your item inventory.\n")
                    curr_item_index: int = 1
                    for item in new_game.player_data.item_inventory.get_items():
                        print("ITEM #" + str(curr_item_index))
                        print(str(item) + "\n")
                        curr_item_index += 1

                    print("Enter 'Y' for yes.")
                    print("Enter anything else for no.")
                    sell_item: str = input("Do you want to sell an item? ")
                    if sell_item == "Y":
                        item_index: int = int(input("Please enter the index of the item you want to sell (1 - " +
                                                    str(len(new_game.player_data.item_inventory.get_items())) + "): "))
                        while item_index < 1 or item_index > len(new_game.player_data.item_inventory.get_items()):
                            item_index = int(input("Sorry, invalid input! Please enter the index of the item you "
                                                   "want to sell (1 - " +
                                                   str(len(new_game.player_data.item_inventory.get_items())) + "): "))

                        to_be_sold: Item = new_game.player_data.item_inventory.get_items()[item_index - 1]
                        if new_game.player_data.sell_item(to_be_sold):
                            print("Congratulations! You have earned " + str(to_be_sold.sell_gold_gain) + " gold and " +
                                  str(to_be_sold.sell_gem_gain) + " gems for selling " + str(to_be_sold.name) + "!")
                        else:
                            print("Sorry! " + str(to_be_sold.name) + " cannot be sold!")

                    runes: list = []  # initial value
                    for item in new_game.player_data.item_inventory.get_items():
                        if isinstance(item, Rune):
                            runes.append(item)

                    # Ask the player which rune to level up if there are runes in the item inventory
                    if len(runes) > 0:
                        print("Below is a list of runes you have.\n")
                        curr_rune_index: int = 1  # initial value
                        for rune in runes:
                            print("RUNE #" + str(curr_rune_index))
                            print(str(rune) + "\n")
                            curr_rune_index += 1

                        print("Enter 'Y' for yes.")
                        print("Enter anything else for no.")
                        level_up_rune: str = input("Do you want to level up a rune? ")
                        if level_up_rune == "Y":
                            rune_index: int = int(input("Please enter the index of the rune you want to level "
                                                        "up (1 - " + str(len(runes)) + "): "))
                            while rune_index < 1 or rune_index > len(runes):
                                rune_index = int(input("Sorry, invalid input! Please enter the index of the rune you "
                                                       "want to level "
                                                       "up (1 - " + str(len(runes)) + "): "))

                            chosen_rune: Rune = runes[rune_index - 1]
                            new_game.player_data.level_up_rune(chosen_rune)

            elif action == "MANAGE LEGENDARY CREATURE INVENTORY":
                # Clearing up the command line window
                clear()
                if len(new_game.player_data.legendary_creature_inventory.get_legendary_creatures()) > 0:
                    print("Below is a list of legendary creatures in your legendary creature inventory.\n")
                    curr_legendary_creature_index: int = 1  # initial value
                    for legendary_creature in new_game.player_data.legendary_creature_inventory. \
                            get_legendary_creatures():
                        print("LEGENDARY CREATURE #" + str(curr_legendary_creature_index))
                        print(str(legendary_creature) + "\n")
                        curr_legendary_creature_index += 1

                    legendary_creature_index: int = int(input("Please enter the index of the legendary creature "
                                                              "you want to remove (1 - " +
                                                              str(len(new_game.player_data.
                                                                      legendary_creature_inventory.
                                                                      get_legendary_creatures())) + "): "))
                    while legendary_creature_index < 1 or legendary_creature_index > \
                            len(new_game.player_data.legendary_creature_inventory.get_legendary_creatures()):
                        legendary_creature_index = int(input("Sorry, invalid input! Please enter the "
                                                             "index of the legendary creature "
                                                             "you want to remove (1 - " +
                                                             str(len(new_game.player_data.
                                                                     legendary_creature_inventory.
                                                                     get_legendary_creatures())) + "): "))

                    to_be_removed: LegendaryCreature = \
                        new_game.player_data.legendary_creature_inventory.get_legendary_creatures() \
                            [legendary_creature_index - 1]
                    new_game.player_data.remove_legendary_creature(to_be_removed)

            elif action == "MANAGE BATTLE TEAM":
                # Clearing up the command line window
                clear()
                if len(new_game.player_data.battle_team.get_legendary_creatures()) > 0:
                    print("Below is a list of legendary creatures in your battle team.\n")
                    current_legendary_creature_index: int = 1  # initial value
                    for legendary_creature in new_game.player_data.battle_team.get_legendary_creatures():
                        print("LEGENDARY CREATURE #" + str(current_legendary_creature_index))
                        print(str(legendary_creature) + "\n")
                        current_legendary_creature_index += 1

                    print("Enter 'Y' for yes.")
                    print("Enter anything else for no.")
                    change_leader: str = input("Do you want to change the leader of your team? ")
                    if change_leader == "Y":
                        legendary_creature_index: int = int(input("Please enter the index of the "
                                                                  "legendary creature you want to set as "
                                                                  "the leader of your battle team (1 - " +
                                                                  str(len(new_game.player_data.
                                                                          battle_team.get_legendary_creatures())) +
                                                                  "): "))
                        while legendary_creature_index < 1 or legendary_creature_index > \
                                len(new_game.player_data.battle_team.get_legendary_creatures()):
                            legendary_creature_index = int(input("Sorry, invalid input! Please enter the index of the "
                                                                      "legendary creature you want to set as "
                                                                      "the leader of your battle team (1 - " +
                                                                      str(len(new_game.player_data.
                                                                              battle_team.get_legendary_creatures())) +
                                                                      "): "))

                        new_leader: LegendaryCreature = new_game.player_data.battle_team.get_legendary_creatures() \
                            [legendary_creature_index - 1]
                        new_game.player_data.battle_team.set_leader(new_leader)

                    print("Enter 'Y' for yes.")
                    print("Enter anything else for no.")
                    remove_legendary_creature: str = input("Do you want to remove a legendary creature from "
                                                           "your team? ")
                    if remove_legendary_creature == "Y":
                        legendary_creature_index: int = int(input("Please enter the index of the legendary "
                                                                  "creature you want to remove from "
                                                                  "your battle team (1 - " +
                                                                  str(len(new_game.player_data.
                                                                          battle_team.get_legendary_creatures())) +
                                                                  "): "))
                        while legendary_creature_index < 1 or legendary_creature_index > \
                                len(new_game.player_data.battle_team.get_legendary_creatures()):
                            legendary_creature_index = int(input("Sorry, invalid input! Please enter the index of the "
                                                                 "legendary "
                                                                 "creature you want to remove from "
                                                                 "your battle team (1 - " +
                                                                 str(len(new_game.player_data.
                                                                         battle_team.get_legendary_creatures())) +
                                                                 "): "))

                        to_be_removed: LegendaryCreature = new_game.player_data.battle_team.get_legendary_creatures() \
                            [legendary_creature_index - 1]
                        new_game.player_data.remove_legendary_creature_from_team(to_be_removed)

                if len(new_game.player_data.battle_team.get_legendary_creatures()) < Team.MAX_LEGENDARY_CREATURES:
                    print("Below is a list of legendary creatures you have.\n")
                    current_legendary_creature_index: int = 1  # initial value
                    for legendary_creature in new_game.player_data.legendary_creature_inventory.get_legendary_creatures():
                        if not legendary_creature.placed_in_habitat and \
                                not legendary_creature.placed_in_training_area and \
                                legendary_creature.legendary_creature_id not in [creature.id for creature in
                                                        new_game.player_data.battle_team.get_legendary_creatures()]:
                            print("LEGENDARY CREATURE #" + str(current_legendary_creature_index))
                            print(str(legendary_creature) + "\n")
                            current_legendary_creature_index += 1

                    print("Enter 'Y' for yes.")
                    print("Enter anything else for no.")
                    add_legendary_creature: str = input("Do you want to add a legendary creature to your team? ")
                    if add_legendary_creature == "Y":
                        legendary_creature_index: int = int(input("Please enter the index of the legendary "
                                                                  "creature you want to add to your "
                                                                  "battle team (1 - " +
                                                                  str(len(new_game.player_data.
                                                                          legendary_creature_inventory.
                                                                          get_legendary_creatures())) + "): "))
                        while legendary_creature_index < 1 or legendary_creature_index > \
                                len(new_game.player_data.legendary_creature_inventory.get_legendary_creatures()):
                            legendary_creature_index = int(input("Sorry, invalid input! Please enter the index "
                                                                 "of the legendary "
                                                                 "creature you want to add to your "
                                                                 "battle team (1 - " +
                                                                 str(len(new_game.player_data.
                                                                         legendary_creature_inventory.
                                                                         get_legendary_creatures())) + "): "))

                        to_be_added: LegendaryCreature = \
                            new_game.player_data.legendary_creature_inventory.get_legendary_creatures() \
                                [legendary_creature_index - 1]
                        new_game.player_data.add_legendary_creature_to_team(to_be_added)

            elif action == "MANAGE PLAYER CITY":
                # Clearing up the command line window
                clear()

                # Asking whether the player wants to add a new section to the player city or not
                print("Enter 'Y' for yes.")
                print("Enter anything else for no.")
                add_section: str = input("Do you want to add a new section to your player city for " +
                                         str(new_game.player_data.player_city.section_build_gold_cost) + " gold? ")
                if add_section == "Y":
                    new_game.player_data.add_section_to_player_city()

                # Showing the sections in the player's city
                if len(new_game.player_data.player_city.get_sections()) > 0:
                    section_count: int = 1
                    for section in new_game.player_data.player_city.get_sections():
                        print("----------SECTION #" + str(section_count) + "----------")
                        print(str(section) + "\n")
                        section_count += 1

                    chosen_section_index: int = int(input("Enter the index of the section you want to manage (1 - " +
                                                          str(len(
                                                              new_game.player_data.player_city.get_sections())) + "): "))
                    while chosen_section_index < 1 or chosen_section_index > \
                            len(new_game.player_data.player_city.get_sections()):
                        chosen_section_index = int(input("Sorry, invalid input! Enter the index of the section "
                                                         "you want to manage (1 - " +
                                                         str(len(
                                                             new_game.player_data.player_city.get_sections())) + "): "))

                    chosen_section: Section = new_game.player_data.player_city.get_sections()[chosen_section_index - 1]
                    print("Enter 'LEVEL UP BUILDING' to level up a building at an section tile.")
                    print("Enter 'BUILD BUILDING' to build at an section tile.")
                    print("Enter 'REMOVE BUILDING' to remove a building from an section tile.")
                    valid_sub_actions: list = ["LEVEL UP BUILDING", "BUILD BUILDING", "REMOVE BUILDING"]
                    sub_action: str = input("What do you want to do? ")
                    while sub_action not in valid_sub_actions:
                        print("Enter 'LEVEL UP BUILDING' to level up a building at an section tile.")
                        print("Enter 'BUILD BUILDING' to build at an section tile.")
                        print("Enter 'REMOVE BUILDING' to remove a building from an section tile.")
                        sub_action = input("Sorry, invalid input! What do you want to do? ")

                    if sub_action == "LEVEL UP BUILDING":
                        tile_x: int = int(input("Please enter x-coordinates of the building to be levelled up: "))
                        tile_y: int = int(input("Please enter y-coordinates of the building to be levelled up: "))
                        if new_game.player_data.level_up_building_at_section_tile(chosen_section_index - 1, tile_x,
                                                                                  tile_y):
                            print("You have successfully levelled up " +
                                  str(chosen_section.get_tile_at(tile_x, tile_y).building.name) + "!")
                        else:
                            print("Building level up failed!")
                    elif sub_action == "BUILD BUILDING":
                        tile_x: int = int(input("Please enter x-coordinates of the tile to build at: "))
                        tile_y: int = int(input("Please enter y-coordinates of the tile to build at: "))
                        if isinstance(chosen_section.get_tile_at(tile_x, tile_y), CityTile):
                            curr_tile: CityTile = chosen_section.get_tile_at(tile_x, tile_y)
                            if curr_tile.building is None:
                                print("Below is a list of buildings you can build on the tile.")
                                building_count: int = 1
                                for building in building_shop.get_buildings_sold():
                                    print("BUILDING #" + str(building_count))
                                    print(str(building) + "\n")
                                    building_count += 1

                                building_index: int = int(input("Please enter the index of the building you "
                                                                "want to build (1 - " +
                                                                str(len(building_shop.get_buildings_sold())) + "): "))
                                while building_index < 1 or building_index > len(building_shop.get_buildings_sold()):
                                    building_index = int(input("Sorry, invalid input! Please enter the index of "
                                                               "the building you "
                                                               "want to build (1 - " +
                                                               str(len(building_shop.get_buildings_sold())) + "): "))

                                to_build: Building = building_shop.get_buildings_sold()[building_index - 1]
                                if new_game.player_data.build_at_section_tile(chosen_section_index - 1, tile_x, tile_y,
                                                                              to_build):
                                    print("You have successfully built " + str(to_build.name) + "!")
                                else:
                                    print("Sorry, you cannot build " + str(to_build.name) + "!")
                            else:
                                print("Sorry, you cannot build here!")
                        else:
                            print("Sorry, you cannot build here!")
                    elif sub_action == "REMOVE BUILDING":
                        tile_x: int = int(input("Please enter x-coordinates of the tile to remove building from: "))
                        tile_y: int = int(input("Please enter y-coordinates of the tile to remove building from: "))
                        if new_game.player_data.remove_building_from_section_tile(chosen_section_index - 1, tile_x,
                                                                                  tile_y):
                            print("You have successfully removed a building!")
                        else:
                            print("You failed to remove a building!")

            elif action == "PLAY ADVENTURE MODE":
                # Clearing up the command line window
                clear()

                # Getting a list of levels for the player to choose from.
                print("Below is a list of levels you can choose from.\n")
                curr_level_index: int = 1  # initial value
                for level in new_game.player_data.get_unlocked_levels():
                    print("LEVEL #" + str(curr_level_index))
                    print(str(level) + "\n")
                    curr_level_index += 1

                level_index: int = int(input("Please enter the index of the level "
                                             "you want to battle in (1 - " +
                                             str(len(new_game.player_data.get_unlocked_levels())) + "): "))
                while level_index < 1 or level_index > len(new_game.player_data.get_unlocked_levels()):
                    level_index = int(input("Sorry, invalid input! Please enter the index of the level "
                                            "you want to battle in (1 - " +
                                            str(len(new_game.player_data.get_unlocked_levels())) + "): "))

                chosen_level: Level = new_game.player_data.get_unlocked_levels()[level_index - 1]

                # Start the battle and battle until all stages are cleared
                curr_stage_number: int = 0
                current_stage: Stage = chosen_level.curr_stage(curr_stage_number)
                while chosen_level.next_stage(curr_stage_number) is not None and \
                        not new_game.player_data.battle_team.all_died():
                    # Clearing up the command line window
                    clear()

                    # Show the current stage
                    print("--------------------STAGE #" + str(curr_stage_number + 1) + "--------------------")
                    curr_battle: Battle = Battle(new_game.player_data.battle_team,
                                                 Team(current_stage.get_enemies_list()))
                    while curr_battle.winner is None:
                        # Printing out the stats of legendary creatures in both teams
                        print("Below are the stats of all legendary creatures in player's team.\n")
                        for legendary_creature in curr_battle.team1.get_legendary_creatures():
                            print(str(legendary_creature) + "\n")

                        print("Below are the stats of all legendary creatures in enemy's team.\n")
                        for legendary_creature in curr_battle.team2.get_legendary_creatures():
                            print(str(legendary_creature) + "\n")

                        # Make a legendary creature move
                        curr_battle.get_someone_to_move()
                        assert isinstance(curr_battle.whose_turn, LegendaryCreature), "Cannot proceed with battle!"

                        if not curr_battle.whose_turn.can_move:
                            # Skip turn
                            curr_battle.whose_turn.have_turn(curr_battle.whose_turn, None, "NORMAL HEAL")

                            # Make another legendary creature move
                            curr_battle.get_someone_to_move()
                            assert isinstance(curr_battle.whose_turn, LegendaryCreature), \
                                "Cannot proceed with battle!"

                        # Checking which legendary creature moves
                        if curr_battle.whose_turn in curr_battle.team1.get_legendary_creatures():
                            moving_legendary_creature: LegendaryCreature = curr_battle.whose_turn
                            # Asking the player what he/she wants to do
                            print("Enter 'NORMAL ATTACK' for normal attack.")
                            print("Enter 'NORMAL HEAL' for normal heal.")
                            print("Enter anything else to use a skill (only applicable if you have usable skills).")
                            usable_skills: list = [skill for skill in curr_battle.whose_turn.get_skills()
                                                   if curr_battle.whose_turn.curr_magic_points >=
                                                   skill.magic_points_cost and isinstance(skill, ActiveSkill)]
                            possible_actions: list = ["NORMAL ATTACK", "NORMAL HEAL"]
                            trainer_battle_action: str = input("What do you want to do? ")
                            while len(usable_skills) == 0 and trainer_battle_action not in possible_actions:
                                print("Enter 'NORMAL ATTACK' for normal attack.")
                                print("Enter 'NORMAL HEAL' for normal heal.")
                                trainer_battle_action = input("Sorry, invalid input! What do you want to do? ")

                            if trainer_battle_action not in possible_actions:
                                # Use skill
                                trainer_battle_action = "USE SKILL"

                                # Show a list of skills the player can use
                                print("Below is a list of skills you can use.\n")
                                curr_skill_index: int = 1  # initial value
                                for skill in usable_skills:
                                    print("SKILL #" + str(curr_skill_index))
                                    print(str(skill) + "\n")
                                    curr_skill_index += 1

                                skill_index: int = int(input("Please enter the index of the skill "
                                                             "you want to use (1 - " +
                                                             str(len(usable_skills)) + "): "))
                                while skill_index < 1 or skill_index > len(usable_skills):
                                    skill_index = int(input("Sorry, invalid input! Please enter the "
                                                            "index of the skill "
                                                            "you want to use (1 - " +
                                                            str(len(usable_skills)) + "): "))

                                skill_to_use: ActiveSkill = usable_skills[skill_index - 1]
                                if skill_to_use.active_skill_type == "ATTACK":
                                    # Asking the user to select a target
                                    print("Below is a list of enemies you can attack.")
                                    enemy_index: int = 1  # initial value
                                    for enemy in curr_battle.team2.get_legendary_creatures():
                                        print("ENEMY #" + str(enemy_index))
                                        print(str(enemy) + "\n")
                                        enemy_index += 1

                                    chosen_enemy_index: int = int(input("Please enter the index of the "
                                                                        "enemy you want to attack (1 - " +
                                                                        str(len(curr_battle.
                                                                                team2.get_legendary_creatures())) +
                                                                        "): "))
                                    while chosen_enemy_index < 1 or chosen_enemy_index > len(curr_battle.
                                                                                                     team2.get_legendary_creatures()):
                                        chosen_enemy_index = int(input("Sorry, invalid input! "
                                                                       "Please enter the index of the "
                                                                       "enemy you want to attack (1 - " +
                                                                       str(len(curr_battle.
                                                                               team2.get_legendary_creatures())) +
                                                                       "): "))

                                    chosen_enemy_target: LegendaryCreature = curr_battle.team2. \
                                        get_legendary_creatures()[chosen_enemy_index - 1]
                                    curr_battle.whose_turn.have_turn(chosen_enemy_target, skill_to_use,
                                                                     trainer_battle_action)
                                    if random.random() < chosen_enemy_target.counterattack_chance + \
                                            chosen_enemy_target.counterattack_chance_up:
                                        chosen_enemy_target.counterattack(curr_battle.whose_turn)

                                elif skill_to_use.active_skill_type == "HEAL":
                                    # Asking the user to select who to heal
                                    print("Below is a list of allies you can heal.")
                                    ally_index: int = 1  # initial value
                                    for ally in curr_battle.team1.get_legendary_creatures():
                                        print("ALLY #" + str(ally_index))
                                        print(str(ally) + "\n")
                                        ally_index += 1

                                    chosen_ally_index: int = int(input("Please enter the index of the "
                                                                       "ally you want to heal (1 - " +
                                                                       str(len(curr_battle.
                                                                               team1.get_legendary_creatures())) +
                                                                       "): "))
                                    while chosen_ally_index < 1 or chosen_ally_index > len(curr_battle.
                                                                                                   team1.get_legendary_creatures()):
                                        chosen_ally_index = int(input("Sorry, invalid input! "
                                                                      "Please enter the index of the "
                                                                      "ally you want to heal (1 - " +
                                                                      str(len(curr_battle.
                                                                              team1.get_legendary_creatures())) +
                                                                      "): "))

                                    chosen_ally_target: LegendaryCreature = curr_battle.team1. \
                                        get_legendary_creatures()[chosen_ally_index - 1]
                                    curr_battle.whose_turn.have_turn(chosen_ally_target, skill_to_use,
                                                                     trainer_battle_action)
                                elif skill_to_use.active_skill_type == "ALLIES EFFECT":
                                    # Asking the user to select who to apply ally effect on
                                    print("Below is a list of allies you can apply ally effect on.")
                                    ally_index: int = 1  # initial value
                                    for ally in curr_battle.team1.get_legendary_creatures():
                                        print("ALLY #" + str(ally_index))
                                        print(str(ally) + "\n")
                                        ally_index += 1

                                    chosen_ally_index: int = int(input("Please enter the index of the "
                                                                       "ally you want to apply ally effect on (1 - " +
                                                                       str(len(curr_battle.
                                                                               team1.get_legendary_creatures())) +
                                                                       "): "))
                                    while chosen_ally_index < 1 or chosen_ally_index > len(curr_battle.
                                                                                                   team1.get_legendary_creatures()):
                                        chosen_ally_index = int(input("Sorry, invalid input! "
                                                                      "Please enter the index of the "
                                                                      "ally you want to apply ally effect on (1 - " +
                                                                      str(len(curr_battle.
                                                                              team1.get_legendary_creatures())) +
                                                                      "): "))

                                    chosen_ally_target: LegendaryCreature = curr_battle.team1. \
                                        get_legendary_creatures()[chosen_ally_index - 1]
                                    curr_battle.whose_turn.have_turn(chosen_ally_target, skill_to_use,
                                                                     trainer_battle_action)
                                elif skill_to_use.active_skill_type == "ENEMIES EFFECT":
                                    # Asking the user to select who to apply enemy effect on
                                    print("Below is a list of enemies you can apply enemy effect on.")
                                    enemy_index: int = 1  # initial value
                                    for enemy in curr_battle.team2.get_legendary_creatures():
                                        print("ENEMY #" + str(enemy_index))
                                        print(str(enemy) + "\n")
                                        enemy_index += 1

                                    chosen_enemy_index: int = int(input("Please enter the index of the "
                                                                        "enemy you want to apply enemy effect on"
                                                                        " (1 - " +
                                                                        str(len(curr_battle.
                                                                                team2.get_legendary_creatures())) +
                                                                        "): "))
                                    while chosen_enemy_index < 1 or chosen_enemy_index > len(curr_battle.
                                                                                                     team2.get_legendary_creatures()):
                                        chosen_enemy_index = int(input("Sorry, invalid input! "
                                                                       "Please enter the index of the "
                                                                       "enemy you want to apply enemy effect on"
                                                                       " (1 - " +
                                                                       str(len(curr_battle.
                                                                               team2.get_legendary_creatures())) +
                                                                       "): "))

                                    chosen_enemy_target: LegendaryCreature = curr_battle.team2. \
                                        get_legendary_creatures()[chosen_enemy_index - 1]
                                    curr_battle.whose_turn.have_turn(chosen_enemy_target, skill_to_use,
                                                                     trainer_battle_action)

                            elif trainer_battle_action == "NORMAL ATTACK":
                                # Asking the user to select a target
                                print("Below is a list of enemies you can attack.")
                                enemy_index: int = 1  # initial value
                                for enemy in curr_battle.team2.get_legendary_creatures():
                                    print("ENEMY #" + str(enemy_index))
                                    print(str(enemy) + "\n")
                                    enemy_index += 1

                                chosen_enemy_index: int = int(input("Please enter the index of the "
                                                                    "enemy you want to attack (1 - " +
                                                                    str(len(curr_battle.
                                                                            team2.get_legendary_creatures())) +
                                                                    "): "))
                                while chosen_enemy_index < 1 or chosen_enemy_index > len(curr_battle.
                                                                                                 team2.get_legendary_creatures()):
                                    chosen_enemy_index = int(input("Sorry, invalid input! "
                                                                   "Please enter the index of the "
                                                                   "enemy you want to attack (1 - " +
                                                                   str(len(curr_battle.
                                                                           team2.get_legendary_creatures())) +
                                                                   "): "))

                                chosen_enemy_target: LegendaryCreature = curr_battle.team2. \
                                    get_legendary_creatures()[chosen_enemy_index - 1]
                                curr_battle.whose_turn.have_turn(chosen_enemy_target, None, trainer_battle_action)
                                if random.random() < chosen_enemy_target.counterattack_chance + \
                                        chosen_enemy_target.counterattack_chance_up:
                                    chosen_enemy_target.counterattack(curr_battle.whose_turn)

                            elif trainer_battle_action == "NORMAL HEAL":
                                # Asking the user to select who to heal
                                print("Below is a list of allies you can heal.")
                                ally_index: int = 1  # initial value
                                for ally in curr_battle.team1.get_legendary_creatures():
                                    print("ALLY #" + str(ally_index))
                                    print(str(ally) + "\n")
                                    ally_index += 1

                                chosen_ally_index: int = int(input("Please enter the index of the "
                                                                   "ally you want to heal (1 - " +
                                                                   str(len(curr_battle.
                                                                           team1.get_legendary_creatures())) +
                                                                   "): "))
                                while chosen_ally_index < 1 or chosen_ally_index > len(curr_battle.
                                                                                               team1.get_legendary_creatures()):
                                    chosen_ally_index = int(input("Sorry, invalid input! "
                                                                  "Please enter the index of the "
                                                                  "ally you want to heal (1 - " +
                                                                  str(len(curr_battle.
                                                                          team1.get_legendary_creatures())) +
                                                                  "): "))

                                chosen_ally_target: LegendaryCreature = curr_battle.team1. \
                                    get_legendary_creatures()[chosen_ally_index - 1]
                                curr_battle.whose_turn.have_turn(chosen_ally_target, None,
                                                                 trainer_battle_action)
                            else:
                                pass

                            # Checking the case where the moving legendary creature gets an extra turn
                            if random.random() < moving_legendary_creature.extra_turn_chance + \
                                    moving_legendary_creature.extra_turn_chance_up and \
                                    moving_legendary_creature.can_move:
                                curr_battle.whose_turn = moving_legendary_creature

                                # Recovering magic points
                                curr_battle.whose_turn.recover_magic_points()
                            else:
                                curr_battle.get_someone_to_move()

                        elif curr_battle.whose_turn in curr_battle.team2.get_legendary_creatures():
                            curr_moving_legendary_creature: LegendaryCreature = curr_battle.whose_turn
                            chance: float = random.random()
                            trainer_battle_action: str = "NORMAL ATTACK" if chance <= 1 / 3 else \
                                "NORMAL HEAL" if 1 / 3 < chance <= 2 / 3 else "USE SKILL"
                            usable_skills: list = [skill for skill in curr_battle.whose_turn.get_skills()
                                                   if curr_battle.whose_turn.curr_magic_points >=
                                                   skill.magic_points_cost and isinstance(skill, ActiveSkill)]

                            # If there are no usable skills and 'trainer_battle_action' is set to "USE SKILL",
                            # change the value of 'trainer_battle_action'
                            if len(usable_skills) == 0:
                                trainer_battle_action = "NORMAL ATTACK" if random.random() < 0.5 else "NORMAL HEAL"

                            if trainer_battle_action == "NORMAL ATTACK":
                                # A normal attack occurs
                                moving_legendary_creature: LegendaryCreature = curr_battle.whose_turn
                                target: LegendaryCreature = curr_battle.team1.get_legendary_creatures() \
                                    [random.randint(0, len(curr_battle.team1.get_legendary_creatures()) - 1)]
                                moving_legendary_creature.have_turn(target, None, trainer_battle_action)
                                if random.random() < target.counterattack_chance + \
                                        target.counterattack_chance_up:
                                    target.counterattack(moving_legendary_creature)
                            elif trainer_battle_action == "NORMAL HEAL":
                                # A normal heal occurs
                                moving_legendary_creature: LegendaryCreature = curr_battle.whose_turn
                                target: LegendaryCreature = curr_battle.team2.get_legendary_creatures() \
                                    [random.randint(0, len(curr_battle.team2.get_legendary_creatures()) - 1)]
                                moving_legendary_creature.have_turn(target, None, trainer_battle_action)
                            elif trainer_battle_action == "USE SKILL":
                                # A skill is used
                                moving_legendary_creature: LegendaryCreature = curr_battle.whose_turn
                                skill_to_use: ActiveSkill = usable_skills[random.randint(0, len(usable_skills) - 1)]
                                if skill_to_use.active_skill_type == "ATTACK" or \
                                        skill_to_use.active_skill_type == "ENEMIES EFFECT":
                                    target: LegendaryCreature = curr_battle.team1.get_legendary_creatures() \
                                        [random.randint(0, len(curr_battle.team1.get_legendary_creatures()) - 1)]
                                    moving_legendary_creature.have_turn(target, skill_to_use, trainer_battle_action)
                                    if skill_to_use.active_skill_type == "ATTACK":
                                        if random.random() < target.counterattack_chance + \
                                                target.counterattack_chance_up:
                                            target.counterattack(moving_legendary_creature)
                                else:
                                    target: LegendaryCreature = curr_battle.team2.get_legendary_creatures() \
                                        [random.randint(0, len(curr_battle.team2.get_legendary_creatures()) - 1)]
                                    moving_legendary_creature.have_turn(target, skill_to_use, trainer_battle_action)
                            else:
                                pass

                            # Checking the case where the moving legendary creature gets an extra turn
                            if random.random() < curr_moving_legendary_creature.extra_turn_chance + \
                                    curr_moving_legendary_creature.extra_turn_chance_up and \
                                    curr_moving_legendary_creature.can_move:
                                curr_battle.whose_turn = curr_moving_legendary_creature

                                # Recovering magic points
                                curr_battle.whose_turn.recover_magic_points()
                            else:
                                curr_battle.get_someone_to_move()

                        # Recovering magic points
                        curr_battle.whose_turn.recover_magic_points()

                    if curr_battle.winner == curr_battle.team1:
                        print("Congratulations! You won the battle!")
                        new_game.player_data.claim_reward(curr_battle.reward)
                        current_stage.is_cleared = True

                        # Checking whether the next stage is None or not. If yes, the player has cleared the level
                        if chosen_level.next_stage(curr_stage_number) is None:
                            new_game.player_data.claim_reward(chosen_level.clear_reward)
                            chosen_level.is_cleared = True
                            new_game.player_data.add_unlocked_level()
                        else:
                            # Move on to the next stage
                            current_stage = chosen_level.next_stage(curr_stage_number)
                            curr_stage_number += 1
                    elif curr_battle.winner == curr_battle.team2:
                        print("You lost the battle! Please come back stronger!")

                    # Restore all legendary creatures
                    curr_battle.team1.recover_all()
                    curr_battle.team2.recover_all()

        print("Enter 'Y' for yes.")
        print("Enter anything else for no.")
        continue_playing = input("Do you want to continue playing 'Legendary Creature City Builder'? ")

    # Saving game data and quitting the game.
    save_game_data(new_game, file_name)
    return 0


if __name__ == '__main__':
    main()
