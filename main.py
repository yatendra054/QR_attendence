import os
import cv2
from pyzbar.pyzbar import decode
import numpy as np

input_path = 'D:\\QR-Attendence\\Image qr\\images2.png'
output_path = 'D:\\QR-Attendence\\Image qr\\output_image1.jpeg'
if not os.path.exists(input_path):
    print(f"Error: File '{input_path}' does not exist.")
else:
    if not input_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
        print(f"Error: '{input_path}' is not a valid image file.")
    else:
        img = cv2.imread(input_path)

        if img is None:
            print(f"Error: Unable to load image '{input_path}'")
        else:
            qr_info = decode(img)

            if not qr_info:
                print("No QR codes detected in the image")
            else:
                for qr in qr_info:
                    data = qr.data.decode('utf-8')
                    rect = qr.rect
                    polygon = qr.polygon
                    img = cv2.rectangle(img, (rect.left, rect.top),
                                        (rect.left + rect.width, rect.top + rect.height),
                                        (0, 255, 0), 5)
                    img = cv2.polylines(img, [np.array(polygon)], True, (255, 0, 0), 5)

                cv2.imwrite(output_path, img)
                print(f"Image with highlighted QR code saved to '{output_path}'")
