
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QLineEdit, QComboBox, QLabel, QPushButton, QGroupBox)
from PyQt6.QtCore import Qt
from .logic import calculate_trace_width
from core.localization import loc

class PcbToolWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        grp = QGroupBox(loc.get("pcb_tool_groupbox"))
        form = QFormLayout()
        
        self.inputs = {}
        self.inputs['current'] = QLineEdit("1.0")
        self.inputs['temp'] = QLineEdit("10") 
        
        self.combo_oz = QComboBox()
        self.combo_oz.addItems(["0.5 oz (18µm)", "1.0 oz (35µm)", "2.0 oz (70µm)"])
        self.combo_oz.setCurrentIndex(1) 
        
        self.combo_layer = QComboBox()
        self.combo_layer.addItems([loc.get("pcb_tool_external"), loc.get("pcb_tool_internal")])
        
        form.addRow(loc.get("pcb_tool_current"), self.inputs['current'])
        form.addRow(loc.get("pcb_tool_temp_rise"), self.inputs['temp'])
        form.addRow(loc.get("pcb_tool_thickness"), self.combo_oz)
        form.addRow(loc.get("pcb_tool_layer"), self.combo_layer)
        
        grp.setLayout(form)
        layout.addWidget(grp)
        
        btn = QPushButton(loc.get("pcb_tool_calculate_button"))
        btn.setStyleSheet("background-color: #22b28b; color: white; font-weight: bold; height: 40px;")
        btn.clicked.connect(self.calculate)
        layout.addWidget(btn)
        
        
        self.lbl_res_mm = QLabel("- mm")
        self.lbl_res_mil = QLabel("- mil")
        
        self.lbl_res_mm.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")
        self.lbl_res_mil.setStyleSheet("font-size: 18px; color: #666;")
        
        res_layout = QVBoxLayout()
        res_layout.addWidget(QLabel(loc.get("pcb_tool_result_label")))
        res_layout.addWidget(self.lbl_res_mm)
        res_layout.addWidget(self.lbl_res_mil)
        res_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addLayout(res_layout)
        layout.addStretch()
        self.setLayout(layout)

    def calculate(self):
        try:
            amps = float(self.inputs['current'].text().replace(',', '.'))
            temp = float(self.inputs['temp'].text().replace(',', '.'))
            
            
            oz_text = self.combo_oz.currentText().split()[0]
            oz = float(oz_text)
            
            layer = "internal" if "Internal" in self.combo_layer.currentText() else "external"
            
            mil, mm = calculate_trace_width(amps, temp, oz, layer)
            
            self.lbl_res_mm.setText(f"{mm:.4f} mm")
            self.lbl_res_mil.setText(f"{mil:.2f} mil")
            
        except ValueError:
            self.lbl_res_mm.setText(loc.get("pcb_tool_error_invalid_input"))