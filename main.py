import os

import cv2
from pyzbar.pyzbar import decode
import numpy as np


input_dir = 'D:\Image qr'

for j in sorted(os.listdir(input_dir)):
    img = cv2.imread(os.path.join(input_dir, j))

    qr_info = decode(img)

    for qr in qr_info:

        data = qr.data
        rect = qr.rect
        polygon = qr.polygon


        img = cv2.rectangle(img, (rect.left, rect.top), (rect.left + rect.width, rect.top + rect.height),
                            (0, 255, 0), 5)

        img = cv2.polylines(img, [np.array(polygon)], True, (255, 0, 0), 5)

        cv2.imshow('QR Code', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


cv2.destroyAllWindows()