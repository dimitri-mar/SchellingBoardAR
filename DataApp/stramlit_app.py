""" A stramlit app that displays the loaded picture and the result of the
 grid detection """
import streamlit as st
import cv2
import numpy as np

from VisualDetector.Img2Game import parse_grid_string
from VisualDetector.ImagePreprocessing import prepare_img_for_boundary, \
    find_largest_box, correct_perspective
with st.sidebar:
    st.set_page_config(layout="wide")
    uploaded_file = st.file_uploader("Choose a file")
    show_threshold_img = st.checkbox('Threshold_img', value=False)


# load the uploaded image into opencv
if uploaded_file is not None:
    if show_threshold_img:
        col1, thr_col , col2 = st.columns(3)
    else:
        col1, col2 = st.columns(2)

    img = cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), 1)
    with col1:
        st.image(img, caption='Uploaded Image.', use_column_width=True,)

    threshold_img = prepare_img_for_boundary(img, False)
    if show_threshold_img:
        with thr_col:
            st.image(threshold_img, caption='Threshold Image.',
                     use_column_width=True,)


    largest_boxes = find_largest_box(threshold_img, return_first_n_boxes=3)
    # in col2 show the image img with the largest box drawn
    img2 = img.copy()

    box_colors = [(0, 255, 0), (0, 0, 255), (255, 0, 0)]
    print(len(box_colors))
    print(len(largest_boxes))
    for ix, box in enumerate(largest_boxes):
        print(ix, box)
        cv2.drawContours(img2, [box], 0, box_colors[ix], 3)

    with col2:
        st.image(img2, caption='Largest box.', use_column_width=True)






