
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QLabel, QGroupBox)
from PyQt6.QtCore import Qt
from .logic import calc_air_core
from core.localization import loc

class CoilWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        grp = QGroupBox(loc.get("coil_tool_wheeler_formula"))
        form = QFormLayout()
        
        self.inp_d = QLineEdit("10")
        self.inp_l = QLineEdit("20")
        self.inp_n = QLineEdit("15")
        
        form.addRow(loc.get("coil_tool_diameter"), self.inp_d)
        form.addRow(loc.get("coil_tool_length"), self.inp_l)
        form.addRow(loc.get("coil_tool_turns"), self.inp_n)
        
        grp.setLayout(form)
        layout.addWidget(grp)
        
        btn = QPushButton(loc.get("coil_tool_calculate_button"))
        btn.setStyleSheet("background-color: #22b28b; color: white; font-weight: bold; height: 40px;")
        btn.clicked.connect(self.calculate)
        layout.addWidget(btn)
        
        self.lbl_res = QLabel("- µH")
        self.lbl_res.setStyleSheet("font-size: 32px; font-weight: bold; color: #E67E22;")
        self.lbl_res.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(QLabel(loc.get("coil_tool_enductance")))
        layout.addWidget(self.lbl_res)
        layout.addStretch()
        
        info = QLabel(loc.get("coil_tool_note"))
        info.setStyleSheet("color: gray; font-size: 11px;")
        layout.addWidget(info)
        
        self.setLayout(layout)

    def calculate(self):
        try:
            d = float(self.inp_d.text())
            l = float(self.inp_l.text())
            n = float(self.inp_n.text())
            
            uH = calc_air_core(d, l, n)
            self.lbl_res.setText(f"{uH:.3f} µH")
        except:
            self.lbl_res.setText(loc.get("coil_tool_invalid_input"))
