
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QPushButton, QComboBox, QLabel)
from PyQt6.QtCore import Qt
from .logic import SerialWorker, get_serial_ports
from core.localization import loc

class SerialWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.worker = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        
        top_bar = QHBoxLayout()
        
        self.combo_ports = QComboBox()
        self.btn_refresh = QPushButton(loc.get("serial_tool_refresh"))
        self.btn_refresh.setFixedWidth(60)
        self.btn_refresh.clicked.connect(self.refresh_ports)
        
        self.combo_baud = QComboBox()
        self.combo_baud.addItems(["9600", "115200", "57600", "38400", "19200"])
        self.combo_baud.setCurrentText("9600")
        
        self.btn_connect = QPushButton(loc.get("serial_tool_connect"))
        self.btn_connect.setStyleSheet("background-color: #22b28b; color: white; font-weight: bold;")
        self.btn_connect.clicked.connect(self.toggle_connection)
        
        top_bar.addWidget(QLabel(loc.get("serial_tool_port")))
        top_bar.addWidget(self.combo_ports)
        top_bar.addWidget(self.btn_refresh)
        top_bar.addWidget(QLabel(loc.get("serial_tool_baudrate")))
        top_bar.addWidget(self.combo_baud)
        top_bar.addWidget(self.btn_connect)
        
        layout.addLayout(top_bar)
        
        
        self.txt_log = QTextEdit()
        self.txt_log.setReadOnly(True)
        self.txt_log.setStyleSheet("background-color: #1e1e1e; color: #00ff00; font-family: monospace;")
        layout.addWidget(self.txt_log)
        
        
        bottom_bar = QHBoxLayout()
        self.txt_input = QLineEdit()
        self.txt_input.setPlaceholderText(loc.get("serial_tool_input_placeholder"))
        self.txt_input.returnPressed.connect(self.send_data)
        
        btn_send = QPushButton(loc.get("serial_tool_send_button"))
        btn_send.clicked.connect(self.send_data)
        
        btn_clear = QPushButton(loc.get("serial_tool_clear_button"))
        btn_clear.clicked.connect(self.txt_log.clear)
        
        bottom_bar.addWidget(self.txt_input)
        bottom_bar.addWidget(btn_send)
        bottom_bar.addWidget(btn_clear)
        layout.addLayout(bottom_bar)
        
        self.setLayout(layout)
        self.refresh_ports()

    def refresh_ports(self):
        self.combo_ports.clear()
        ports_info = get_serial_ports() 
        
        if ports_info:
            for device, desc in ports_info:
                
                self.combo_ports.addItem(f"{device} ({desc})", device)
        else:
            self.combo_ports.addItem(loc.get("serial_tool_no_ports"))

    def toggle_connection(self):
        if self.worker is None:
            
            
            port = self.combo_ports.currentData()
            
            if not port:
                
                port = self.combo_ports.currentText().split(' ')[0]

            if loc.get("serial_tool_no_ports") in self.combo_ports.currentText() or not port:
                return

            baud = int(self.combo_baud.currentText())
            
            self.worker = SerialWorker(port, baud)
            self.worker.data_received.connect(self.update_log)
            self.worker.error_occurred.connect(self.handle_error)
            self.worker.start()
            
            self.btn_connect.setText(loc.get("serial_tool_disconnect_button"))
            self.btn_connect.setStyleSheet("background-color: #d9534f; color: white; font-weight: bold;")
            self.combo_ports.setEnabled(False)
            self.combo_baud.setEnabled(False)
            self.btn_refresh.setEnabled(False)
        else:
            
            self.worker.stop()
            self.worker = None
            
            self.btn_connect.setText(loc.get("serial_tool_connect_button"))
            self.btn_connect.setStyleSheet("background-color: #22b28b; color: white; font-weight: bold;")
            self.combo_ports.setEnabled(True)
            self.combo_baud.setEnabled(True)
            self.btn_refresh.setEnabled(True)

    def update_log(self, text):
        self.txt_log.append(text)
        sb = self.txt_log.verticalScrollBar()
        sb.setValue(sb.maximum())

    def handle_error(self, err_msg):
        
        log_text = loc.get("serial_tool_log_error").format(msg=str(err_msg))
        
        self.update_log(log_text)
        
        
        if self.worker:
            self.toggle_connection()

    def send_data(self):
        if self.worker and self.txt_input.text():
            data = self.txt_input.text()
            self.worker.send_data(data)
            self.update_log(f"> {data}")
            self.txt_input.clear()