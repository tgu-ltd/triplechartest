import os
import time
import serial
import random
import string

from triplechartest.rigol import Rigol
from triplechartest.camera import Camera
from triplechartest.comtocom import ComToCom


def test_com_setup(com0: serial.Serial, com1: serial.Serial):
    rx_char = None
    tx_char = random.choice(string.ascii_uppercase)
    with ComToCom(tx_com=com0, rx_com=com1) as cc:
        cc.set_tx(tx_char)
        time.sleep(3)
        cc.wait_for_rx(rx=tx_char)
        rx_char = cc.rx
    assert rx_char== tx_char


def text_camera_setup(camera: Camera):
    camera.save()
    assert os.path.exists(Camera.OUTPUT)
    os.remove(Camera.OUTPUT)


def test_scope_setup(scope: Rigol):
    assert "RIGOL" in scope.query("*IDN?")
    scope.write_setup()
    assert True


def test_com_scope(com0: serial.Serial, com1: serial.Serial, scope: Rigol):
    rx_char = None
    tx_char = random.choice(string.ascii_uppercase)
    with ComToCom(tx_com=com0, rx_com=com1) as cc:
        cc.set_tx(tx_char)
        cc.wait_for_rx(rx=tx_char)
        scope.show_event_table()
        rx_char = scope.get_event_data()
        scope.get_screen_image()
        scope.hide_event_table()
    assert rx_char == tx_char


def test_com_camera(com0: serial.Serial, com1: serial.Serial, camera: Camera):
    """ Test the camera and com """
    rx_char = None
    tx_char = random.choice(string.ascii_uppercase)
    with ComToCom(tx_com=com0, rx_com=com1) as cc:
        cc.set_tx(tx_char)
        rx_char = camera.get_text()
        cc.wait_for_rx(rx=tx_char)
    assert rx_char == tx_char


def test_camera_accuracy(com0: serial.Serial, com1: serial.Serial, camera: Camera):
    """ Test the camera and com """
    hits = 0
    for _ in range(10):
        rx_char = None
        tx_char = random.choice(string.ascii_uppercase)
        with ComToCom(tx_com=com0, rx_com=com1) as cc:
            cc.set_tx(tx_char)
            rx_char = camera.get_text()
            cc.wait_for_rx(rx=tx_char)
            if rx_char == tx_char:
                hits += 1
    assert hits >= 5


def test_triplechartest(com0: serial.Serial, com1: serial.Serial, scope: Rigol, camera: Camera):
    """ The final triple char test """
    com_rx_char = None
    scope_rx_char = None
    camera_rx_char = None
    tx_char = random.choice(string.ascii_uppercase)
    with ComToCom(tx_com=com0, rx_com=com1) as cc:
        cc.set_tx(tx_char)
        camera_rx_char = camera.get_text()
        cc.wait_for_rx(rx=tx_char)
        scope_rx_char = scope.get_event_data()
        com_rx_char = cc.rx
    assert camera_rx_char == tx_char
    assert scope_rx_char == tx_char
    assert com_rx_char == tx_char