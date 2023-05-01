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

from glob import glob
import os 
import pandas as pd
import matplotlib.pylab as plt
from PIL import Image



def file_selection():
    import streamlit as st

    st.set_page_config(layout="wide",
                       page_title="The Schelling Board Augmented Reality :)", )

    hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
    st.markdown(hide_st_style, unsafe_allow_html=True)

    st.markdown("# Teams activities")
    data_path = "data_processed"


    file_data_list =  glob(os.path.join(data_path, "*","*.pkl"))
    file_data_list.sort()
    print(file_data_list)
    n_teams =  len(file_data_list)

    col = st.columns(n_teams)

    team_pictures = {}
    
    for ix, f_team in enumerate(file_data_list):
        print(ix, f_team)
        team_name = os.path.basename(os.path.dirname(f_team))
        team_pictures[team_name] = pd.read_pickle(f_team)
        fig, ax = plt.subplots()
        ax = team_pictures[team_name] ["datetime"].hist(
            ax=ax, bins=60)
        ax.set_title(team_name)
        col[ix].pyplot(fig, )
    
    selected = st.selectbox("teams data", team_pictures.keys() )

    pagination_size = 10 

    if selected is not None:
        img_lst = []
        for ix in range(10):

            #ix = 0
            img_df = team_pictures[selected]
            row = img_df.iloc[ix]

            image_path = row["image_path"]
            img     = Image.open(image_path)
            img_lst.append(img)

            st.image(img, caption=image_path, width=300 )
        #st.table(img_lst)



    #ret = st.dataframe(df_images["datetime"])
    #print(df_images["DateTime"].info())
    









file_selection()