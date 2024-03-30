import time
import cv2
from cv2 import VideoCapture
import pytesseract
import numpy as np


class Camera:
    """
    This class is a wrapper around the OpenCV VideoCapture class
    """
    MAIN_IMAGE = 'main.png'
    TEST_IMAGE = 'test.png'

    def __init__(self, device: int = None) -> None:
        pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
        self._cap: VideoCapture = cv2.VideoCapture(device)
        self._device = device

    def set_focus(self, value: int):
        """ Set the focus of the camera"""
        self._cap.set(cv2.CAP_PROP_FOCUS, value)

    def set_brightness(self, value: int):
        """ Set the brightness of the camera"""
        self._cap.set(cv2.CAP_PROP_BRIGHTNESS, value)
    
    def set_auto_focus(self, value: int):
        """ Set the auto focus of the camera"""
        self._cap.set(cv2.CAP_PROP_AUTOFOCUS, value)
    
    def get_text(self):
        """ Examine the camera image for text """
        frame = None
        self.set_auto_focus(0)
        for _ in range(7):
            # Give time for camera to setup
            time.sleep(0.2)
            self.set_focus(130)
            self.set_brightness(0)
            _, frame = self._cap.read()
        
        # Grab specific region of interest
        roi = frame[292:363, 265:360]
        roi = cv2.resize(roi, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC)
        cv2.imwrite(Camera.MAIN_IMAGE, frame)
        cv2.imwrite(Camera.TEST_IMAGE, roi)
        img = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        stack = np.hstack((img, img, img))
        char = pytesseract.image_to_string(
            stack,
            config='--psm 10 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        )
        if len(char) > 1:
            char = char[0]
        return char


    def open(self):
        """ Open the camera"""
        if self._device is None:
            raise RuntimeError("No device")
        if not self._cap.isOpened():
            self._cap.open(index=self._device)
            if not self._cap.isOpened():
                raise RuntimeError("Unable to open webcam")

    def close(self):
        """ Close the camera"""
        self._cap.release()
        
    def __enter__(self):
        if not self._cap.isOpened():
            self.open()
        return self

    def __exit__(self, *args):
        self.close()

