from typing import Iterator
import serial
import pytest
from pathlib import Path
from triplechartest.camera import Camera
from triplechartest.rigol import Rigol

@pytest.fixture(scope="module")
def envs():
    env = {"com0": "", "com1": "", "video": "", "scope": ""}
    filename = f"{Path.home()}/triplechartest.txt"
    with open(filename, "r") as f:
        lines = f.readlines()
        data = ''.join(lines).strip().split(",")
        env["com0"] = data[0]
        env["com1"] = data[1]
        env["video"] = int(data[2])
        env["scope"] = data[3]
    yield env

def get_com(port: str):
    return serial.Serial(port, timeout=1, write_timeout=1, baudrate=9600)


@pytest.fixture(scope="module")
def com0(envs) -> Iterator[serial.Serial]:
    com = get_com(envs["com0"])
    com.close()
    com.open()
    yield com
    com.close()


@pytest.fixture(scope="module")
def com1(envs) -> Iterator[serial.Serial]:
    com = get_com(envs["com1"])
    com.close()
    com.open()
    yield com
    com.close()


@pytest.fixture(scope="module")
def camera(envs) -> Iterator[Camera]:
    camera = Camera(envs["video"])
    camera.open()
    yield camera
    camera.close()


@pytest.fixture(scope="module")
def scope(envs) -> Iterator[Camera]:
    scope = Rigol(envs["scope"])
    scope.connect()
    yield scope
    scope.disconnect()