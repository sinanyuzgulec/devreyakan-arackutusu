from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QLabel) 
from .logic import calculate_adc
from core.localization import loc

class AdcWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        form = QFormLayout()
        
        self.inputs = {}
        self.inputs['bit'] = QLineEdit("10")
        self.inputs['vref'] = QLineEdit("5.0")
        self.inputs['vin'] = QLineEdit()
        
        form.addRow(loc.get("adcwidget_bit_resolution"), self.inputs['bit'])
        form.addRow(loc.get("adcwidget_vref_voltage"), self.inputs['vref'])
        form.addRow(loc.get("adcwidget_input_voltage"), self.inputs['vin'])
        
        btn = QPushButton(loc.get("adcwidget_calculate_button"))
        btn.clicked.connect(self.calculate)
        
        self.lbl_res = QLabel(loc.get("adcwidget_result_label"))
        self.lbl_res.setStyleSheet("font-family: Monospace;") 
        
        layout.addLayout(form)
        layout.addWidget(btn)
        layout.addWidget(self.lbl_res)
        layout.addStretch()
        self.setLayout(layout)
        
    def calculate(self):
        try:
            bit = int(self.inputs['bit'].text())
            vref = float(self.inputs['vref'].text().replace(',', '.'))
            vin = float(self.inputs['vin'].text().replace(',', '.'))
            
            if vin > vref:
                self.lbl_res.setText(loc.get("adcwidget_vinvref_error"))
                return

            res = calculate_adc(bit, vref, vin)
            if res:
                
                txt = (
                    f"{loc.get('adcwidget_digital_value')} {res.digital_val}\n"
                    f"{loc.get('adcwidget_binary_output')} {res.binary_str}\n"
                    f"{loc.get('adcwidget_step_voltage')} {res.resolution_step*1000:.2f} mV"
                )
                self.lbl_res.setText(txt)
        except ValueError:
            self.lbl_res.setText(loc.get("adcwidget_input_error"))