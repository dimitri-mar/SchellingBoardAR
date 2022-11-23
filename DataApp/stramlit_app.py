""" A stramlit app that displays the loaded picture and the result of the
 grid detection """
import streamlit as st
import cv2
import numpy as np

from VisualDetector.Img2Game import parse_grid_string, correct_perspective, \
    prepare_img_for_boundary, find_largest_box

st.set_page_config(layout="wide")
uploaded_file = st.file_uploader("Choose a file")

# load the uploaded image into opencv
if uploaded_file is not None:
    col1, col2 = st.columns(2)
    img = cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), 1)
    with col1:
        st.image(img, caption='Uploaded Image.', use_column_width=True,)

    threshold_img = prepare_img_for_boundary(img, False)
    largest_box = find_largest_box(threshold_img)
    # in col2 show the image img with the largest box drawn
    img2 = img.copy()
    cv2.drawContours(img2, [largest_box], 0, (0, 255, 0), 3)
    with col2:
        st.image(img2, caption='Largest box.', use_column_width=True)





