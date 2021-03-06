import glob
import unittest
from unittest.mock import patch
from legendary_creature_city_builder import *


class MyTestCase(unittest.TestCase):
    @patch("legendary_creature_city_builder.input")
    def test_input_main_01(self, mocked_input):
        mocked_input.side_effect = ["player 1", "player 1", "N"]
        self.assertEquals(main(), 0)

    @patch("legendary_creature_city_builder.input")
    def test_input_main_02(self, mocked_input):
        mocked_input.side_effect = ["player 2", "player 2", "Y", "BUY ITEM", 7021, "Y", "MANAGE PLAYER CITY",
                                    "N", 1, "BUILD BUILDING", 0, 0, 1, "Y", "PLACE EGG", 1, 1, "N"]
        self.assertEquals(main(), 0)

    @patch("legendary_creature_city_builder.input")
    def test_input_main_03(self, mocked_input):
        mocked_input.side_effect = ["player 3", "player 3", "Y", "VIEW STATS", "N"]
        self.assertEquals(main(), 0)

    @patch("legendary_creature_city_builder.input")
    def test_input_main_04(self, mocked_input):
        mocked_input.side_effect = ["player 4", "player 4", "Y", "BUY ITEM", 7021, "Y",
                                    "BUY ITEM", 7022, "Y", "MANAGE PLAYER CITY", "N", 1,
                                    "BUILD BUILDING", 0, 0, 1, "Y", "PLACE EGG", 1, 1, "Y",
                                    "PLACE EGG", 1, 1, "N"]
        self.assertEquals(main(), 0)

    @patch("legendary_creature_city_builder.input")
    def test_input_main_05(self, mocked_input):
        mocked_input.side_effect = ["player 5", "player 5", "Y", "BUY ITEM", 7021, "Y",
                                    "BUY ITEM", 7022, "Y", "BUY ITEM", 7023, "Y", "MANAGE PLAYER CITY", "N", 1,
                                    "BUILD BUILDING", 0, 0, 1, "Y", "PLACE EGG", 1, 1, "Y",
                                    "PLACE EGG", 1, 1, "Y", "PLACE EGG", 1, 1, "N"]
        self.assertEquals(main(), 0)

    @patch("legendary_creature_city_builder.input")
    def test_input_main_06(self, mocked_input):
        mocked_input.side_effect = ["player 6", "player 6", "Y", "BUY ITEM", 7021, "Y",
                                    "BUY ITEM", 7022, "Y", "BUY ITEM", 7023, "Y", "BUY ITEM", 7024, "Y",
                                    "MANAGE PLAYER CITY", "N", 1,
                                    "BUILD BUILDING", 0, 0, 1, "Y", "PLACE EGG", 1, 1, "Y",
                                    "PLACE EGG", 1, 1, "Y", "PLACE EGG", 1, 1, "Y", "PLACE EGG", 1, 1, "N"]
        self.assertEquals(main(), 0)

    @patch("legendary_creature_city_builder.input")
    def test_input_main_07(self, mocked_input):
        mocked_input.side_effect = ["player 7", "player 7", "Y", "BUY ITEM", 7021, "Y",
                                    "BUY ITEM", 7022, "Y", "BUY ITEM", 7023, "Y", "BUY ITEM", 7024, "Y",
                                    "BUY ITEM", 7025, "Y",
                                    "MANAGE PLAYER CITY", "N", 1,
                                    "BUILD BUILDING", 0, 0, 1, "Y", "PLACE EGG", 1, 1, "Y",
                                    "PLACE EGG", 1, 1, "Y", "PLACE EGG", 1, 1, "Y", "PLACE EGG", 1, 1,
                                    "Y", "PLACE EGG", 1, 1, "N"]
        self.assertEquals(main(), 0)

    ################################################################################################################
    # Tests in loading users' data from the newly saved files to check whether correct data is represented or not
    def test_load_user_01(self):
        user1_data: Game = load_game_data("SAVED LEGENDARY CREATURE CITY BUILDER GAME DATA - PLAYER 1")
        user1: Player = user1_data.player_data
        self.assertEquals(user1.name, "player 1")
        self.assertEquals(user1.level, 1)
        self.assertEquals(len(user1.item_inventory.get_items()), 0)

    def test_load_user_02(self):
        user2_data: Game = load_game_data("SAVED LEGENDARY CREATURE CITY BUILDER GAME DATA - PLAYER 2")
        user2: Player = user2_data.player_data
        self.assertEquals(user2.name, "player 2")
        self.assertEquals(user2.level, 1)
        self.assertEquals(len(user2.item_inventory.get_items()), 1)

    def test_load_user_03(self):
        user3_data: Game = load_game_data("SAVED LEGENDARY CREATURE CITY BUILDER GAME DATA - PLAYER 3")
        user3: Player = user3_data.player_data
        self.assertEquals(user3.name, "player 3")
        self.assertEquals(user3.level, 1)
        self.assertEquals(len(user3.item_inventory.get_items()), 0)

    def test_load_user_04(self):
        user4_data: Game = load_game_data("SAVED LEGENDARY CREATURE CITY BUILDER GAME DATA - PLAYER 4")
        user4: Player = user4_data.player_data
        self.assertEquals(user4.name, "player 4")
        self.assertEquals(user4.level, 1)
        self.assertEquals(len(user4.item_inventory.get_items()), 2)

    def test_load_user_05(self):
        user5_data: Game = load_game_data("SAVED LEGENDARY CREATURE CITY BUILDER GAME DATA - PLAYER 5")
        user5: Player = user5_data.player_data
        self.assertEquals(user5.name, "player 5")
        self.assertEquals(user5.level, 1)
        self.assertEquals(len(user5.item_inventory.get_items()), 3)

    def test_load_user_06(self):
        user6_data: Game = load_game_data("SAVED LEGENDARY CREATURE CITY BUILDER GAME DATA - PLAYER 6")
        user6: Player = user6_data.player_data
        self.assertEquals(user6.name, "player 6")
        self.assertEquals(user6.level, 1)
        self.assertEquals(len(user6.item_inventory.get_items()), 4)

    def test_load_user_07(self):
        user7_data: Game = load_game_data("SAVED LEGENDARY CREATURE CITY BUILDER GAME DATA - PLAYER 7")
        user7: Player = user7_data.player_data
        self.assertEquals(user7.name, "player 7")
        self.assertEquals(user7.level, 1)
        self.assertEquals(len(user7.item_inventory.get_items()), 5)

    ################################################################################################################
    # Checking whether the number of saved data files is correct or not
    def test_number_of_files(self):
        self.assertEquals(len([filename for filename in os.listdir(".") if filename[0:5] == "SAVED"]), 7)

    ################################################################################################################
    # Delete all the created files with "SAVED DATA" in their name from the directory
    # "LEGENDARY_CREATURE_CITY_BUILDER" in the project after test execution is complete. This is to ensure that
    # all other test cases pass
    def test_remove_all_files(self):
        for f in os.listdir("."):
            if f[0:5] == "SAVED":
                os.remove(f)


if __name__ == '__main__':
    unittest.main()
