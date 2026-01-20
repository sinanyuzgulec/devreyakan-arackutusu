
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QLabel, QGroupBox)
from PyQt6.QtCore import Qt
from .logic import calculate_ntc_temp
from core.localization import loc

class NtcToolWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        grp = QGroupBox(loc.get("ntc_tool_parameters"))
        form = QFormLayout()
        
        self.inputs = {}
        self.inputs['r25'] = QLineEdit("10000") 
        self.inputs['beta'] = QLineEdit("3950") 
        self.inputs['meas'] = QLineEdit("10000") 
        
        form.addRow(loc.get("ntc_tool_resistance") + "  @ 25°C:", self.inputs['r25'])
        form.addRow(loc.get("ntc_tool_beta"), self.inputs['beta'])
        form.addRow(loc.get("ntc_tool_resistance"), self.inputs['meas'])
        
        grp.setLayout(form)
        layout.addWidget(grp)
        
        btn = QPushButton(loc.get("ntc_tool_calculate_button"))
        btn.setStyleSheet("background-color: #22b28b; color: white; font-weight: bold; height: 40px;")
        btn.clicked.connect(self.calculate)
        layout.addWidget(btn)
        
        self.lbl_res = QLabel("- °C")
        self.lbl_res.setStyleSheet("font-size: 32px; font-weight: bold; color: #d9534f;")
        self.lbl_res.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(QLabel(loc.get("ntc_tool_result_label")))
        layout.addWidget(self.lbl_res)
        layout.addStretch()
        self.setLayout(layout)

    def calculate(self):
        try:
            r25 = float(self.inputs['r25'].text())
            beta = float(self.inputs['beta'].text())
            meas = float(self.inputs['meas'].text())
            
            temp = calculate_ntc_temp(meas, beta, r25)
            
            if temp is not None:
                self.lbl_res.setText(f"{temp:.2f} °C")
            else:
                self.lbl_res.setText(loc.get("ntc_tool_calculation_error"))
        except:
            self.lbl_res.setText(loc.get("ntc_tool_input_error"))