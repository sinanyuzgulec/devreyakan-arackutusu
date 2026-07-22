from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QLabel, QComboBox, QTextEdit
)
from .logic import calculate_crc
from core.localization import loc

class CrcWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        form = QFormLayout()
        
        self.inputs = {}
        self.inputs['data'] = QTextEdit()
        self.inputs['data'].setPlaceholderText("Örn: 123456789 veya HEX formatında: 31 32 33")
        self.inputs['data'].setMaximumHeight(100)
        
        self.inputs['input_type'] = QComboBox()
        self.inputs['input_type'].addItem(loc.get("checksumtoolwidget_ascii_input"), "ASCII")
        self.inputs['input_type'].addItem(loc.get("checksumtoolwidget_hex_input"), "HEX")
        
        self.inputs['algo'] = QComboBox()
        algos = ["CRC-8", "CRC-16-MODBUS", "CRC-16-CCITT-FALSE", "CRC-32"]
        self.inputs['algo'].addItems(algos)
        
        form.addRow(loc.get("crcwidget_input_data"), self.inputs['data'])
        form.addRow(loc.get("crcwidget_input_type"), self.inputs['input_type'])
        form.addRow(loc.get("crcwidget_algorithm"), self.inputs['algo'])
        
        btn = QPushButton(loc.get("crcwidget_calculate_button"))
        btn.clicked.connect(self.calculate)
        
        self.lbl_res = QLabel(loc.get("crcwidget_result_label"))
        self.lbl_res.setStyleSheet("font-family: Monospace; font-size: 14px; font-weight: bold;")
        
        layout.addLayout(form)
        layout.addWidget(btn)
        layout.addWidget(self.lbl_res)
        layout.addStretch()
        self.setLayout(layout)
        
    def calculate(self):
        text = self.inputs['data'].toPlainText().strip()
        in_type = self.inputs['input_type'].currentData()
        algo = self.inputs['algo'].currentText()
        
        if not text:
            self.lbl_res.setText(loc.get("crcwidget_error_empty"))
            return
            
        data_bytes = bytearray()
        if in_type == "ASCII":
            data_bytes = text.encode('utf-8')
        else:
            # Hex parsing
            try:
                hex_clean = text.replace("0x", "").replace(" ", "").replace("\n", "").replace(",", "")
                data_bytes = bytes.fromhex(hex_clean)
            except ValueError:
                self.lbl_res.setText(loc.get("crcwidget_error_hex"))
                return
                
        res = calculate_crc(data_bytes, algo)
        if res:
            self.lbl_res.setText(
                f"HEX: {res.hex_val}\n"
                f"DEC: {res.dec_val}\n"
                f"BIN: {res.bin_val}"
            )
