""" A stramlit app that displays the loaded picture and the result of the
 grid detection """
import os

import numpy as np
import streamlit as st
from loguru import logger
import datetime, hashlib
import pandas
import time

def countdown(minutes):
    ph = st.empty()
    seconds = minutes*60
    for secs in range(seconds,0,-1):
        mm, ss = minutes, 0
        ph.metric("Countdown", f"{mm:02d}:{ss:02d}")
        time.sleep(1)
    

options= ['Test', 'Ordered', 'Free']
board_names=['Abella','Cabra','Elefant','Gat','Granota','Mico','Os','Serp', 'Tortuga', 'Vaca']
games_types = []
games_times = []

st.title('Schelling Board Game: Manager App')

board_number = st.number_input('Select the number of boards',min_value=1, max_value=10,value=1, step=1)
col1, col2 = st.columns([1,22.3])

for i in range(board_number):
    col1.image('Avatares/' +  board_names[i]+'.png')
    col2.text('Board ' + board_names[i] + ':' + ' hyperlink')

games_number = st.number_input('Select the number of games',min_value=1, max_value=10,value=1, step=1)

col1, col2 = st.columns([1,1])

advanced_time_settings= col1.checkbox('Dou you want advanced time settings?')
if not advanced_time_settings:
    games_times.append(col2.number_input('Select the length of all games in minutes', min_value=5, max_value=59, value=20, step=1))    

col1, col2 = st.columns([1,1])

for i in range(games_number):
   games_types.append(col1.selectbox(label = 'Choose type for game nº ' + str(i+1), options = options))
   if advanced_time_settings:
       games_times.append(col2.number_input('Select the length of game nº' + str(i+1) + ' in minutes', min_value=5, max_value=59, value=20, step=1))

col1, col2 = st.columns([1,1])
if col1.button('Start', use_container_width= True):
    countdown(games_times[0])
col2.button('Stop', use_container_width= True)