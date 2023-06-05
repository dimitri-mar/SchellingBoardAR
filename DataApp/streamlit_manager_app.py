# Copyright (C) 2023-present Aleix Nicolás Olivé <aleix.niol@gmail.com>
#
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
import streamlit as st
import gettext
from loguru import logger

from DataApp.AppManager import AppManager
from MatchManager.MatchManager import MatchManager


# handle multiple languages
_ = gettext.gettext
st.session_state.language = st.sidebar.selectbox('', ['en', 'ca', 'es'])

try:
    localizator = gettext.translation('base', localedir='locales',
                                      languages=[st.session_state.language])
    localizator.install()
    _ = localizator.gettext
except:
    pass

# manage match
# We first load the AppManager
app_manager = AppManager()
app_manager.init_db_connection()
# the match manager handles the match evolution
mm = MatchManager(db_engine=app_manager.db_engine)

# is the match started already?
match_started = mm.is_match_started()

game_dynamics_labels = mm.get_available_dynamics_labels()
game_dynamics_long_description= mm.get_available_name_description()

gd_helper_description = "  \n".join([
    "**{name}** - {description}".format(name=name, description=description)
    for name, description in game_dynamics_long_description.items()])

gd_helper_description  = "Type of games available are:  \n" + gd_helper_description



options = game_dynamics_labels.values()
board_names = ['Abella', 'Cabra', 'Elefant', 'Gat', 'Granota', 'Mico', 'Os',
               'Serp', 'Tortuga', 'Vaca']

if "page" not in st.session_state:
    st.session_state.page = 0

if "games_number" not in st.session_state:
    st.session_state.games_number = 0

if "board_number" not in st.session_state:
    st.session_state.board_number = 0


def nextpage(): st.session_state.page += 1


def restart(): st.session_state.page = 0


def create_list_empty_strings(n):
    return ['' for _ in range(n)]


def setting_page():
    st.title(_('Schelling Board Game: Manager App'))
    st.title(_('Data entry'))

    st.session_state.board_number = st.number_input(
        _('Select the number of boards'), min_value=1, max_value=10, value=1,
        step=1)

    st.session_state.games_number = st.number_input(
        _('Select the number of games'), min_value=1, max_value=10, value=1,
        step=1)

    for i in range(st.session_state.board_number):
        col1, col2 = st.columns([1, 10])
        col1.image('Avatares/' + board_names[i] + '.png', width=23)
        col2.text(_('Board ') + board_names[
            i] + ':' + ' hyperlink')  # Placeholder for hyperlink, maybe a QR Could be used instead

    col1, col2 = st.columns([1, 1])

    advanced_time_settings = col1.checkbox(
        _('Dou you want advanced time settings?'))
    if not advanced_time_settings:
        st.session_state.games_times = [0]
        st.session_state.games_times[0] = col1.slider(
            _('Select the length of all games in minutes'), min_value=5,
            max_value=59, value=20, step=1)
    else:
        st.session_state.games_times = [0] * st.session_state.games_number

    if st.session_state.games_number >= 1:
        st.session_state.games_types = []
        for i in range(st.session_state.games_number):
            col1, col2 = st.columns([1, 1])
            st.session_state.games_types.append(col1.selectbox(
                label=_('Choose type for game nº ') + str(i + 1),
                options=options, help=gd_helper_description ))
            if advanced_time_settings:
                st.session_state.games_times = [
                                                   0] * st.session_state.games_number
                st.session_state.games_times[i] = col2.slider(
                    _('Select the length of game nº') + str(i + 1) + _(
                        ' in minutes'), min_value=5, max_value=59, value=20,
                    step=1)
    else:
        st.session_state_games_types = ['']
        st.session_state.games_types = (
            col1.selectbox(label=_('Choose type for the game'),
                           options=options, help=gd_helper_description))

    def submit_config():
        """ this utility function converts the data from the form into a
        version compatible with the database """

        logger.debug(f"board_number= { st.session_state.board_number}")
        logger.debug(f"games_number= { st.session_state.games_number}")
        logger.debug(f"is_advnced= { advanced_time_settings}")
        logger.debug(f"game_types= { st.session_state.games_types}")
        logger.debug(f"game_times= { st.session_state.games_times}")

        boards = board_names[:st.session_state.board_number]
        n_games = len(st.session_state.games_types)
        assert n_games == st.session_state.games_number, \
               "The number of games types and the number of games must be the same"

        if advanced_time_settings:
            times = st.session_state.games_times
        else:
            times = [st.session_state.games_times[0], ] * n_games

        assert len(times) == n_games, \
                "The number of games times and the number of games must be the same"

        mm.create_match(boards=boards,
                        game_types=st.session_state.games_types,
                        game_times=times,)
        nextpage()


    col1, col2 = st.columns([1, 1])
    if col1.button(_('Submit configuration'), use_container_width=True):
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        col2.button(_('Cancel'), use_container_width=True)
        col1.button(_('Confirm'), on_click=submit_config,
                    disabled=(st.session_state.page > 3),
                    use_container_width=True)


def game_page():
    st.title(_('Schelling Board Game: Manager App'))
    st.header(_('Game ') + str(st.session_state.page) + ': ' +
              st.session_state.games_types[st.session_state.page - 1])

    for i in range(st.session_state.board_number):
        col1, col2, col3, col4 = st.columns([1, 6, 6, 6])
        col1.image('Avatares/' + board_names[i] + '.png', width=23)
        col2.text(_('Board ') + board_names[i] + ': ')
        col3.text(
            _('State'))  # Placeholder: Should show wether the board has started playing.
        col4.text(
            _(' Timer'))  # Placeholder: Should show time left for corresponding board.

    col1, col2 = st.columns([1, 1])

    if st.session_state.page == st.session_state.games_number:
        end_message = _('Finish last game and proceed to results')
    else:
        end_message = _('Finish this game and start next one')

    if col1.button(end_message, use_container_width=True):
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        col2.button(_('Cancel'), use_container_width=True)
        col1.button(_('Confirm'), on_click=nextpage,
                    disabled=(st.session_state.page > 11),
                    use_container_width=True)


def results_page():
    st.title(_('Results'))
    # Pending: What results to show


if st.session_state.page == 0:
    setting_page()
elif st.session_state.page == st.session_state.games_number + 1:
    results_page()
elif st.session_state.page >= 1:
    game_page()
