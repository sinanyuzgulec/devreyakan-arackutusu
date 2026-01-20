
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QLabel, QGroupBox, QComboBox)
from PyQt6.QtCore import Qt
from .logic import calc_antenna
from core.localization import loc

class RfAntennaWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        grp = QGroupBox(loc.get("rf_antenna_tool_input_parameters"))
        form = QFormLayout()
        
        self.inp_freq = QLineEdit("145.500") 
        self.inp_k = QLineEdit("0.95") 
        
        form.addRow(loc.get("rf_antenna_tool_frequency"), self.inp_freq)
        form.addRow("Velocity Factor (k):", self.inp_k)
        
        grp.setLayout(form)
        layout.addWidget(grp)
        
        btn = QPushButton(loc.get("rf_antenna_tool_calculate_button"))
        btn.setStyleSheet("background-color: #22b28b; color: white; font-weight: bold; height: 40px;")
        btn.clicked.connect(self.calculate)
        layout.addWidget(btn)
        
        
        self.lbl_wave = QLabel("- m")
        self.lbl_dipole = QLabel("- cm")
        self.lbl_leg = QLabel("- cm")
        self.lbl_gp = QLabel("- cm")
        
        
        res_style = "font-size: 16px; font-weight: bold; color: #333;"
        self.lbl_dipole.setStyleSheet("font-size: 20px; font-weight: bold; color: blue;")
        
        res_layout = QFormLayout()
        res_layout.addRow(loc.get("rf_antenna_tool_full_wave_lenght"), self.lbl_wave)
        res_layout.addRow(loc.get("rf_antenna_tool_dipole_total_length"), self.lbl_dipole)
        res_layout.addRow(loc.get("rf_antenna_tool_dipole_leg_length"), self.lbl_leg)
        res_layout.addRow(loc.get("rf_antenna_tool_quarter_wave_length"), self.lbl_gp)
        
        layout.addLayout(res_layout)
        layout.addStretch()
        
        info = QLabel(loc.get("rf_antenna_tool_info"))
        info.setStyleSheet("color: gray; font-size: 11px;")
        layout.addWidget(info)
        
        self.setLayout(layout)

    def calculate(self):
        try:
            freq = float(self.inp_freq.text().replace(',', '.'))
            k = float(self.inp_k.text().replace(',', '.'))
            
            wl, dp, leg, gp = calc_antenna(freq, k)
            
            self.lbl_wave.setText(f"{wl:.4f} m")
            self.lbl_dipole.setText(f"{dp*100:.2f} cm")
            self.lbl_leg.setText(f"{leg*100:.2f} cm")
            self.lbl_gp.setText(f"{gp*100:.2f} cm")
        except:
            self.lbl_wave.setText(loc.get("rf_antenna_tool_invalid_input"))
