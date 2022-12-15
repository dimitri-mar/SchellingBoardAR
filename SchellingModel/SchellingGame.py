import numpy as np
from scipy.ndimage import convolve

from typing import Union


class SchellingBoard:
    def __init__(self, teams=None,
                 moods=None,
                 team_names=["R", "B"],
                 separator="_",
                 mood_map={"H": 1, "S": -1},
                 empty_value=0,
                 ):

        if (np.unique(teams).size - 1) != len(team_names):
            raise ValueError("teams should contain only the team names")

        assert teams.shape == moods.shape, "teams and moods should have the same shape"

        self.teams = teams
        self.moods = moods
        self.empty_value = empty_value
        self.team_names = team_names
        self.separator = separator
        self.mood_map = mood_map

    @property
    def n_teams(self):
        return len(self.team_names)

    @property
    def grid_x(self):
        return self.teams.shape[1]

    @property
    def grid_y(self):
        return self.teams.shape[0]


    def teams_str(self, append_separator=True):
        """Return a string representation of the teams matrix"""
        team_str = np.empty_like(self.teams, dtype=np.str_)
        for i, team in enumerate(self.team_names):
            team_str[self.teams == (i + 1)] = \
                (team + self.separator) if append_separator else team

        return team_str

    def moods_str(self):
        mood_str = np.empty_like(self.moods, dtype=np.str_)
        for mood, value in self.mood_map.items():
            mood_str[self.moods == value] = mood

        return mood_str

    def to_str_matrix(self):
        return \
            np.char.add(self.teams_str(append_separator=True),
                        self.moods_str())


class SchellingGame:
    def __init__(self, grid_x, grid_y, threshold=0.5, n_teams=2):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.threshold = threshold
        self.n_teams = n_teams

        if n_teams != 2:
            raise NotImplementedError("Only implemented for 2 teams")

    @classmethod
    def from_board(cls, board_status, threshold=0.5):
            n_teams = board_status.n_teams
            return cls(board_status.grid_x, board_status.grid_y, n_teams)












