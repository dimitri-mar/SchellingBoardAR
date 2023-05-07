# Copyright (C) 2023-present Associació Heuristica <info@heuristica.barcelona>
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

""" this module manages the database that keeps track of Schelling Board games

The ORM uses sqlalchemy."""
import datetime, uuid

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, \
    DateTime, Float, event, UniqueConstraint
from sqlalchemy.orm import relationship, backref, validates, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func



# Declare a base class for declarative table definitions
Base = declarative_base()


# Define the Match table
class Match(Base):
    """ the experience can be grouped in matches

    A match is a set of games that are played in a specific order.
    Multiple boards can be used to play at the same time. Each board will
    play the games in the same order."""

    __tablename__ = 'matches'
    id = Column(String, primary_key=True)
    # Add any other columns you want for this table
    starting_time = Column(DateTime, nullable=False,
                           server_default=func.now())
    ending_time = Column(DateTime, nullable=True)
    base_url = Column(String, nullable=True)

    #a one to many relationship with the game, table. Each Mattch has several games in a specific order
    # sequence_of_games = relationship('Game',
    #                                  order_by='Game.order_in_match',
    #                                  back_populates='matches')


    games = relationship('Game', back_populates='match', uselist=True)
                         #overlaps='sequence_of_games')
    # at least one game is mandatory
    # sequence_of_games = relationship('Game', back_populates='match',
    #                                  uselist=True, overlaps='match')


    boards = relationship('Board', back_populates='match')

    def __init__(self):
        self.id = datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S') + str(
            uuid.uuid4().hex)

    @validates('games')
    def validate_sequence_of_games(self, key, value):
        if not value:
            raise ValueError('At least one game must be selected for a match')
        return value

    # TODO add metadatas of the match, like how many students will participate, etc.


# Define the Game table
class Game(Base):
    """ A game is a single instance of a Schelling Game, it has a starting and
    will end either after a specific time or when the game is finished."""
    __tablename__ = 'games'
    id = Column(Integer, primary_key=True)

    match_id = Column(Integer, ForeignKey('matches.id'))
    match = relationship('Match', back_populates='games')

    order_in_match = Column(Integer, default=0)
    max_time_minutes = Column(Integer, nullable=True)

    # one-to-one relationship with the dynamics of the game
    game_dynamics_id = Column(Integer, ForeignKey('sgdynamics.id'), default=0)
    game_dynamics = relationship('SGdynamics', backref='game')

    # a one-to-many relationship with the games_per_board table
    games_per_board = relationship('GamePerBoard', back_populates='game')


class Board(Base):
    """ Several boards can play at the same time.

    Here metadata regarding the board are stored"""

    __tablename__ = 'boards'
    id = Column(Integer, primary_key=True)
    # a relation with one single match
    match_id = Column(Integer, ForeignKey('matches.id'))
    match = relationship('Match', back_populates='boards')

    # a one-to-many relationship with the games_per_board table
    games_per_board = relationship('GamePerBoard', back_populates='board', uselist=True)

    #optional:
    n_players = Column(Integer, nullable=True)



class GamePerBoard(Base):
    """ A game per board is a single instance of a game played on a specific
    board.

    It can have a starting and ending time, indipendent from the other boards.
    """
    __tablename__ = 'game_per_board'
    id = Column(Integer, primary_key=True)

    # a relation with one single board
    board_id = Column(Integer, ForeignKey('boards.id'))
    board = relationship('Board', back_populates='games_per_board', uselist=False)
    # a relation with one single game
    game_id = Column(Integer, ForeignKey('games.id'))
    game = relationship('Game', back_populates='games_per_board', uselist=False)

    # I need a constraint that ensures that we have one single game
    # per board per game per board
    #__table_args__ = (UniqueConstraint('board_id', 'game_id', name='_board_game_uc'),)

    starting_time = Column(DateTime, nullable=True)
    ending_time = Column(DateTime, nullable=True)

    # a one-to-many relationship with the pictures table
    pictures = relationship('Picture', back_populates='game_per_board', uselist=True)


# Define the SGdynamics table (Schelling Game dynamics)
class SGdynamics(Base):
    __tablename__ = 'sgdynamics'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True)
    description = Column(String)

    def __str__(self):
        return f"{self.id} - {self.name}: {self.description}"

    @classmethod
    def default_row(cls):
        """ insert the default dynamics of the Schelling Game"""
        return cls(id=0, name='free',
                   description='Free dynamics or not specified')

@event.listens_for(SGdynamics.__table__, 'after_create')
def insert_default_rows_on_create(target, connection, **kw):
    session = Session(bind=connection)
    new_row = SGdynamics.default_row()
    session.add(new_row)
    session.commit()


class Picture(Base):
    __tablename__ = "picture_table"
    picture_id = Column(Integer, primary_key=True)
    picture_user_id = Column(Integer) # the id of the user who uploaded the picture
    picture_hash = Column(String)
    picture_path = Column(String)
    picture_upload_time = Column(DateTime)
    # a column will store the metadata of the picture as raw json string
    picture_metadata = Column(String)
    # each picture can be part of a game per board

    game_per_board_id = Column(Integer, ForeignKey('game_per_board.id'),
                               nullable=True)
    game_per_board = relationship('GamePerBoard', back_populates='pictures')



if __name__ == '__main__':
    import click
    @click.command()
    def create_db():
        """Create the database."""

        engine = create_engine('')

    # Create a SQLAlchemy engine to connect to your database
    engine = create_engine('your_database_url')
    # Create the tables in the databas
    Base.metadata.create_all(engine)
