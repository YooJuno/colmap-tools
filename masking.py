import numpy as np
from PIL import Image

dataset_name = 'F1'
width, height = 2304, 1296

mask = np.zeros((height,width), dtype=np.uint8)
mask[93:950, : ] = 255 # RoI

mask_image = Image.fromarray(mask).save(dataset_name + '_mask.png')