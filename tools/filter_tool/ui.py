from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QLabel, QTabWidget, QComboBox)
from PyQt6.QtCore import Qt
from .logic import calc_cutoff_freq, calc_required_c
from core.localization import loc

class FilterToolWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        tabs = QTabWidget()
        
        tabs.addTab(self.create_freq_tab(), loc.get("rc_filter_tool_calculate_freq"))
        tabs.addTab(self.create_cap_tab(), loc.get("rc_filter_tool_find_cap"))
        
        layout.addWidget(tabs)
        self.setLayout(layout)

    def create_freq_tab(self):
        w = QWidget()
        l = QVBoxLayout()
        f = QFormLayout()
        
        self.inp_r = QLineEdit("1000") 
        self.inp_c = QLineEdit("0.1")  
        self.combo_c_unit = QComboBox()
        self.combo_c_unit.addItems(["uF", "nF", "pF"])
        self.combo_c_unit.setCurrentText("uF")
        
        f.addRow(loc.get("rc_filter_tool_resistance"), self.inp_r)
        f.addRow(loc.get("rc_filter_tool_capacitance"), self.inp_c)
        f.addRow(loc.get("rc_filter_tool_capacitance_unit"), self.combo_c_unit)
        
        btn = QPushButton(loc.get("rc_filter_tool_calculate_freq"))
        btn.clicked.connect(self.calc_freq)
        
        self.lbl_f_res = QLabel("- Hz")
        self.lbl_f_res.setStyleSheet("font-size: 24px; font-weight: bold; color: blue;")
        
        l.addLayout(f)
        l.addWidget(btn)
        l.addWidget(self.lbl_f_res)
        l.addStretch()
        w.setLayout(l)
        return w

    def create_cap_tab(self):
        w = QWidget()
        l = QVBoxLayout()
        f = QFormLayout()
        
        self.inp_req_r = QLineEdit("1000")
        self.inp_req_f = QLineEdit("1000") 
        
        f.addRow(loc.get("rc_filter_tool_fixed_resistance"), self.inp_req_r)
        f.addRow(loc.get("rc_filter_tool_frequency"), self.inp_req_f)
        
        btn = QPushButton(loc.get("rc_filter_tool_find_cap"))
        btn.clicked.connect(self.calc_cap)
        
        self.lbl_c_res = QLabel("-")
        self.lbl_c_res.setStyleSheet("font-size: 24px; font-weight: bold; color: green;")
        
        l.addLayout(f)
        l.addWidget(btn)
        l.addWidget(self.lbl_c_res)
        l.addStretch()
        w.setLayout(l)
        return w

    def get_c_multiplier(self, unit):
        if unit == "uF": return 1e-6
        if unit == "nF": return 1e-9
        if unit == "pF": return 1e-12
        return 1.0

    def calc_freq(self):
        try:
            r = float(self.inp_r.text())
            c_val = float(self.inp_c.text())
            mult = self.get_c_multiplier(self.combo_c_unit.currentText())
            
            freq = calc_cutoff_freq(r, c_val * mult)
            self.lbl_f_res.setText(f"{freq:.2f} Hz")
        except:
            self.lbl_f_res.setText(loc.get("rc_filter_tool_error"))

    def calc_cap(self):
        try:
            r = float(self.inp_req_r.text())
            f = float(self.inp_req_f.text())
            
            c_farad = calc_required_c(r, f)
            
            
            if c_farad < 1e-9:
                self.lbl_c_res.setText(f"{c_farad*1e12:.2f} pF")
            elif c_farad < 1e-6:
                self.lbl_c_res.setText(f"{c_farad*1e9:.2f} nF")
            else:
                self.lbl_c_res.setText(f"{c_farad*1e6:.2f} uF")
        except:
            self.lbl_c_res.setText(loc.get("rc_filter_tool_error"))