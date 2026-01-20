
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QLabel, QTabWidget, QGroupBox)
from PyQt6.QtCore import Qt
from .logic import calc_lm317_voltage, calc_lm317_resistor, calc_power_dissipation
from core.localization import loc

class RegulatorWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        tabs = QTabWidget()
        
        tabs.addTab(self.create_calc_vout(), loc.get("regulator_tool_calc_output_voltage"))
        tabs.addTab(self.create_calc_r2(), loc.get("regulator_tool_calc_r2_value"))
        
        layout.addWidget(tabs)
        
        
        layout.addWidget(self.create_thermal_section())
        
        self.setLayout(layout)

    def create_calc_vout(self):
        w = QWidget()
        l = QVBoxLayout()
        f = QFormLayout()
        
        self.inp_v_r1 = QLineEdit("240") 
        self.inp_v_r2 = QLineEdit("1000")
        
        f.addRow(loc.get("regulator_tool_resistor_r1_general"), self.inp_v_r1)
        f.addRow(loc.get("regulator_tool_resistor_r2_fixed"), self.inp_v_r2)
        
        btn = QPushButton(loc.get("regulator_tool_calculate_output_voltage"))
        btn.clicked.connect(self.run_calc_vout)
        
        self.lbl_vout = QLabel("- V")
        self.lbl_vout.setStyleSheet("font-size: 24px; font-weight: bold; color: blue;")
        
        l.addLayout(f)
        l.addWidget(btn)
        l.addWidget(self.lbl_vout)
        l.addStretch()
        w.setLayout(l)
        return w

    def create_calc_r2(self):
        w = QWidget()
        l = QVBoxLayout()
        f = QFormLayout()
        
        self.inp_r_vout = QLineEdit("5.0")
        self.inp_r_r1 = QLineEdit("240")
        
        f.addRow(loc.get("regulator_tool_output_voltage"), self.inp_r_vout)
        f.addRow(loc.get("regulator_tool_resistor_r1"), self.inp_r_r1)
        
        btn = QPushButton(loc.get("regulator_tool_calculate_r2_2"))
        btn.clicked.connect(self.run_calc_r2)
        
        self.lbl_r2 = QLabel("- Ohm")
        self.lbl_r2.setStyleSheet("font-size: 24px; font-weight: bold; color: green;")
        
        l.addLayout(f)
        l.addWidget(btn)
        l.addWidget(self.lbl_r2)
        l.addStretch()
        w.setLayout(l)
        return w

    def create_thermal_section(self):
        grp = QGroupBox(loc.get("regulator_tool_thermal_dissipation"))
        l = QFormLayout()
        
        self.th_vin = QLineEdit("12.0")
        self.th_vout = QLineEdit("5.0")
        self.th_i = QLineEdit("0.5") 
        
        l.addRow(loc.get("regulator_tool_input_voltage"), self.th_vin)
        l.addRow(loc.get("regulator_tool_output_voltage"), self.th_vout)
        l.addRow(loc.get("regulator_tool_current_draw"), self.th_i)
        
        btn = QPushButton(loc.get("regulator_tool_calculate_power_dissipation"))
        btn.clicked.connect(self.run_thermal)
        
        self.lbl_watts = QLabel("- Watt")
        self.lbl_watts.setStyleSheet("font-size: 18px; font-weight: bold; color: #d9534f;")
        
        self.lbl_advice = QLabel("")
        self.lbl_advice.setStyleSheet("font-style: italic; color: #555;")
        
        w = QWidget()
        v = QVBoxLayout()
        v.addLayout(l)
        v.addWidget(btn)
        v.addWidget(self.lbl_watts)
        v.addWidget(self.lbl_advice)
        grp.setLayout(v)
        return grp

    def run_calc_vout(self):
        try:
            r1 = float(self.inp_v_r1.text())
            r2 = float(self.inp_v_r2.text())
            v = calc_lm317_voltage(r1, r2)
            self.lbl_vout.setText(f"{v:.2f} V")
            self.th_vout.setText(f"{v:.2f}") 
        except: self.lbl_vout.setText(loc.get("regulator_tool_error"))

    def run_calc_r2(self):
        try:
            vout = float(self.inp_r_vout.text())
            r1 = float(self.inp_r_r1.text())
            r2 = calc_lm317_resistor(vout, r1)
            self.lbl_r2.setText(f"{r2:.2f} Ω")
        except: self.lbl_r2.setText(loc.get("regulator_tool_error"))

    def run_thermal(self):
        try:
            vin = float(self.th_vin.text())
            vout = float(self.th_vout.text())
            i = float(self.th_i.text())
            
            watts = calc_power_dissipation(vin, vout, i)
            self.lbl_watts.setText(loc.get("regulator_tool_result_watt_heat").format(val=f"{watts:.2f}"))
            
            if watts < 0.25:
                self.lbl_advice.setText(loc.get("regulator_tool_no_heatsink_needed"))
            elif watts < 1.0:
                self.lbl_advice.setText(loc.get("regulator_tool_small_heatsink_advice"))
            else:
                self.lbl_advice.setText(loc.get("regulator_tool_large_heatsink_advice"))
        except: self.lbl_watts.setText(loc.get("regulator_tool_error"))
