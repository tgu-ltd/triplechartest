import os
import time
import pyvisa


class Rigol:
    """ Rigol class to communicate with a 1054Z via SCPI """
    def __init__(self, ip: None) -> None:
        self._ip =  ip 
        self._setup_bin_file = "rigol_setup.bin"
        self._instrument: pyvisa.ResourceManager = None
        self._connected: bool = False
        self.screen_grab = 'screen.png'
        

    def connect(self) -> None:
        """ Connect to the scope """
        if not self._ip:
            raise RuntimeError("No IP")
        self._instrument = pyvisa.ResourceManager().open_resource(
            resource_name=f"TCPIP::{self._ip}::inst0::INSTR",
            write_termination='\n',
            read_termination='\n',
        )
        if not self._instrument.query("*IDN?"):
            self.disconnect()
            raise RuntimeError("No IDN")
        self._connected = True

    def _read_setup(self):
        with open(self._setup_bin_file, "wb") as f:
            binary = self._instrument.query_binary_values(":SYSTem:SETup?", datatype="B", container=bytes)
            f.write(binary)
        
    def write_setup(self):
        """ Write the setup to the scope"""
        binary = None
        if os.path.exists(self._setup_bin_file):
            with open(self._setup_bin_file, "rb") as f:
                binary = f.read()
            self._instrument.write_binary_values(":SYSTem:SETup", binary, datatype="B")
    
    def disconnect(self) -> None:
        """ Disconnect from the scope """
        if self._connected and self._instrument:
            self._instrument.close()
        self._connected = False

    def get_event_data(self):
        """ Get the event data """
        table = self.query(':ETABle1:DATA?').split('\n')
        if len(table) < 2:
            return ""
        data = table[2].split(',')
        if len(data) < 2:
            return ""
        return data[1]

    def show_event_table(self):
        self.write(':ETABle1:DISP 1')
        self.write('::ETABle1:FORMat ASCii')

    def hide_event_table(self):
        """ Hide the event table"""
        self.write(':ETABle1:DISP 0')

    def get_screen_image(self):
        """ Get the screen image """
        binary = self._instrument.query_binary_values(":DISP:DATA? ON,OFF,PNG", datatype="B", container=bytes)
        with open(self.screen_grab, 'wb') as f:
            f.write(bytearray(binary))

    def write(self, command: str) -> None:
        """ Write to the scope """
        self._instrument.write(command)
        time.sleep(0.05)

    def query(self, command: str) -> str:
        """ query the scope """
        return self._instrument.query(command)
