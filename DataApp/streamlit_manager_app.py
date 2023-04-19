""" A stramlit app that displays the loaded picture and the result of the
 grid detection """
import os

import numpy as np
import streamlit as st
from loguru import logger
import datetime, hashlib
import pandas

options= ['Test', 'Ordered', 'Free']
board_names=['1','2','3','4','5','6','7','8','9','10']
games_types = []
games_times = []

st.title('Schelling Board Game: Manager App')

board_number = st.number_input('Select the number of boards',min_value=1, max_value=10,value=1, step=1)
for i in range(board_number):
    st.text('Board ' + board_names[i] + ':' + ' hyperlink')

games_number = st.number_input('Select the number of games',min_value=1, max_value=10,value=1, step=1)


for i in range(games_number):
   games_types.append(st.selectbox(label = 'Choose type for game nº ' + str(i+1), options = options))
   fixed_time= st.checkbox('Do you want a fixed ammount of time for game nº ' + str(i+1) + ' ?')
   if fixed_time is True:
       games_times.append(st.number_input('Select the length of game nº' + str(i+1) + ' in minutes', min_value=5, max_value=30, value=5, step=1))
   
st.button('Stop')