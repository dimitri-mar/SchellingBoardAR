""" A stramlit app that displays the loaded picture and the result of the
 grid detection """
import streamlit as st
import cv2
import numpy as np

from VisualDetector.Img2Game import parse_grid_string
from VisualDetector.ImagePreprocessing import prepare_img_for_boundary, \
    find_largest_box

@st.cache
def read_loaded_img(uploaded_file):
    return cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), 1)

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

submitted = None



with st.sidebar:
    uploaded_file = st.file_uploader("Choose a file")




# load the uploaded image into opencv
if uploaded_file is not None:
    with st.sidebar:
        show_threshold_img = st.checkbox('Threshold_img', value=False)
        with st.expander("adjust preprocessing parameters"):
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
        with st.form("grid_selection_form"):
            checkbox_val = st.radio(
                "Select the box that contains only the grid:",
                key="visibility",
                options=["no box matches the grid", "green", "red", "blue"],
            )
            # Every form must have a submit button.
            submitted = st.form_submit_button("Submit")
            if submitted:
                if checkbox_val == "no box matches the grid":
                    #grid_string = "no box matches the grid"
                    st.write("Please adjust the parameters or take a new picture")
                else:
                    placeholder = st.empty( )

    if show_threshold_img:
        col1, thr_col, col2 = st.columns(3)
    else:
        col1, col2 = st.columns(2)

    img = read_loaded_img(uploaded_file)
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
    # in col2 show the image img with the largest box drawn
    img2 = img.copy()

    box_colors = [(0, 255, 0), (0, 0, 255), (255, 0, 0)]
    print(len(box_colors))
    print(len(largest_boxes))
    for ix, box in enumerate(largest_boxes):
        print(ix, box)
        cv2.drawContours(img2, [box], 0, box_colors[ix], 15)

    with col2:
        st.image(img2, caption='Largest box.', use_column_width=True)


