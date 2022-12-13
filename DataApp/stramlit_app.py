""" A stramlit app that displays the loaded picture and the result of the
 grid detection """
import streamlit as st
import cv2
import numpy as np

from loguru import logger
import os

from VisualDetector.Img2Game import parse_grid_string
from VisualDetector.ImagePreprocessing import prepare_img_for_boundary, \
    find_largest_box, correct_perspective

@st.cache
def read_loaded_img(uploaded_file):
    imageBGR =  cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8),
                        cv2.IMREAD_COLOR)
    imageRGB = cv2.cvtColor(imageBGR , cv2.COLOR_BGR2RGB)
    return imageRGB




def save_img_as_dataset(img, img_corrected, img_file_name, grid_x, grid_y):

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

    cell_size = int(img_corrected.shape[1] / grid_x)
    assert cell_size == int(img_corrected.shape[0] / grid_y), \
            "cell size is not the same for x and y"
    logger.info(f"Cell size: {cell_size}")

    # save the cells in a subdirectory
    cells_dir = os.path.join(process_dir, "cell_imgs")
    if not os.path.exists(cells_dir):
        os.makedirs(cells_dir)
        logger.info(f"Created directory {cells_dir}")
    for i in range(grid_x):
        for j in range(grid_y):
            cell = img_corrected[j * cell_size:(j + 1) * cell_size,
                   i * cell_size:(i + 1) * cell_size]
            cv2.imwrite(
                os.path.join(cells_dir, f"cell_{i}_{j}_{process_name}.png"),
                cell)
def second_page():
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


    st.title("Second Page")
    st.write("Here's our second page")

    # let's correct the perspective
    img = st.session_state["img"]
    grid_x = st.session_state["grid_x"]
    grid_y = st.session_state["grid_y"]
    largest_box = st.session_state["largest_box"]

    # print(grid_x, grid_y, largest_box)
    img_corrected = correct_perspective(img, largest_box, (grid_x, grid_y))
    cols2 = st.columns(3, )
    with cols2[0]:
        st.image(img_corrected, caption='Corrected Image.', )

    with st.sidebar:
        prepare_dataset = st.button("Prepare Dataset", key="prepare_dataset")
        new_image = st.button("new picture", key="new_picture")

        if prepare_dataset:
            save_img_as_dataset(img, img_corrected,
                                st.session_state["img_file_name"],
                                grid_x, grid_y)
        if new_image:
            st.session_state["submitted"] = False
            st.experimental_rerun()


def starting_page():
    import streamlit as st

    st.set_page_config(layout="wide",
                           page_title="The Schelling Board Augmented Reality :)",)

    hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
    st.markdown(hide_st_style, unsafe_allow_html=True)




    with st.sidebar:
        uploaded_file = st.file_uploader("Choose a file")
        sb_content = st.empty( )
        sb_container = sb_content.container()

    empty_main = st.empty()
    main_container = empty_main.container()

    box_colors = [(0, 255, 0), (0, 0, 255), (255, 0, 0)]
    color_names = ["green", "blue", "red"]


    # load the uploaded image into opencv
    if uploaded_file is not None:

        with st.sidebar:
            show_threshold_img = sb_container.checkbox('Threshold_img', value=False)
            with sb_container.expander("adjust preprocessing parameters"):
                blurry_kernel_size = st.number_input('reduce the noise',
                                                     min_value=0,
                                                     value=5, step=2)
                adaptive_threshold_mode = st.selectbox(
                    "threshold method",
                    ("adaptive_mean", "adaptive_gaussian") )
                dilate_kernel_size = st.number_input('increase thickness',
                                                     min_value=0,
                                                     value=3)
                dilate_iterations = st.number_input('times you repeate increase thickness',
                                                    min_value=0,
                                                    value=1)
            with sb_container.form("grid_selection_form"):
                checkbox_val = st.radio(
                    "Select the box that contains only the grid:",
                    key="visibility",
                    options=(["no box matches the grid",] + color_names)
                )
                # Every form must have a submit button.
                submitted = st.form_submit_button("Submit")
                if submitted:

                    if checkbox_val == "no box matches the grid":
                        #grid_string = "no box matches the grid"
                        st.write("Please adjust the parameters or take a new picture")
                    else:
                        st.session_state["submitted"] = True
                        def find_color_ix(color_name):
                            return color_names.index(color_name)

                        st.session_state["largest_box"] = \
                            st.session_state["largest_box"][find_color_ix(checkbox_val)]
                        st.experimental_rerun()
                        #sb_content.empty()
                        #main_container.empty()
            cols =  sb_container.columns(3, )
            with cols[0]:
                grid_x = sb_container.number_input('x grid',
                                             min_value=1, max_value=50,
                                             value=20, step=1, key="x_grid",
                                             help="number of columns in the grid",
                                           label_visibility="visible")
            with cols[2]:
                grid_y = sb_container.number_input("y grid",
                                             min_value=1, max_value=50,
                                             value=20, step=1, key="y_grid",
                                             help="number of columns in the grid",
                                           label_visibility="visible")
            st.session_state["grid_x"] = grid_x
            st.session_state["grid_y"] = grid_y

        if not submitted or checkbox_val == "no box matches the grid":
            if show_threshold_img:
                col1, thr_col, col2 = main_container.columns(3)
            else:
                col1, col2 = main_container.columns(2)

            img = read_loaded_img(uploaded_file)
            st.session_state["img"] = img
            st.session_state["img_file_name"] = uploaded_file.name
            with col1:
                st.image(img, caption='Uploaded Image.', use_column_width=True, )

            threshold_img = prepare_img_for_boundary(img, False,
                                                     blurry_kernel_size,
                                                     adaptive_threshold_mode,
                                                     dilate_kernel_size,
                                                     dilate_iterations)

            if show_threshold_img:
                with thr_col:
                    st.image(threshold_img, caption='Threshold Image.',
                             use_column_width=True, )

            largest_boxes = find_largest_box(threshold_img, return_first_n_boxes=3)
            st.session_state["largest_box"] = largest_boxes
            # in col2 show the image img with the largest box drawn
            img2 = img.copy()

            for ix, box in enumerate(largest_boxes):
                # print(ix, box)
                cv2.drawContours(img2, [box], 0, box_colors[ix], 15)

            with col2:
                st.image(img2, caption='Largest box.', use_column_width=True)



if ("submitted" not in st.session_state) or \
        (not st.session_state["submitted"]):
   starting_page()
else:
    second_page()
