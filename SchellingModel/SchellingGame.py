# Copyright (C) 2022-present Associació Heuristica <info@heuristica.barcelona>
#                      and   Dimitri Marinelli <dimi.marin@proton.me>
#
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# A copy of the GNU Affero General Public License is in the LICENSE file
# in the source code repository.

import numpy as np
from scipy.ndimage import convolve

from typing import Union, List, Dict
import numpy.typing as npt


class SchellingBoard:
    def __init__(self,
                 teams:npt.ArrayLike=None,
                 moods:npt.ArrayLike=None,
                 team_names:List=["B", "R"],
                 separator:str="_",
                 mood_map:Dict={"H": 1, "S": -1},
                 empty_value:int=0,
                 ) -> None:
        """ Manages the status of the board of the Schelling game

        The board is encoded in a matrix of strings representing the teams and the moods.
        Ore two matrices, one for the teams and one for the moods.
        It is important to notice that moods can be wrong, while the position of the teams is always correct.

        Args:
            teams (npt.ArrayLike): a 2D array of teams
            moods (npt.ArrayLike): a 2D array of moods
            team_names (List, optional): A list representing the team names. Defaults to ["B", "R"].
            separator (str, optional): separtor betwen team and mood in the matrix. Defaults to "_".
            mood_map (Dict, optional): The mapping between the status of each agent and an integer value. Defaults to {"H": 1, "S": -1}.
            empty_value (int, optional): the integer representing . Defaults to 0.
        """


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

    def count_team_agents(self, team: Union[int, str]) -> int:
        """Return the number of agents of a given team"""
        team = self.parse_team(team)
        return np.count_nonzero(self.teams == team)

    def cont_empty_cells(self) -> int:
        return np.count_nonzero(self.teams == self.empty_value)

    def count_agents_teams(self) -> Dict:
        """Return the number of agents of each team"""
        count =  {team: self.count_team_agents(team) for team in self.team_names}
        count["Empty"] = self.cont_empty_cells()
        return count

    def get_status_cell_str(self,
                            x:int, y:int, separator="_"):
        """Return a string representation of the status of a cell"""

        team = self.teams[y, x]
        mood = self.moods[y, x]

        if team == self.empty_value:
            return "Empty"
        else:
            return f"{self.get_team_str(team)}{separator}{self.get_team_mood(mood)}"



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

    def mood_positions(self, mood: Union[int, str]) ->np.ndarray[np.bool_]:

        mood = self.parse_mood(mood)

        return (self.moods == mood)


    def same_team_neighbours(self, team: Union[int, str], use_cache=True) ->np.ndarray[np.int_]:
        team = self.parse_team(team)

        if use_cache and team in self.same_team_neighbours_cache:
            return self.same_team_neighbours_cache[team]

        position = self.team_positions(team).astype(int)

        kernel = np.array([[1, 1, 1],
                           [1, 0, 1],
                           [1, 1, 1]])

        return convolve(position, kernel, mode="constant")

    def model_happy_cells(self, team: Union[int, str]) ->np.ndarray[np.bool_]:
        """Return a boolean array representing the cells of the team that are happy according to the model"""
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


    def happyness(self, details=False):
        """Return the percentage of happy cells based on the modellized happiness"""

        happiness = {}
        for team in self.team_names:
            team_positions = self.team_positions(team)


            happy_cells = self.model_happy_cells(team)
            sad_cells = ~happy_cells

            # if the cell is of the team and is happy, it should be happy
            pct_happy = np.sum(team_positions & happy_cells) / np.sum(team_positions)
            happiness[team] = pct_happy

        happiness["total"]= np.sum(list(happiness.values())) / len(happiness)

        return happiness


    def segregation(self):
        """Return the segregation of the board"""
        links = 0
        mixed_links = 0
        for i in range(self.teams.shape[0]):
            for j in range(self.teams.shape[1]):
                if self.teams[i,j] != self.empty_value:
                    
                    if j+1 <= self.teams.shape[1]-1:
                        if self.teams[i,j] == self.teams[i,j+1]:
                            links += 1
                        elif self.teams[i,j+1] != self.empty_value:
                            mixed_links += 1
                            links += 1
                    if i+1 <= self.teams.shape[0]-1:                       
                        if self.teams[i,j] == self.teams[i+1,j]:
                            links += 1
                        elif self.teams[i+1,j] != self.empty_value:
                            mixed_links += 1
                            links += 1
 
                    if j+1 <= self.teams.shape[1]-1 and i+1 <= self.teams.shape[0]-1:
                        if self.teams[i,j] == self.teams[i+1,j+1]:
                            links += 1
                        elif self.teams[i+1,j+1] != self.empty_value:
                            mixed_links += 1
                            links += 1

                    if j-1 >= 0 and i+1 <= self.teams.shape[0]-1:                        
                        if self.teams[i,j] == self.teams[i+1,j-1]:
                            links += 1
                        elif self.teams[i+1,j-1] != self.empty_value:
                            mixed_links += 1
                            links += 1
        
        if links > 0:
            return 1-mixed_links/links
        else:
            return -1

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












