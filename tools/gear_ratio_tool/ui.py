from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QLabel, QGroupBox, QSpinBox)
from .logic import calculate_gear_ratio
from core.localization import loc

class GearRatioWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        form = QFormLayout()
        self.inputs = {}
        
        # Input speed
        self.inputs['input_speed'] = QLineEdit()
        self.inputs['input_speed'].setPlaceholderText("Örn: 1000")
        form.addRow(loc.get("gear_input_speed"), self.inputs['input_speed'])
        
        # Input torque
        self.inputs['input_torque'] = QLineEdit()
        self.inputs['input_torque'].setPlaceholderText("Örn: 5")
        form.addRow(loc.get("gear_input_torque"), self.inputs['input_torque'])
        
        # Input gear teeth
        self.inputs['teeth_input'] = QSpinBox()
        self.inputs['teeth_input'].setMinimum(1)
        self.inputs['teeth_input'].setMaximum(500)
        self.inputs['teeth_input'].setValue(20)
        form.addRow(loc.get("gear_teeth_input"), self.inputs['teeth_input'])
        
        # Output gear teeth
        self.inputs['teeth_output'] = QSpinBox()
        self.inputs['teeth_output'].setMinimum(1)
        self.inputs['teeth_output'].setMaximum(500)
        self.inputs['teeth_output'].setValue(40)
        form.addRow(loc.get("gear_teeth_output"), self.inputs['teeth_output'])
        
        # Efficiency
        self.inputs['efficiency'] = QLineEdit()
        self.inputs['efficiency'].setPlaceholderText("Örn: 95")
        form.addRow(loc.get("gear_efficiency"), self.inputs['efficiency'])
        
        grp = QGroupBox(loc.get("gear_input_speed"))
        grp.setLayout(form)
        layout.addWidget(grp)
        
        # Calculate button
        btn = QPushButton(loc.get("gear_calculate_button"))
        btn.setStyleSheet("background-color: #f59f00; color: white; font-weight: bold; padding: 10px;")
        btn.clicked.connect(self.calculate)
        layout.addWidget(btn)
        
        # Result label
        self.lbl_result = QLabel(loc.get("gear_result_placeholder"))
        self.lbl_result.setStyleSheet("font-size: 13px; margin-top: 10px; padding: 10px; background-color: #f8f9fa; border-radius: 5px;")
        self.lbl_result.setWordWrap(True)
        layout.addWidget(self.lbl_result)
        
        layout.addStretch()
        self.setLayout(layout)
        
    def calculate(self):
        try:
            input_speed = float(self.inputs['input_speed'].text().replace(',', '.'))
            input_torque = float(self.inputs['input_torque'].text().replace(',', '.'))
            teeth_input = int(self.inputs['teeth_input'].value())
            teeth_output = int(self.inputs['teeth_output'].value())
            efficiency = float(self.inputs['efficiency'].text().replace(',', '.'))
            
            result = calculate_gear_ratio(input_speed, input_torque, teeth_input, teeth_output, efficiency)
            
            if result:
                result_text = loc.get("gear_result_success").format(
                    ratio=result.gear_ratio,
                    speed=result.output_speed,
                    torque=result.output_torque,
                    loss=result.power_loss
                )
                self.lbl_result.setText(result_text)
                self.lbl_result.setStyleSheet("color: #f59f00; font-weight: bold; padding: 10px; background-color: #fff9e6; border-left: 4px solid #f59f00;")
            else:
                self.lbl_result.setText(loc.get("gear_error_invalid"))
                self.lbl_result.setStyleSheet("color: red; font-weight: bold; padding: 10px;")
                
        except ValueError:
            self.lbl_result.setText(loc.get("gear_error"))
            self.lbl_result.setStyleSheet("color: red; font-weight: bold; padding: 10px;")
