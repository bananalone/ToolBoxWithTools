'''
    plugin template, implement setup and run method, this is entry point of tool box
'''
import os

import cv2
import numpy as np


class Plugin:
    def __init__(self) -> None:
        self.image_path = None
        self.save_path = None

    def setup(self):
        user_input = input("Enter path to image >>> ")
        if not os.path.isfile(user_input):
            raise Exception("{} is not a file".format(user_input))
        self.image_path = user_input
        user_input = input("Enter path to save as txt >>> ")
        if len(user_input) == 0:
            _substrs = self.image_path.split('.')
            _substrs[-1] = 'txt'
            self.save_path = '.'.join(_substrs)
        else:
            if os.path.exists(user_input):
                raise Exception("{} should not exist".format(user_input))
            self.save_path = user_input

    def _image2binary(self, image: np.ndarray):
        h, w = image.shape[0], image.shape[1]
        rw = 128
        rh = int((h * rw) / (w * 2))
        rimg = cv2.resize(image, (rw, rh))
        gimg = cv2.cvtColor(rimg, cv2.COLOR_BGR2GRAY)
        bimg = cv2.adaptiveThreshold(gimg, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 11)
        bimg[bimg == 255] = 1
        return bimg

    def run(self):
        '''
            run
        '''
        image = cv2.imread(self.image_path)
        binary = self._image2binary(image)
        ascii = np.array(binary, dtype=str)
        ascii[binary == 1] = '+'
        ascii[binary == 0] = '#'
        txt = ''
        for i in range(ascii.shape[0]):
            line = ''.join(ascii[i])
            txt += line + '\n'
        with open(self.save_path, 'w') as f:
            f.write(txt)
        print(txt)



if __name__ == '__main__':
    plugin = Plugin()
    plugin.setup()
    plugin.run()