
import serial
import serial.tools.list_ports
from PyQt6.QtCore import QThread, pyqtSignal
import core.localization as loc

class SerialWorker(QThread):
    
    data_received = pyqtSignal(str)
    error_occurred = pyqtSignal(str)

    def __init__(self, port, baudrate):
        super().__init__()
        self.port = port
        self.baudrate = baudrate
        self.is_running = True
        self.serial_conn = None

    def run(self):
        try:
            
            self.serial_conn = serial.Serial(self.port, self.baudrate, timeout=1)
            while self.is_running:
                if self.serial_conn.is_open and self.serial_conn.in_waiting:
                    try:
                        
                        line = self.serial_conn.readline().decode('utf-8', errors='ignore').strip()
                        if line:
                            self.data_received.emit(line)
                    except Exception as e:
                        self.error_occurred.emit(str(e))
                self.msleep(10) 

        except serial.SerialException as e:
            err_text = loc.get("serial_tool_connection_error").format(msg=str(e))
            self.error_occurred.emit(err_text)
        finally:
            if self.serial_conn and self.serial_conn.is_open:
                self.serial_conn.close()

    def stop(self):
        self.is_running = False
        self.wait()

    def send_data(self, data):
        if self.serial_conn and self.serial_conn.is_open:
            try:
                self.serial_conn.write((data + '\n').encode('utf-8'))
            except Exception as e:
                err_text = loc.get("serial_tool_send_error").format(msg=str(e))
                self.error_occurred.emit(err_text)

def get_serial_ports():

    ports = serial.tools.list_ports.comports()
    result = []
    for p in ports:
        
        
        desc = p.description
        
        
        if p.manufacturer and p.manufacturer not in desc:
            desc = f"{desc} ({p.manufacturer})"
            
        result.append((p.device, desc))
    return result