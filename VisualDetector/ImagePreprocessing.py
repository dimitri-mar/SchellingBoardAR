import cv2
import numpy as np
from loguru import logger


def prepare_img_for_boundary(img, show=False):
    """Prepare image for boundary detection"""

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # plt.imshow(gray, cmap='gray')
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    # plt.imshow(blur, cmap='gray')
    thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 2)
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, \
                                   cv2.THRESH_BINARY, 11, 2)

    # remove small boundary discontinuities
    kernel = np.ones((3, 3), np.uint8)
    kernel = np.ones((4, 4), np.uint8)
    thresh2 = cv2.dilate(thresh, kernel, iterations=2)
    thresh2 = thresh

    if show:
        cv2.imshow('thresh2', thresh2)

    return thresh2


def find_largest_box(img):
    """Find largest box in image

        Args:
            img: better to be a threshold image
            show: show intermediate images
            img_origin: original image for drawing

        Returns:
              countour of largest box

        """
    logger.info("Finding largest box in image")
    contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)
    areas = [cv2.contourArea(i) for i in contours]

    # find the countour with the largest area
    # max_ctr = np.argmax(areas)

    sorted_ix = np.flip(np.argsort(areas))

    # find the rectangle with largest area (namely it has to have 4 edges)
    for ix, max_ctr in enumerate(sorted_ix):
        # approximate the contour with a polygon
        c = contours[max_ctr]
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.01 * peri, True)  # 0.02

        if len(approx) == 4:
            logger.info("Found largest box in image")
            return approx
        else:
            logger.warning(
                f"The {ix + 1}th largest contour is not a rectangle")

    logger.error("No box found in image")
    raise ValueError("No box found in image")


def correct_perspective(img, box, grid_size):
    """Correct perspective of image

    Args:
        img: original image
        box: box boundaries
        grid_size: size of grid

    Returns:
        corrected image

    """
    grid_x, grid_y = grid_size

    # lets identify the corners of the box
    sx_points = box[box[:, 0, 0].argsort()][:2]
    dx_points = box[box[:, 0, 0].argsort()][2:]
    sx_top_point, sx_bottom_point = sx_points[sx_points[:, 0, 1].argsort()]
    dx_top_point, dx_bottom_point = dx_points[dx_points[:, 0, 1].argsort()]

    # to find the min conveninet dimension to avoid deformation, I look for the minimum
    # difference between axies
    # if grid_size is None:
    min_y = np.min([np.abs(np.diff(sx_points[:, 0, 1])),
                    np.abs(np.diff(dx_points[:, 0, 1]))])

    dy = min_y - (min_y % grid_y)
    dx = dy / grid_y * grid_x
    # else:
    #    dy = grid_size * grid_y
    #    dx = grid_size * grid_x

    start_poly = np.array(
        [sx_top_point[0], dx_top_point[0], dx_bottom_point[0],
         sx_bottom_point[0]], np.float32)

    target_rectangular = np.array([[0, 0], [dx, 0], [dx, dy], [0, dy]],
                                  np.float32)

    M = cv2.getPerspectiveTransform(start_poly, target_rectangular)
    destination_size = (int(dx), int(dy))
    dst = cv2.warpPerspective(img, M, destination_size)
    logger.info(f"Corrected perspective of image to size {destination_size}")

    return dst
