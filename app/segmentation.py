from operator import imod
import cv2
import io
import numpy as np
from base64 import b64encode

color_image_flag = 1

class Segmentation:
    def __init__(self) -> None:
        self.input = None
        self.result = None
        self.in_memory_file = io.BytesIO()

    def set_input(self, img):
        self.input = img
        self.in_memory_file.flush()
        self.input.save(self.in_memory_file)

    def do_segmentation(self, part='all'):
        data = np.fromstring(self.in_memory_file.getvalue(), dtype=np.uint8)
        img = cv2.imdecode(data, color_image_flag)
        
        if part == 'all':
            self.result = cv2.rotate(img, cv2.ROTATE_180)
        elif part == 'nose':
            self.result = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        elif part == 'eyes':
            self.result = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            self.result = img

    def encode_result(self, file_ext):
        retval, buffer = cv2.imencode('.'+file_ext, self.result)
        return b64encode(buffer).decode('ascii')

    def do_segmentation_chain(self, img, part, file_ext):
        self.set_input(img=img)
        self.do_segmentation(part=part)
        return self.encode_result(file_ext=file_ext)