
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QGridLayout, QCheckBox, QLineEdit, QLabel, QGroupBox, QHBoxLayout)
from PyQt6.QtCore import Qt
from .logic import update_val_from_bits, update_bits_from_val
from core.localization import loc

class StructBitToolWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.checkboxes = []
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        grid = QGridLayout()
        grid.setSpacing(5)

        for i in range(32):
            cb = QCheckBox()
            cb.setToolTip(f"Bit {i}")
            cb.stateChanged.connect(self.on_bit_change)
            self.checkboxes.append(cb)
            
            lbl = QLabel(str(i))
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setStyleSheet("font-size: 10px; color: gray;")
            
            row = 3 - (i // 8)
            col = 7 - (i % 8)
            
            vbox = QVBoxLayout()
            vbox.addWidget(lbl)
            vbox.addWidget(cb)
            vbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            container = QWidget()
            container.setLayout(vbox)
            if (i // 8) % 2 != 0: 
                container.setStyleSheet("background-color: #f0f0f0; border-radius: 4px;")
            
            grid.addWidget(container, row, col)

        grp_bits = QGroupBox(loc.get("structbittoolwidget_registermap"))
        grp_bits.setLayout(grid)
        layout.addWidget(grp_bits)
        
        io_layout = QHBoxLayout()
        
        self.txt_hex = QLineEdit("0x00000000")
        self.txt_hex.returnPressed.connect(self.on_hex_change)
        
        self.txt_dec = QLineEdit("0")
        self.txt_dec.returnPressed.connect(self.on_dec_change)
        
        self.txt_bin = QLineEdit()
        self.txt_bin.setReadOnly(True)
        self.txt_bin.setPlaceholderText("Binary")
        
        io_layout.addWidget(QLabel("HEX:"))
        io_layout.addWidget(self.txt_hex)
        io_layout.addWidget(QLabel("DEC:"))
        io_layout.addWidget(self.txt_dec)
        
        layout.addLayout(io_layout)
        layout.addWidget(QLabel("BIN:"))
        layout.addWidget(self.txt_bin)
        
        layout.addStretch()
        self.setLayout(layout)

    def on_bit_change(self):
        bits = [cb.isChecked() for cb in self.checkboxes]
        val = update_val_from_bits(bits)
        self.update_texts(val)

    def on_hex_change(self):
        try:
            text = self.txt_hex.text().replace('0x', '')
            val = int(text, 16)
            self.update_checkboxes(val)
            self.update_texts(val)
        except: pass

    def on_dec_change(self):
        try:
            val = int(self.txt_dec.text())
            self.update_checkboxes(val)
            self.update_texts(val)
        except: pass

    def update_checkboxes(self, val):
        bits = update_bits_from_val(val)
        for i, state in enumerate(bits):
            self.checkboxes[i].blockSignals(True)
            self.checkboxes[i].setChecked(state)
            self.checkboxes[i].blockSignals(False)

    def update_texts(self, val):
        self.txt_hex.blockSignals(True)
        self.txt_dec.blockSignals(True)
        
        self.txt_hex.setText(f"0x{val:08X}")
        self.txt_dec.setText(str(val))
        
        b_str = f"{val:032b}"
        fmt_bin = " ".join([b_str[i:i+4] for i in range(0, len(b_str), 4)])
        self.txt_bin.setText(fmt_bin)
        
        self.txt_hex.blockSignals(False)
        self.txt_dec.blockSignals(False)