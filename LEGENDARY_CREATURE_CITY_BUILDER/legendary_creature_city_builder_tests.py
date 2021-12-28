import glob
import unittest
from unittest.mock import patch
from legendary_creature_city_builder import *


class MyTestCase(unittest.TestCase):
    @patch("legendary_creature_city_builder_client.input")
    def test_input_main_01(self, mocked_input):
        mocked_input.side_effect = ["player 1", "player 1", "N"]
        self.assertEquals(main(), 0)

    @patch("legendary_creature_city_builder_client.input")
    def test_input_main_02(self, mocked_input):
        mocked_input.side_effect = ["player 2", "player 2", "Y", "BUY ITEM", 7021, "Y", "MANAGE PLAYER CITY",
                                    "N", 1, "BUILD BUILDING", 0, 0, 1, "Y", "PLACE EGG", 1, 1, "N"]
        self.assertEquals(main(), 0)

    @patch("legendary_creature_city_builder_client.input")
    def test_input_main_03(self, mocked_input):
        mocked_input.side_effect = ["player 3", "player 3", "Y", "VIEW STATS", "N"]
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

    ################################################################################################################
    # Checking whether the number of saved data files is correct or not
    def test_number_of_files(self):
        self.assertEquals(len([filename for filename in os.listdir(".") if filename[0:5] == "SAVED"]), 3)

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
