import time
import serial
from threading import Thread

class ComToCom:

    def __init__(self, rx_com: serial.Serial, tx_com: serial.Serial):
        self._rx = None
        self._tx = None
        self._sleep = 0.01
        self._transmit = True
        self._rx_com = rx_com
        self._tx_com = tx_com
        self._encoding = "ascii"
        self._read_thread = Thread(target=self._read)
        self._write_thread = Thread(target=self._write)

    @property
    def rx(self):
        return self._rx

    def set_tx(self, tx: str):
        self._tx = bytes(tx, self._encoding)

    def _read(self):
        while self._transmit:
            rx = self._rx_com.read().decode(self._encoding)
            if self._transmit:
                self._rx = rx
        
    def _write(self):
        while self._transmit:
            if self._tx:
                self._tx_com.write(self._tx)
            time.sleep(self._sleep)

    def wait_for_rx(self, rx: str, seconds: int = 1):
        for _ in range(seconds*100):
            if self._rx == rx:
                break
            time.sleep(self._sleep)
        
    def start(self):
        self._read_thread.start()
        self._write_thread.start()

    def stop(self):
        self._transmit = False
        self._tx_com.write(b"\n")
        self._read_thread.join()
        self._write_thread.join()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args):
        self.stop()

