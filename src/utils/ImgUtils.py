import numpy as np
from numpy import array
from PIL import Image


class ImgUtils(object):

    @staticmethod
    def read_image_bytes(filename):
        with open(filename, mode='rb') as file:
            return file.read()

    @staticmethod
    def read_image_numpy(filename, w, h):
        img = Image.open(filename).resize((w, h))
        img = img.convert('RGB')
        return array(img)

    @staticmethod
    def scale(arr):
        return arr / 255.0

    @staticmethod
    def mosaic_images(images_tensor, ncols, grayscale=False):
        img_size = images_tensor.shape[1]
        col_size = ncols * (img_size + 1) - 1
        nrows = int(np.ceil(images_tensor.shape[0] / ncols))
        row_size = nrows * (img_size + 1) - 1

        if grayscale:
            final = np.ones((row_size, col_size))
        else:
            final = np.ones((row_size, col_size, 3))

        for i in range(images_tensor.shape[0]):
            row = int(np.floor(i / ncols))
            col = i % ncols
            kernel = images_tensor[i]
            x = col * (img_size + 1)
            y = row * (img_size + 1)
            final[y:y + img_size, x:x + img_size] = kernel
        return final
