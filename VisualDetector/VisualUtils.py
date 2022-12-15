import cv2

def overlap_matrix_to_picture(img, overlap_matrix,
                              color=(36, 255, 12),
                              draw_cell=True,
                              thickness_text=4,
                              thickness_cell=2):
    """Draws the overlap matrix on the image.
    """
    img2 = img.copy()
    dy = img2.shape[0] // overlap_matrix.shape[0]
    dx = img2.shape[1] // overlap_matrix.shape[1]

    for y_ix in range(overlap_matrix.shape[0]):
        for x_ix in range(overlap_matrix.shape[1]):
            x = x_ix * dx + dx * (0.3)
            y = y_ix * dy + dy * (0.7)
            # import pdb ; pdb.set_trace()
            cv2.putText(img2,
                        overlap_matrix[y_ix, x_ix],
                        (int(x), int(y)),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.1, color, thickness_text)
            if draw_cell and overlap_matrix[y_ix, x_ix] != "":
                cv2.rectangle(img2, (x_ix * dx, y_ix * dy),
                                ((x_ix + 1) * dx, (y_ix + 1) * dy),
                                color, thickness_cell)
    return img2


def overlap_bool_matrix_to_picture(img, bool_matrix,
                                   color=(36, 255, 12),
                                   thickness=2):
    """
    Draw an X on the True entries of the bool_matrix.
    """
    img2 = img.copy()
    dy = img2.shape[0] // bool_matrix.shape[0]
    dx = img2.shape[1] // bool_matrix.shape[1]

    for y_ix in range(bool_matrix.shape[0]):
        for x_ix in range(bool_matrix.shape[1]):
            if bool_matrix[y_ix, x_ix]:
                # draw a rectangle around the cell
                cv2.rectangle(img2, (x_ix * dx, y_ix * dy),
                                ((x_ix + 1) * dx, (y_ix + 1) * dy),
                                color, thickness)
                # draw an X in the cell
                cv2.line(img2, (x_ix * dx, y_ix * dy),
                                ((x_ix + 1) * dx, (y_ix + 1) * dy),
                                color, thickness)
                cv2.line(img2, ((x_ix + 1) * dx, y_ix * dy),
                                (x_ix * dx, (y_ix + 1) * dy),
                                color, thickness)
    return img2


