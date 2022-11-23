import cv2
import numpy as np
import os
import click

from datetime import datetime
from loguru import logger

from VisualDetector.ImagePreprocessing import prepare_img_for_boundary, \
    find_largest_box, correct_perspective


def parse_grid_string(grid_string):
    """Parse grid string into a 2D array

    Args:
        grid_string: string of grid

    Returns:
        2D array of grid

    """

    # parse grid string
    grid = grid_string.split('x')
    grid = [int(i) for i in grid]
    assert len(grid) == 2, "Grid must be in format 'NxM'"
    assert grid[0] > 0 and grid[1] > 0, "Grid must be in format 'NxM'"

    return grid


def process_name_id():
    return f"img_{datetime.today().strftime('%Y%m%d%_H%M%S')}"


@click.group()
def control():
    """ manage the image processing pipeline """
    pass


@control.command()
@click.option('--img-path', '-i', type=click.Path(exists=True), required=True)
@click.option("--show", "-s", type=bool, is_flag=True)
@click.option("--grid", "-g", type=str, default="26x18", help=
"Grid size in format \n n_cell_horizontally x n_cell_vertically"
"default is 26x18")
@click.option('--output-dir', '-o', type=click.Path(exists=False),
              default=None)
@click.option('--process-name', '-n', type=str, default=process_name_id())
@click.option("--cell-size", "-c", type=int, default=None)
def data_preparation(img_path, show,
                     grid,
                     output_dir, process_name,
                     cell_size):
    grid_x, grid_y = parse_grid_string(grid)

    # load image
    img = cv2.imread(img_path)

    if output_dir is None:
        img_file_name = os.path.basename(img_path).replace(".", "_")
        output_dir = os.path.dirname(img_path)
        output_dir = os.path.join(output_dir, f"output_{img_file_name}")

    # create a directory in output_dir if it does not exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)  # create directory

    # setup the logger
    logger.add(f"{output_dir}/{process_name}.log", rotation="10 MB")
    logger.info(f"Process name: {process_name}")
    logger.info(f"Grid size: {grid_x}x{grid_y}")
    logger.info(f"Image size: {img.shape[1]}x{img.shape[0]}")
    logger.info(f"Image path: {img_path}")
    logger.info(f"Output directory: {output_dir}")

    # create a directory for the current process
    process_dir = os.path.join(output_dir, process_name)
    if not os.path.exists(process_dir):
        os.makedirs(process_dir)
        logger.info(f"Created directory {process_dir}")

    # save original image
    cv2.imwrite(os.path.join(process_dir, "original.png"), img)

    threshold_img = prepare_img_for_boundary(img, show)

    threshold_img_file_name = os.path.join(process_dir, "threshold.png")
    cv2.imwrite(threshold_img_file_name, threshold_img)
    logger.info(
        f"computed threshold image and saved to {threshold_img_file_name}")

    largest_box = find_largest_box(threshold_img)
    logger.info(f"Found largest box")

    # save the mask of the largest_box
    mask = np.zeros((img.shape), np.uint8)
    cv2.drawContours(mask, [largest_box], 0, 255, -1)
    cv2.drawContours(mask, [largest_box], 0, 0, 2)
    if show:
        cv2.imshow("mask", mask)
    cv2.imwrite(os.path.join(process_dir, "mask.png"), mask)

    img2 = img.copy()
    cv2.drawContours(img2, [largest_box], 0, (0, 255, 0), 3)
    if show:
        cv2.imshow("boundary", img2)
    cv2.imwrite(os.path.join(process_dir, "contour.png"), img2)

    # let's correct the perspective
    img_corrected = correct_perspective(img, largest_box, (grid_x, grid_y))
    if show:
        cv2.imshow("corrected", img_corrected)

    cv2.imwrite(os.path.join(process_dir, "corrected.png"), img_corrected)
    logger.info(
        f"Corrected perspective "
        f"and saved to {os.path.join(process_dir, 'corrected.png')}  \n"
        f"Image size: {img_corrected.shape}")

    # divede the image along the grid and save the different images
    if cell_size is None:
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
                os.path.join(cells_dir, f"cell_{i}_{j}.png"), cell)

    if show:
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == '__main__':
    control()
