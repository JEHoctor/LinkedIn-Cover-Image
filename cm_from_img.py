from pathlib import Path

from matplotlib.colors import ListedColormap
import numpy as np


here = Path(__file__).parent
sample_image_path = here / 'BBC_image_nuclear_lighthouse.jpg'


def cm_from_img(img_path=None):
    if img_path is None:
        img_path = str(sample_image_path)

    img = Image.open(img_path)
