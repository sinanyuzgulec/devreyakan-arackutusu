
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QLabel, QTabWidget, QGroupBox)
from PyQt6.QtCore import Qt
from .logic import calc_non_inverting, calc_inverting
from core.localization import loc

class OpAmpWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        tabs = QTabWidget()
        
        tabs.addTab(self.create_tab("non-inv"), loc.get("opamp_tool_non_inverting"))
        tabs.addTab(self.create_tab("inv"), loc.get("opamp_tool_inverting"))
        
        layout.addWidget(tabs)
        self.setLayout(layout)

    def create_tab(self, mode):
        w = QWidget()
        l = QVBoxLayout()
        form = QFormLayout()
        
        vin = QLineEdit("1.0")
        r1 = QLineEdit("1000")
        r2 = QLineEdit("10000")
        
        form.addRow(loc.get("opamp_tool_input_voltage"), vin)
        form.addRow(loc.get("opamp_tool_resistor_r1"), r1)
        form.addRow(loc.get("opamp_tool_resistor_r2"), r2)
        
        btn = QPushButton(loc.get("opamp_tool_calculate_button"))
        btn.clicked.connect(lambda: self.calc(mode, vin, r1, r2, lbl_res, lbl_gain))
        
        lbl_res = QLabel(loc.get("opamp_tool_output_voltage") + ": - V")
        lbl_gain = QLabel(loc.get("opamp_tool_result_label") + ": -")
        lbl_res.setStyleSheet("font-size: 20px; font-weight: bold; color: blue;")
        
        l.addLayout(form)
        l.addWidget(btn)
        l.addWidget(lbl_res)
        l.addWidget(lbl_gain)
        l.addStretch()
        w.setLayout(l)
        return w

    def calc(self, mode, vin_wdg, r1_wdg, r2_wdg, res_lbl, gain_lbl):
        try:
            vin = float(vin_wdg.text())
            r1 = float(r1_wdg.text())
            r2 = float(r2_wdg.text())
            
            if mode == "non-inv":
                vout, gain = calc_non_inverting(r1, r2, vin)
            else:
                vout, gain = calc_inverting(r1, r2, vin)
                
            res_lbl.setText(f"Vout: {vout:.2f} V")
            gain_lbl.setText(loc.get("opamp_tool_result_label") + f" {gain:.2f}")
        except:
            res_lbl.setText(loc.get("opamp_tool_error_invalid_input"))
