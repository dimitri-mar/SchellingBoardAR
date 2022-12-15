import logging

import numpy as np
from loguru import logger

import tensorflow as tf
import keras_preprocessing
from keras_preprocessing import image

import cv2

from SchellingModel.SchellingGame import SchellingBoard

target_size = (75, 75)


def generate_cell_imgs(img_corrected, grid_x, grid_y):
    #cell_size = int(img_corrected.shape[1] / grid_x)
    cell_size = target_size[0]
    # assert cell_size == int(img_corrected.shape[0] / grid_y), \
    #    "cell size is not the same for x and y"

    target_width = grid_x * target_size[0]
    target_height = grid_y * target_size[1]

    if (img_corrected.shape[0], img_corrected.shape[1]) != (target_height, target_width):
        logger.info(f"resizing image to {(target_width, target_height)}")
        img_corrected = cv2.resize(img_corrected, (target_width, target_height))


    positions = []
    cells = []
    # TODO vectorize this
    for i in range(grid_x):
        for j in range(grid_y):
            cell = img_corrected[j * cell_size:(j + 1) * cell_size,
                   i * cell_size:(i + 1) * cell_size]
            assert cell.shape == (target_size[0], target_size[1], 3), \
                f"cell shape {cell.shape} is not {(target_size[0], target_size[1], 3)}"
            positions.append((i, j))
            cells.append(cell)

    import matplotlib.pylab as plt
    plt.figure(figsize=(10, 10))
    plt.imshow(cells[20])
    plt.savefig("test.png")
    #1print(f"cells shape: {cells.shape} and cells[20] shape: {cells[20].shape}")

    return positions, cells


def detect_labels(corrected_image,  grid_x, grid_y, model, return_label_img=False):
    labels = {'B_H': 0, 'B_S': 1, 'Empty': 2, 'R_H': 3, 'R_S': 4}
    int2label = {v: k for k, v in labels.items()}


    logger.info("loading model")
    model = tf.keras.models.load_model(model)

    logger.info("loading image")
    positions, cells = generate_cell_imgs(corrected_image, grid_x, grid_y)

    label_matrix = np.empty((grid_x, grid_y), dtype='|S3')

    # TODO: onepass
    for position, img in zip(positions, cells):
        #img = image.load_img(image_path, target_size=(75, 75))
        x = image.img_to_array(img, )
        x = x / 255
        x = x.reshape((1,) + x.shape)

        logger.info(f"predicting {(position[0], position[1])}")
        classes = model.predict(x)

        for key, value in labels.items():
            logger.info(f"{key}: {classes[0][value] :.2%}")

        most_probable_class = np.argmax(classes, axis=1)

        label_matrix[position[0], position[1]] = int2label[most_probable_class[0]]
        logger.info(f"predicted label for position {(position[0], position[1])}"
                    f"{int2label[most_probable_class[0]]}")

        #for key, value in labels.items():
        #    logger.info(f"{key}: {classes[0][value] :.2%}")

    if return_label_img:
        # annotate image with labels
        #img2 = cv2.cvtColor(corrected_image, cv2.COLOR_BGR2RGB)
        img2 = corrected_image.copy()

        dy = img2.shape[0] // grid_y
        dx = img2.shape[1] // grid_x
        for x_ix in range(grid_x):
            for y_ix in range(grid_y):
                x = x_ix * dx + dx * (0.3)
                y = y_ix * dy + dy * (0.7)

                cv2.putText(img2,
                            label_matrix[x_ix, y_ix].decode('ascii'),
                            (int(x), int(y)),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.1, (36, 255, 12), 4)
        #plt.figure(figsize=(26, 18))
        #plt.imshow(img2)

        return label_matrix, img2

    return label_matrix


def generate_cell_imgs_vect(img_corrected, grid_x, grid_y):
    #TODO Bug for rectangular images

    # cell_size = int(img_corrected.shape[1] / grid_x)
    cell_size = target_size[0]
    # assert cell_size == int(img_corrected.shape[0] / grid_y), \
    #    "cell size is not the same for x and y"

    target_width = grid_x * target_size[0]
    target_height = grid_y * target_size[1]

    if (img_corrected.shape[0], img_corrected.shape[1]) != \
            (target_height, target_width):
        logger.info(f"resizing image to {(target_width, target_height)}")
        img_corrected = cv2.resize(img_corrected,
                                   (target_width, target_height))

    #dataset = img_corrected.reshape(img_corrected.shape[1] // target_size[1],
    #                                target_size[1],
    #                                img_corrected.shape[0] // target_size[0],
    #                                target_size[0], img_corrected.shape[2])
    dataset = img_corrected.reshape(img_corrected.shape[0] // target_size[0],
                                    target_size[0],
                                    img_corrected.shape[1] // target_size[1],
                                    target_size[1], img_corrected.shape[2])
    dataset = dataset.swapaxes(1, 2)

    dataset = dataset.reshape(-1, target_size[0], target_size[1],
                              img_corrected.shape[2])

    logger.info(f"dataset shape: {dataset.shape}")

    return dataset


def decode_labels(label_matrix):
    labels = {'B_H': 0, 'B_S': 1, 'Emp': 2, 'R_H': 3, 'R_S': 4}
    int2label = {v: k for k, v in labels.items()}
    
    
    teams = np.zeros_like(label_matrix)
    blue_team = (label_matrix ==0) | (label_matrix ==1)
    red_team = (label_matrix == 3) | (label_matrix == 4)
    
    teams[blue_team] = 1
    teams[red_team] = 2
    
    moods = np.zeros_like(label_matrix)
    happy = (label_matrix == 0) | (label_matrix == 3)
    sad = (label_matrix == 1) | (label_matrix == 4)
    moods[happy] = 1
    moods[sad] = -1

    return teams, moods
    

def detect_labels_fast(corrected_image,  grid_x, grid_y, model ):
    # TODO Bug for rectangular images

    logger.info("loading model")
    model = tf.keras.models.load_model(model)

    logger.info("loading image")
    cells = generate_cell_imgs_vect(corrected_image, grid_x, grid_y)
    # import matplotlib.pylab as plt
    # plt.figure(figsize=(10, 10))
    # plt.imshow(cells[20])
    # plt.savefig("test.png")
    print(f"cells shape: {cells.shape} and cells[20] shape: {cells[20].shape}")

    logger.info(f"predicting all cells at once")

    x = cells / 255
    class_probabilities = model.predict(x)

    most_probable_classes = class_probabilities.argmax(axis=-1)#np.argmax(class_probabilities, axis=1)
    label_matrix = most_probable_classes.reshape((grid_y, grid_x))
    
    teams, moods = decode_labels(label_matrix)
    
    return SchellingBoard(teams, moods)



