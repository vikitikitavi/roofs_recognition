import os
import numpy as np
import matplotlib.image as mpimg
from PIL import Image
import random

DIRECTORY = 'C:\\Users\\tori\\Desktop\\Крыши'
LEARN = 'C:\\Users\\tori\\Desktop\\Крыши\\обучение'
TEST = 'C:\\Users\\tori\\Desktop\\Крыши\\тест'
ROUND = '\\круглая'
FLAT = '\\плоская'
TRIANGULAR = '\\треугольная'
SLASH = '\\'
DASH = '_'
PNG = '.png'
IMAGE_SIZE = 28

def create_new_set(roofs_shape, index):
    directory = DIRECTORY + roofs_shape
    # files = list(filter(lambda x: x.endswith(PNG), os.listdir(directory)))
    # angle = 90
    # for persent in range(int(len(files) * 0.8)):
    #     img = Image.open(directory + SLASH + files[persent]).convert('L')
    #     img = img.resize((IMAGE_SIZE, IMAGE_SIZE), Image.ANTIALIAS)
    #     for ind in range(0, 1):
    #         img = img.rotate(angle*ind)
    #         img.save(LEARN + SLASH + str(persent) + DASH + str(ind) + DASH + str(index) + PNG)
    #
    # for rest in range(persent + 1, len(files)):
    #     img = Image.open(directory + SLASH + files[rest]).convert('L')
    #     img = img.resize((IMAGE_SIZE, IMAGE_SIZE), Image.ANTIALIAS)
    #
    #     for ind in range(0, 1):
    #         img = img.rotate(angle*ind)
    #         img.save(TEST + SLASH + str(rest) + DASH + str(ind) + DASH + str(index) + PNG)

def array(index):
    arr = ([0., 0., 0.])
    arr[index] = 1.
    return arr

def create_roofs_arrays(folder):
    roof_images = list(filter(lambda x: x.endswith(PNG), os.listdir(folder)))
    image_array = []
    result_array = []
    random.shuffle(roof_images)
    for image_name in roof_images:
        img = mpimg.imread(folder + SLASH + image_name)
        image_array.append(np.array(img.ravel(), dtype=np.float32))

        result_array.append(int(image_name[-5]))
        image_array_converted = np.array(image_array, dtype=np.float32)
        result_array_converted = np.array(result_array, dtype=np.int32)
    return image_array_converted, result_array_converted


create_new_set(ROUND, 0)
create_new_set(FLAT, 1)
create_new_set(TRIANGULAR, 2)

im_1, result = create_roofs_arrays(LEARN)
print (im_1.shape)
print(result.shape)
print('b')


