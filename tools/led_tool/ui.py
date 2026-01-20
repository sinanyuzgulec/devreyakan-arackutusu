from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QLabel, QGroupBox, QMessageBox)
from .logic import calculate_led
from core.localization import loc

class LedWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        form = QFormLayout()
        self.inputs = {}
        
        
        self.inputs['vs'] = QLineEdit()
        self.inputs['vs'].setPlaceholderText(loc.get("led_tool_voltage_supply_placeholder"))
        form.addRow(loc.get("led_tool_voltage_supply"), self.inputs['vs'])
        
        self.inputs['vl'] = QLineEdit()
        self.inputs['vl'].setPlaceholderText(loc.get("led_tool_voltage_led_placeholder"))
        form.addRow(loc.get("led_tool_voltage_led"), self.inputs['vl'])
        
        self.inputs['il'] = QLineEdit()
        self.inputs['il'].setPlaceholderText(loc.get("led_tool_current_led_placeholder"))
        form.addRow(loc.get("led_tool_current_led"), self.inputs['il'])
        
        self.inputs['n'] = QLineEdit("1")
        form.addRow(loc.get("led_tool_number_leds"), self.inputs['n'])
        
        grp = QGroupBox(loc.get("led_tool_parameters_group"))
        grp.setLayout(form)
        layout.addWidget(grp)
        
        
        btn = QPushButton(loc.get("led_tool_calculate_button"))
        btn.setStyleSheet("background-color: #22b28b; color: white; font-weight: bold; padding: 10px;")
        btn.clicked.connect(self.calculate)
        layout.addWidget(btn)
        
        
        self.lbl_result = QLabel(loc.get("led_tool_result_placeholder"))
        self.lbl_result.setStyleSheet("font-size: 14px; margin-top: 10px;")
        layout.addWidget(self.lbl_result)
        
        layout.addStretch()
        self.setLayout(layout)
        
    def calculate(self):
        try:
            vs = float(self.inputs['vs'].text().replace(',', '.'))
            vl = float(self.inputs['vl'].text().replace(',', '.'))
            il_ma = float(self.inputs['il'].text().replace(',', '.'))
            n = int(self.inputs['n'].text())
            
            
            il_amp = il_ma / 1000.0
            
            res = calculate_led(vs, vl, il_amp, n)
            
            if res:
                result_text = loc.get("led_tool_result_success").format(
                    ohm=f"{res.resistor_ohm:.2f}",
                    power=f"{res.resistor_power:.4f}"
                )

                self.lbl_result.setText(result_text)
                self.lbl_result.setStyleSheet("color: #22b28b; font-weight: bold;")
            else:
                
                self.lbl_result.setText(loc.get("led_tool_error_voltage"))
                self.lbl_result.setStyleSheet("color: red;")
                
        except ValueError:
            self.lbl_result.setText(loc.get("led_tool_error"))