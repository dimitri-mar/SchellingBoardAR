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
from typing import Callable, Tuple
from loguru import logger

VERSION = "0.1.0"

available_languages = ['en', 'ca', 'es']
default_language = 'ca'


def set_language(lang: str) -> Callable[[str], str]:
    """Set the language of the app.

    Args:
        lang (str): the language to set.

    Returns:
        Callable[[str], str]: a function that translates a string to the
        selected language. In particular gettex propery configured.
    """
    try:
        logger.info(
            "Loading the language: {}".format(st.session_state.language))
        localizator = gettext.translation('base', localedir='locales',
                                          languages=[
                                              st.session_state.language])
        localizator.install()  # TODO: check if this is needed
        return localizator.gettext
    except Exception as e:
        logger.error("Error loading the language: {}".format(e))


if 'language' not in st.session_state:
    st.session_state.language = default_language

options = ['Test', 'Ordered', 'Free']
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
    with st.sidebar:
        st.session_state.language = st.sidebar.selectbox(
            'select your language',
            available_languages,
            index=available_languages.index(
                default_language),
            label_visibility="hidden")
        _ = set_language(st.session_state.language)
        st.markdown(f"""` app version v{VERSION} `""")

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

    if st.session_state.games_number > 1:
        advanced_time_settings = col1.checkbox(
            _('Dou you want advanced time settings?'))
        if not advanced_time_settings:
            st.session_state.games_times = [0]
            st.session_state.games_times[0] = col1.slider(
                _('Select the length of all games in minutes'), min_value=5,
                max_value=59, value=20, step=1)
        else:
            st.session_state.games_times = [0] * st.session_state.games_number
        st.session_state.games_types = []
        for i in range(st.session_state.games_number):
            col1, col2 = st.columns([1, 1])
            st.session_state.games_types.append(col1.selectbox(
                label=_('Choose type for game nº ') + str(i + 1),
                options=options))
            if advanced_time_settings:
                st.session_state.games_times[i] = col2.slider(
                    _('Select the length of game nº') + str(i + 1) + _(
                        ' in minutes'), min_value=5, max_value=59, value=20,
                    step=1)
    else:
        st.session_state_games_types = ['']
        st.session_state.games_types = (
            col1.selectbox(label=_('Choose type for the game'),
                           options=options))
        st.session_state.games_times = col2.slider(
            _('Select the length of game nº') + str(i + 1) + _(' in minutes'),
            min_value=5, max_value=59, value=20, step=1)

    col1, col2 = st.columns([1, 1])
    if col1.button(_('Submit configuration'), use_container_width=True):
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        col2.button(_('Cancel'), use_container_width=True)
        col1.button(_('Confirm'), on_click=nextpage,
                    disabled=(st.session_state.page > 3),
                    use_container_width=True)

    # For testing purposes
    # st.text(st.session_state.games_types)
    # st.text(st.session_state.games_times)


def game_page():
    with st.sidebar:
        st.session_state.language = st.sidebar.selectbox(
            'select your language',
            available_languages,
            index=available_languages.index(
                default_language),
            label_visibility="hidden")
        _ = set_language(st.session_state.language)
        st.markdown(f"""` app version v{VERSION} `""")
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
    with st.sidebar:
        st.session_state.language = st.sidebar.selectbox(
            'select your language',
            available_languages,
            index=available_languages.index(
                default_language),
            label_visibility="hidden")
        _ = set_language(st.session_state.language)
        st.markdown(f"""` app version v{VERSION} `""")
    st.title(_('Results'))
    # Pending: What results to show


if st.session_state.page == 0:
    setting_page()
elif st.session_state.page == st.session_state.games_number + 1:
    results_page()
elif st.session_state.page >= 1:
    game_page()
