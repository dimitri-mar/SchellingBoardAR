from unittest import TestCase
from SchellingModel.SchellingGame import SchellingBoard

import numpy as np


class TestSchellingBoard(TestCase):

    @staticmethod
    def default_sb():
        board_teams = [[1, 2, 3, 1],
                       [0, 2, 1, 0],
                       [3, 1, 2, 1]]
        board_moods = [[1, -1, 1, -1],
                       [0, 1, -1, 0],
                       [1, -1, 1, 1]]

        sb = SchellingBoard(
            teams=np.array(board_teams),
            moods=np.array(board_moods),
            team_names=["Red", "Blue", "Green"]
        )

        return sb
    def test__init__(self):
        board_teams = [[1, 2, 3, 1],
                       [0, 2, 1, 0],
                       [3, 1, 2, 1]]
        board_moods = [[1, -1, 1, -1],
                       [0, 1, -1, 0],
                       [1, -1, 1, 1]]

        board_moods_wrong_shape = [[1, -1, 1],
                                   [0, 1, -1],
                                   [1, -1, 1]
                                   ]

        # wrong number of teams
        self.assertRaises(ValueError,
                          SchellingBoard, np.array(board_teams),
                                        np.array(board_moods)
                          )

        # all good
        sb = SchellingBoard(
            teams=np.array(board_teams),
            moods=np.array(board_moods),
            team_names=["Red", "Blue", "Green"]
        )

        # mismetch of board shape of tems and moods
        self.assertRaises(AssertionError,
                          SchellingBoard, np.array(board_teams),
                                        np.array(board_moods_wrong_shape),
                          team_names=["Red", "Blue", "Green"]

                          )

    def test_n_teams(self):
        board_teams = [[1, 2, 3, 1],
                       [0, 2, 1, 0],
                       [3, 1, 2, 1]]
        board_moods = [[1, -1, 1, -1],
                       [0, 1, -1, 0],
                       [1, -1, 1, 1]]

        sb = SchellingBoard(
            teams=np.array(board_teams),
            moods=np.array(board_moods),
            team_names=["Red", "Blue", "Green"]
        )

        self.assertEqual(sb.n_teams, 3)


    def test_count_team_agents(self):
        board_teams = [[1, 2, 3, 1],
                       [0, 2, 1, 0],
                       [3, 1, 2, 1]]
        board_moods = [[1, -1, 1, -1],
                       [0, 1, -1, 0],
                       [1, -1, 1, 1]]

        sb = SchellingBoard(
            teams=np.array(board_teams),
            moods=np.array(board_moods),
            team_names=["Red", "Blue", "Green"]
        )
        assert sb.count_team_agents(1) ==  sb.count_team_agents("Red") == 5
        assert sb.count_team_agents(2) == sb.count_team_agents("Blue") == 3
        assert sb.count_team_agents(3) == sb.count_team_agents("Green") == 2

    def test_count_empty_cells(self):
        board_teams = [[1, 2, 3, 1],
                       [0, 2, 1, 0],
                       [3, 1, 2, 1]]
        board_moods = [[1, -1, 1, -1],
                       [0, 1, -1, 0],
                       [1, -1, 1, 1]]

        sb = SchellingBoard(
            teams=np.array(board_teams),
            moods=np.array(board_moods),
            team_names=["Red", "Blue", "Green"]
        )
        assert sb.count_empty_cells() == 2


    def test_count_agents_teams(self):
        board_teams = [[1, 2, 3, 1],
                       [0, 2, 1, 0],
                       [3, 1, 2, 1]]
        board_moods = [[1, -1, 1, -1],
                       [0, 1, -1, 0],
                       [1, -1, 1, 1]]

        sb = SchellingBoard(
            teams=np.array(board_teams),
            moods=np.array(board_moods),
            team_names=["Red", "Blue", "Green"]
        )


        assert sb.count_agents_teams() == {"Red": 5, "Blue": 3,
                                           "Green": 2, "Empty": 2}

    def test_get_status_cell_str(self):
        sb = self.default_sb()
        print(sb.get_status_cell_str(0, 0))
        assert sb.get_status_cell_str(0, 0) == "Red_H"
        assert sb.get_status_cell_str(0, 1) == "Empty"





    def test_get_all_classes_str(self):
        sb = self.default_sb()
        print(sb.get_all_classes_str())
        assert  ['Red_H', 'Red_S', 'Blue_H', 'Blue_S', 'Green_H', 'Green_S', 'Empty'] == sb.get_all_classes_str()

    def test_get_team_str(self):
        sb = self.default_sb()
        assert sb.get_team_str(3) == "Green"

    def test_get_team_mood(self):
        sb = self.default_sb()
        sb.get_team_mood(1) == "H"

    def test_parse_team(self):
        sb = self.default_sb()
        assert sb.parse_team("Red") == 1
        assert sb.parse_team(1)  == 1


    def test_parse_mood(self):
        sb = self.default_sb()
        assert sb.parse_mood("H") == 1
        assert sb.parse_mood(1) == 1


    def test_teams_str(self):
        print(self.default_sb().teams_str())

    def test_moods_str(self):
        pass # TODO

    def test_to_str_matrix(self):
        #todo
        sb = self.default_sb()
        print(sb.to_str_matrix())

    def test_team_positions(self):
        self.fail()

    def test_empty_positions(self):
        self.fail()

    def test_mood_positions(self):
        self.fail()

    def test_same_team_neighbours(self):
        self.fail()

    def test_model_happy_cells(self):
        self.fail()

    def test_find_wrong_position(self):
        self.fail()

    def test_happyness(self):
        self.fail()

    def test_segregation(self):
        board_teams = [
            [1,0,2,0],
            [2,1,0,0],
            [3,2,3,0],
        ]
        board_moods = [
            [1,0,-1,0],
            [1,1,0,0],
            [-1,-1,-1,0],
        ]

        sb = SchellingBoard(
            teams=np.array(board_teams),
            moods=np.array(board_moods),
            team_names=["Red", "Blue", "Green"]
        )

        segregation = sb.segregation()
        assert  np.isclose(segregation, 2/11)

