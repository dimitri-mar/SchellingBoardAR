import numpy as np
from scipy.ndimage import convolve

from typing import Union


class SchellingBoard:
    def __init__(self, teams=None,
                 moods=None,
                 team_names=["B", "R"],
                 separator="_",
                 mood_map={"H": 1, "S": -1},
                 empty_value=0,
                 ):

        #if (np.unique(teams).size - 1) <= len(team_names):
        #    raise ValueError("teams should contain only the team names")

        assert teams.shape == moods.shape, "teams and moods should have the same shape"

        self.teams = teams
        self.moods = moods
        self.empty_value = empty_value
        self.team_names = team_names
        self.separator = separator
        self.mood_map = mood_map
        self.mood_map_inv = {v: k for k, v in self.mood_map.items()}


        self.same_team_neighbours_cache = {}

    @property
    def n_teams(self):
        return len(self.team_names)

    @property
    def grid_x(self):
        return self.teams.shape[1]

    @property
    def grid_y(self):
        return self.teams.shape[0]

    def get_status_cell_str(self, x, y, separator="_"):
        team = self.teams[y, x]
        mood = self.moods[y, x]

        if team == self.empty_value:
            return "Empty"
        else:
            return f"{self.get_team_str(team)}{separator}{self.get_team_mood(mood)}"

        return "sad"

    def get_all_classes_str(self, separator="_"):
        classes = []
        for team in self.team_names:
            for mood in self.mood_map.keys():
                classes.append(f"{team}{separator}{mood}")

        classes.append("Empty")

        return classes


    def get_team_str(self, team: Union[int]):
        return self.team_names[team - 1]

    def get_team_mood(self, mood: Union[int]):
        return self.mood_map_inv[mood]


    def parse_team(self, team: Union[int, str]):
        if isinstance(team, str):
            team = self.team_names.index(team) + 1

        return team

    def parse_mood(self, mood: Union[int, str]):
        if isinstance(mood, str):
            mood = self.mood_map[mood]

        return mood


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

    def team_positions(self, team: Union[int, str]):
        team = self.parse_team(team)

        return (self.teams == team)

    def empty_positions(self):
        return (self.teams == self.empty_value)

    def mood_positions(self, mood: Union[int, str]):
        mood = self.parse_mood(mood)

        return (self.moods == mood)


    def same_team_neighbours(self, team: Union[int, str], use_cache=True):
        team = self.parse_team(team)

        if use_cache and team in self.same_team_neighbours_cache:
            return self.same_team_neighbours_cache[team]

        position = self.team_positions(team).astype(int)

        kernel = np.array([[1, 1, 1],
                           [1, 0, 1],
                           [1, 1, 1]])

        return convolve(position, kernel, mode="constant")

    def model_happy_cells(self, team: Union[int, str]):
        # TODO implement multiple teams and different thresholds

        other_teams = [t for t in self.team_names if t != team]

        my_neighbours = self.same_team_neighbours(team)

        others_neighbours = 0
        for other_team in other_teams:
            others_neighbours += self.same_team_neighbours(other_team)

        return my_neighbours >= others_neighbours

    def find_wrong_position(self):

        wrong_mood = np.full_like(self.moods, False)

        for team in self.team_names:
            team_positions = self.team_positions(team)
            mood_happy = self.mood_positions("H")
            mood_sad = self.mood_positions("S")

            happy_cells = self.model_happy_cells(team)
            sad_cells = ~happy_cells

            # if the cell is of the team and is happy, it should be happy
            wrong_mood[(team_positions & mood_happy) & ~happy_cells] = True

            # if the cell is of the team and is sad, it should be sad
            wrong_mood[(team_positions & mood_sad) & ~sad_cells] = True

        return wrong_mood








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












