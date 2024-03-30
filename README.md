# Triple Char Test

## Overview

This project demonstrates of testing a ascii character three times when transmitted over a serial connection.
The character will be sent from one serial device, CP210x UART Bridge, to another device and a Oscilloscope
will read the data and display the character and a camera looking at the Oscilloscope will also read the character.

The three test points are:

1. (T1) Scope reading over TCP/IP
2. (T2) Web cam OCR looking at the scope
3. (T3) The receiving serial device

```text
Char -> Serial Device->|<- Silicon Labs CP210x UART Bridge 
                       |
T1 <--- Scope Data <---|
            |          |
T2 <---- USB Cam OCR   |
                       |
T3 <- Serial Device----|<- Silicon Labs CP210x UART Bridge
```

## Hardware Used

* Rigol 1054z Oscilloscope
* 2 x Silicon Labs CP210x UART Bridge
* Logitech USB C Web Cam

## Packages Used

* opencv-python
* pyserial
* pytesseract
* pytest
* PyVISA
* PyVISA-py

## Configuration

The `tests/conftest.py` file looks for `$HOME/triplechartest.txt"` file. And in that file is a comma separated list of values.

For example:

```text
# Serial Device,Serial Device,Vide0 Device,Rigol Scope IP Address
/dev/ttyUSB0,/dev/ttyUSB0,4,127.0.0.1
```

## To Install and Run

```bash
$ git clone https://github.com/tgu-ltd/triplechartest
$ cd triplechartest
$ poetry install
$ poetry shell
$ pytest
```

## Captured Images

### Rigol Screen with Event Table

![Event Table](https://www.tgu-ltd.uk/img/tripple_char_test_rigol_event_table.png)

## Camera Character Capture

![Character Capture](https://www.tgu-ltd.uk/img/triplechartest_character_capture.png)

## Files Read and Written

Three files are written during the tests:

1. `main.png` is a image of the webcam
2. `test.png` is a captured region of the webcam image
3. `screen.png` is a screen shot loaded from the rigol scope

One file is read during the tests:

1. `rigol_setup.bin` is used to setup the rigol 1054z. This file can be generated using the `Rigol(ip=x.x.x.x)._read_setup()` after manually setting up the scope.
