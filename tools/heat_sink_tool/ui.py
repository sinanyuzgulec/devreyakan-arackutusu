from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QLabel, QGroupBox)
from .logic import calculate_heat_sink
from core.localization import loc

class HeatSinkWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        form = QFormLayout()
        self.inputs = {}
        
        # Power dissipation
        self.inputs['power'] = QLineEdit()
        self.inputs['power'].setPlaceholderText("Örn: 10")
        form.addRow(loc.get("heat_sink_power_dissipation"), self.inputs['power'])
        
        # Ambient temperature
        self.inputs['ambient'] = QLineEdit()
        self.inputs['ambient'].setPlaceholderText("Örn: 25")
        form.addRow(loc.get("heat_sink_ambient_temp"), self.inputs['ambient'])
        
        # Maximum junction temperature
        self.inputs['max_junction'] = QLineEdit()
        self.inputs['max_junction'].setPlaceholderText("Örn: 150")
        form.addRow(loc.get("heat_sink_max_junction"), self.inputs['max_junction'])
        
        # Tj-Case thermal resistance
        self.inputs['tj_case'] = QLineEdit()
        self.inputs['tj_case'].setPlaceholderText("Örn: 0.5")
        form.addRow(loc.get("heat_sink_tj_case_resistance"), self.inputs['tj_case'])
        
        grp = QGroupBox(loc.get("heat_sink_power_dissipation"))
        grp.setLayout(form)
        layout.addWidget(grp)
        
        # Calculate button
        btn = QPushButton(loc.get("heat_sink_calculate_button"))
        btn.setStyleSheet("background-color: #ff6b6b; color: white; font-weight: bold; padding: 10px;")
        btn.clicked.connect(self.calculate)
        layout.addWidget(btn)
        
        # Result label
        self.lbl_result = QLabel(loc.get("heat_sink_result_placeholder"))
        self.lbl_result.setStyleSheet("font-size: 13px; margin-top: 10px; padding: 10px; background-color: #f8f9fa; border-radius: 5px;")
        self.lbl_result.setWordWrap(True)
        layout.addWidget(self.lbl_result)
        
        layout.addStretch()
        self.setLayout(layout)
        
    def calculate(self):
        try:
            power = float(self.inputs['power'].text().replace(',', '.'))
            ambient = float(self.inputs['ambient'].text().replace(',', '.'))
            max_junction = float(self.inputs['max_junction'].text().replace(',', '.'))
            tj_case = float(self.inputs['tj_case'].text().replace(',', '.'))
            
            result = calculate_heat_sink(power, ambient, max_junction, tj_case)
            
            if result:
                result_text = loc.get("heat_sink_result_success").format(
                    theta=result.required_theta,
                    tc=result.max_case_temp
                )
                self.lbl_result.setText(result_text)
                self.lbl_result.setStyleSheet("color: #22b28b; font-weight: bold; padding: 10px; background-color: #f0fdf4; border-left: 4px solid #22b28b;")
            else:
                self.lbl_result.setText(loc.get("heat_sink_error_invalid"))
                self.lbl_result.setStyleSheet("color: red; font-weight: bold; padding: 10px;")
                
        except ValueError:
            self.lbl_result.setText(loc.get("heat_sink_error"))
            self.lbl_result.setStyleSheet("color: red; font-weight: bold; padding: 10px;")
