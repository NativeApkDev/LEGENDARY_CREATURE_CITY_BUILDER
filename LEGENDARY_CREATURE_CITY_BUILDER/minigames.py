"""
This file contains code for minigames in the game "Legendary Creature City Builder".
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


class Minigame:
    """
    This class contains attributes of a minigame in this game.
    """

    POSSIBLE_NAMES: list = ["BOX EATS PLANTS", "MATCH WORD PUZZLE", "MATCH-3 GAME"]

    def __init__(self, name):
        # type: (str) -> None
        self.name: str = name
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
                               "EXCEPT",
                               "FALSE", "FINALLY", "FOR", "FROM", "GLOBAL", "IF", "IMPORT", "IN", "IS", "LAMBDA",
                               "NONE",
                               "NONLOCAL", "NOT", "OR", "PASS", "RAISE", "RETURN", "TRUE", "TRY", "WHILE", "WITH",
                               "YIELD"]

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
                               "EXCEPT",
                               "FALSE", "FINALLY", "FOR", "FROM", "GLOBAL", "IF", "IMPORT", "IN", "IS", "LAMBDA",
                               "NONE",
                               "NONLOCAL", "NOT", "OR", "PASS", "RAISE", "RETURN", "TRUE", "TRY", "WHILE", "WITH",
                               "YIELD"]

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
