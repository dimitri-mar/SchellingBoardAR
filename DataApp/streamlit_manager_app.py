""" A stramlit app that displays the loaded picture and the result of the
 grid detection """

import streamlit as st
import pandas as pd
import pydeck as pdk
import streamlit_extras as stex
import streamlit_book as stb

options= ['Test', 'Ordered', 'Free']
board_names=['Abella','Cabra','Elefant','Gat','Granota','Mico','Os','Serp', 'Tortuga', 'Vaca']

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
    st.title('Schelling Board Game: Manager App')
    st.title('Data entry')
    
    st.session_state.board_number = st.number_input('Select the number of boards',min_value=1, max_value=10,value=1, step=1)
    
    st.session_state.games_number = st.number_input('Select the number of games',min_value=1, max_value=10,value=1, step=1)
    
    col1, col2 = st.columns([1,22.3])
    
    for i in range(st.session_state.board_number):
        col1.image('Avatares/' +  board_names[i]+'.png')
        col2.text('Board ' + board_names[i] + ':' + ' hyperlink') #Placeholder for hyperlink, maybe a QR Could be used instead
    
    col1, col2 = st.columns([1,1])
        
    advanced_time_settings= col1.checkbox('Dou you want advanced time settings?')
    if not advanced_time_settings:
        st.session_state.games_times = [0]
        st.session_state.games_times[0] = col1.slider('Select the length of all games in minutes', min_value=5, max_value=59, value=20, step=1)
    else:
        st.session_state.games_times = [0]*st.session_state.games_number
    
    col1, col2 = st.columns([1,1])
    if st.session_state.games_number > 1:
        st.session_state.games_types = []
        for i in range(st.session_state.games_number):
           st.session_state.games_types.append(col1.selectbox(label = 'Choose type for game nº ' + str(i+1), options = options))
           if advanced_time_settings:
               st.session_state.games_times = [0]*st.session_state.games_number
               st.session_state.games_times[i] = col2.slider('Select the length of game nº' + str(i+1) + ' in minutes', min_value=5, max_value=59, value=20, step=1)
    else:
        st.session_state_games_types = ['']
        st.session_state.games_types = (col1.selectbox(label = 'Choose type for the game', options = options))
    
    
    if col1.button('Submit configuration', use_container_width= True):
        col1, col2, col3, col4 = st.columns([1,1,1,1])
        col2.button('Cancel', use_container_width=True)
        col1.button('Confirm', on_click=nextpage, disabled = (st.session_state.page > 3), use_container_width=True)
            
def game_page():
    st.title('Schelling Board Game: Manager App')
    st.header('Game '+ str(st.session_state.page)+ ': '+st.session_state.games_types[st.session_state.page-1])
    col1, col2, col3, col4 = st.columns([1,6.48,6.48,6.48])
    
    for i in range(st.session_state.board_number):
        col1.image('Avatares/' +  board_names[i]+'.png')
        col2.text('Board ' + board_names[i] + ': ')
        col3.text('State') #Placeholder: Should show wether the board has started playing.
        col4.text(' Timer') #Placeholder: Should show time left for corresponding board.
    
    col1, col2 = st.columns([1,1])
    
    if st.session_state.page ==st.session_state.games_number:
        end_message = 'Finish last game and proceed to results'
    else:
        end_message = 'Finish this game and start next one'
    
    if col1.button(end_message, use_container_width= True):
        col1, col2, col3, col4 = st.columns([1,1,1,1])
        col2.button('Cancel', use_container_width=True)
        col1.button('Confirm', on_click=nextpage, disabled = (st.session_state.page > 11), use_container_width=True)            

def results_page():
    st.title('Results')    
    #Pending: What results to show
    
if st.session_state.page == 0:        
    setting_page()
elif st.session_state.page == st.session_state.games_number + 1:
    results_page()
elif st.session_state.page >= 1:
    game_page()
