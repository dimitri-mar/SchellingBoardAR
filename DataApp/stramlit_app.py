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

""" A streamlit app that displays the loaded picture and the result of the
 grid detection """
import os

import cv2
import numpy as np
import streamlit as st
from loguru import logger
import datetime, hashlib
import gettext

from VisualDetector.ImageLabelPrediction import detect_labels_fast
from VisualDetector.ImagePreprocessing import prepare_img_for_boundary, \
    find_largest_box, correct_perspective
from VisualDetector.VisualUtils import overlap_matrix_to_picture, \
    overlap_bool_matrix_to_picture


st.set_page_config(layout="wide",
                   page_title="The Schelling Board Augmented Reality :)", )

VERSION = "0.1.2"


available_languages = ['en', 'ca', 'es']
default_language = 'en'


def set_language(lang):
    try:
        logger.info(
            "Loading the language: {}".format(st.session_state.language))
        localizator = gettext.translation('base', localedir='locales',
                                          languages=[
                                              st.session_state.language])
        localizator.install() #TODO check if this is needed
        return  localizator.gettext
    except Exception as e:
        logger.error("Error loading the language: {}".format(e))

if 'language' not in st.session_state:
    st.session_state.language = default_language

# _ = set_language(st.session_state.language)



@st.cache_data #@st.cache deprecated
def read_loaded_img(uploaded_file, save_img=True):
    # upload time
    ct = datetime.datetime.now()
    timestamp = ct.timestamp()

    up_file = uploaded_file.read()
    #compute the hash of the uploaded file
    file_hash = hashlib.md5(up_file).hexdigest()
    img_file_name_base = os.path.splitext(uploaded_file.name)[0]

    process_name = "app_" + file_hash + "_" + str(timestamp)
    folder_name = "data/" + process_name

    #imageBGR = cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8),
    #                        cv2.IMREAD_COLOR)
    imageBGR = cv2.imdecode(np.frombuffer(up_file, np.uint8),
                            cv2.IMREAD_COLOR)
    imageRGB = cv2.cvtColor(imageBGR, cv2.COLOR_BGR2RGB)
    # compute a hash of the imageRGB

    if save_img:
        # create a directory in output_dir if it does not exist
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        with open(os.path.join(folder_name, uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())

        #let's save the timestamp
        with open(os.path.join(folder_name, "timestamp.txt"), "w") as f:
            f.write(str(timestamp))



    return process_name,  imageRGB


def save_img_as_dataset(img, img_corrected, img_file_name, grid_x, grid_y,
                        schelling_board=None):
    # TODO add uniqe id to the file name for future refererence
    output_dir = "data"
    # create a directory in output_dir if it does not exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)  # create directory
    # remove extension from file name
    img_file_name_base = os.path.splitext(img_file_name)[0]
    process_name = "app_" + img_file_name_base

    # setup the logger
    logger.add(f"{output_dir}/{process_name}.log", rotation="10 MB")
    logger.info(f"Process name: {process_name}")
    logger.info(f"Grid size: {grid_x}x{grid_y}")
    logger.info(f"Image size: {img.shape[1]}x{img.shape[0]}")
    logger.info(f"Image name: {img_file_name}")
    logger.info(f"Output directory: {output_dir}")

    process_dir = os.path.join(output_dir, process_name)
    if not os.path.exists(process_dir):
        os.makedirs(process_dir)
        logger.info(f"Created directory {process_dir}")

    # save original image
    cv2.imwrite(os.path.join(process_dir, "original.png"), img)
    cv2.imwrite(os.path.join(process_dir, "corrected.png"), img_corrected)

    cell_size = int(img_corrected.shape[1] / grid_x)
    assert cell_size == int(img_corrected.shape[0] / grid_y), \
        "cell size is not the same for x and y"
    logger.info(f"Cell size: {cell_size}")

    # save the cells in a subdirectory
    cells_dir = os.path.join(process_dir, "cell_imgs")
    if not os.path.exists(cells_dir):
        os.makedirs(cells_dir)
        logger.info(f"Created directory {cells_dir}")
        if schelling_board is not None:
            # create directories for all the classes
            for class_name in schelling_board.get_all_classes_str():
                class_dir = os.path.join(cells_dir, class_name)
                os.makedirs(class_dir)
                logger.info(f"Created directory {class_dir}")

    for i in range(grid_x):
        for j in range(grid_y):
            cell = img_corrected[j * cell_size:(j + 1) * cell_size,
                   i * cell_size:(i + 1) * cell_size]
            if schelling_board is not None:
                class_name = schelling_board.get_status_cell_str(i, j)
                cell_path = os.path.join(cells_dir, class_name,
                                         f"cell_{i}_{j}_{process_name}.png")
            else:
                cell_path = os.path.join(cells_dir, f"cell_{i}_{j}_{process_name}.png")
            cv2.imwrite(cell_path, cell)


def starting_page():
    import streamlit as st

    hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
    st.markdown(hide_st_style, unsafe_allow_html=True)
    markdown_container =st.container()

    with st.sidebar:
        st.session_state.language = st.sidebar.selectbox('',
                                                         available_languages)#,
                                                         # index=available_languages.index(
                                                         #     default_language))
        _ = set_language(st.session_state.language)
    uploaded_file = st.file_uploader(_("Choose a file"), key="file_uploader")
    sb_content = st.empty()
    sb_container = sb_content.container()



    empty_main = st.empty()
    main_container = empty_main.container()

    box_colors = [(0, 255, 0), (0, 0, 255), (255, 0, 0)]
    color_names = ["green", "blue", "red"]

    # load the uploaded image into opencv
    if uploaded_file is not None:

        with st.sidebar:
            show_threshold_img = sb_container.checkbox('Threshold_img',
                                                       value=False)
        with sb_container.expander(_("adjust preprocessing parameters")):
            blurry_kernel_size = st.number_input(_('reduce the noise'),
                                                     min_value=0,
                                                     value=5, step=2)
            adaptive_threshold_mode = st.selectbox(
                    "threshold method",
                    ("adaptive_mean", "adaptive_gaussian"))
            dilate_kernel_size = st.number_input(_('increase thickness'),
                                                     min_value=0,
                                                     value=3)
            dilate_iterations = st.number_input(
                    _('times you repeate increase thickness'),
                    min_value=0,
                    value=1)
        with sb_container.form("grid_selection_form"):
            checkbox_val = st.radio(
                    _("Select the box that contains only the grid:"),
                    key="visibility",
                    options=([_("no box matches the grid"), ] + color_names),
                    index=1
                )
                # Every form must have a submit button.
            submitted = st.form_submit_button(_("Submit"))
            if submitted:

                if checkbox_val == _("no box matches the grid"):
                        # grid_string = "no box matches the grid"
                    st.write(
                            _("Please adjust the parameters or take a new picture"))
                else:
                    st.session_state["submitted"] = True

                    def find_color_ix(color_name):
                        return color_names.index(color_name)

                    st.session_state["largest_box"] = \
                            st.session_state["largest_box"][
                                find_color_ix(checkbox_val)]
                    st.experimental_rerun()
                        # sb_content.empty()
                        # main_container.empty()
        cols = sb_container.columns(3, )
        with cols[0]:
            grid_x = sb_container.number_input(_('x grid'),
                                                   min_value=1, max_value=50,
                                                   value=20, step=1,
                                                   key="x_grid",
                                                   help="number of columns in the grid",
                                                   label_visibility="visible")
        with cols[2]:
            grid_y = sb_container.number_input(_("y grid"),
                                                   min_value=1, max_value=50,
                                                   value=20, step=1,
                                                   key="y_grid",
                                                   help=_(
                                                       "number of columns in the grid"),
                                                   label_visibility="visible")
        st.session_state["grid_x"] = grid_x
        st.session_state["grid_y"] = grid_y

        if not submitted or checkbox_val == _("no box matches the grid"):
            if show_threshold_img:
                #col1, thr_col, col2 = main_container.columns(3)
                col1, thr_col = main_container.columns(2)
            #else:
                #col1, col2 = main_container.columns(2)

            process_name, img = read_loaded_img(uploaded_file)

            st.session_state["img"] = img
            st.session_state["img_file_name"] = uploaded_file.name
            st.session_state["process_name"] = process_name

            #with col1:
                #st.image(img, caption=_('Uploaded Image.'),
                         #use_column_width=True, )

            threshold_img = prepare_img_for_boundary(img, False,
                                                     blurry_kernel_size,
                                                     adaptive_threshold_mode,
                                                     dilate_kernel_size,
                                                     dilate_iterations)

            if show_threshold_img:
                with thr_col:
                    st.image(threshold_img, caption=_('Threshold Image.'),
                             use_column_width=True, )

            largest_boxes = find_largest_box(threshold_img,
                                             return_first_n_boxes=3)
            st.session_state["largest_box"] = largest_boxes
            # in col2 show the image img with the largest box drawn
            img2 = img.copy()

            for ix, box in enumerate(largest_boxes):
                # print(ix, box)
                cv2.drawContours(img2, [box], 0, box_colors[ix], 15)

            #with col2:
                #st.image(img2, caption=_('Largest box.'),
                 #        use_column_width=True)
            st.image(img2, caption=_('Largest box.'),
                     use_column_width=True)    

    else:
        with markdown_container:
            st.markdown(f"""
            # """ + _('Welcome to Schelling Board Augmented Reality') + f""" 🙂  
              """ + _('Please upload a picture of the board.') + f"""


        v{VERSION}""")

def second_page():
    import streamlit as st

    hide_st_style = """
                    <style>
                    #MainMenu {visibility: hidden;}
                    footer {visibility: hidden;}
                    header {visibility: hidden;}
                    </style>
                    """
    st.markdown(hide_st_style, unsafe_allow_html=True)
    with st.sidebar:
        st.session_state.language = st.sidebar.selectbox('',
                                                         available_languages)#,
                                                         # index=available_languages.index(
                                                         #     default_language))
        _ = set_language(st.session_state.language)
        show_labels = st.checkbox(_("Show labels"), value=False)




    # st.title("Labelled Board")

    # let's correct the perspective
    img = st.session_state["img"]
    grid_x = st.session_state["grid_x"]
    grid_y = st.session_state["grid_y"]
    largest_box = st.session_state["largest_box"]

    # print(grid_x, grid_y, largest_box)
    img_corrected = correct_perspective(img, largest_box, (grid_x, grid_y))
    board = detect_labels_fast(img_corrected, grid_x, grid_y,
                               #model="../models/cnn_dataset_1.h5")
                               #model="../models/cnn_dataset_evento_2000.h5")
                               model="../models/cnn_dataset_230509_plastica_luce.h5")

    wrong_moods = board.find_wrong_position()
    if show_labels:
        cols2 = st.columns(2, )
        with cols2[1]:
            st.markdown(_("The board is labelled with the following labels: \n"
                        "`B_H`: Blue Happy, `B_S`: Blue Sad, `R_H`: Red Happy, "
                        "`R_S`: Red Sad, "
                        "`Emp`: Empty"))

            annotated_img = \
                overlap_matrix_to_picture(img_corrected, board.to_str_matrix())
            st.image(annotated_img, caption=_('Labelled Image.'))
        with cols2[0]:
            st.write(f"{_('Number of wrong moods')}: {np.sum(wrong_moods)}")

            wrong_image = \
                overlap_bool_matrix_to_picture(img_corrected, wrong_moods)
            st.image(wrong_image, caption=_('Wrong moods.'))
            
    else:
        #st.markdown(f"Number of wrong moods: {np.sum(wrong_moods)}\n"
                    #f"please flip the coin marked with an `X` to the correct ")
        st.markdown(f""+_('Number of wrong moods')+f": {np.sum(wrong_moods)}\n")
        st.markdown(_('please flip the coin marked with an `X` to reach a correct state'))

        wrong_image = \
            overlap_bool_matrix_to_picture(img_corrected, wrong_moods)
        st.image(wrong_image, caption=_('Wrong moods.'))

    with st.sidebar:
        prepare_dataset = st.button(_("Prepare Dataset"), key="prepare_dataset")
        new_image = st.button(_("new picture"), key="new_picture")

        if prepare_dataset:
            save_img_as_dataset(img, img_corrected,
                                st.session_state["img_file_name"],
                                grid_x, grid_y, board,)
        if new_image:
            st.session_state["submitted"] = False
            st.experimental_rerun()




if ("submitted" not in st.session_state) or \
        (not st.session_state["submitted"]):
    starting_page()
else:
    second_page()
