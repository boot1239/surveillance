import random

import glob
import os

import cv2
import numpy as np
from PIL import Image

from config import ROOT_DIR

image = Image.open(ROOT_DIR + '/website/static/map.png')
WIDTH, HEIGHT = image.size


def render_image(citizens):
    files = glob.glob(ROOT_DIR + '/website/static/temp/*')
    for f in files:
        os.remove(f)

    map_name = f'map{random.randint(10_000, 99_999)}'
    img = np.array(image)

    circle_color = [176, 0, 0, 255]
    circle_width = 8
    for citizen in citizens:
        if not citizen.position:
            citizen.position = sector_to_coordinate(citizen.sector)
        cv2.circle(
            img,
            tuple(citizen.position),
            circle_width,
            circle_color,
            -1
        )

    new_image = Image.fromarray(img)
    new_image.save(ROOT_DIR + f'/website/static/temp/{map_name}.png')
    return map_name


def sector_to_coordinate(sector):
    if sector == 'A':
        coordinate = (
            random.randint(10, WIDTH // 2),
            random.randint(10, HEIGHT // 2),
        )
    elif sector == 'B':
        coordinate = (
            random.randint(WIDTH // 2, WIDTH - 10),
            random.randint(10, HEIGHT // 2),
        )
    elif sector == 'C':
        coordinate = (
            random.randint(10, WIDTH // 2),
            random.randint(HEIGHT // 2, HEIGHT - 10),
        )
    else:
        coordinate = (
            random.randint(WIDTH // 2, WIDTH - 10),
            random.randint(HEIGHT // 2, HEIGHT - 10),
        )
    return coordinate
