from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QLabel, QComboBox
)
from .logic import calculate_i2c_pullup
from core.localization import loc

class I2cPullupWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        form = QFormLayout()
        
        self.inputs = {}
        self.inputs['vdd'] = QLineEdit("3.3")
        self.inputs['bus_speed'] = QComboBox()
        self.inputs['bus_speed'].addItem("Standard-mode (100 kHz)", 100)
        self.inputs['bus_speed'].addItem("Fast-mode (400 kHz)", 400)
        self.inputs['bus_speed'].addItem("Fast-mode Plus (1 MHz)", 1000)
        
        self.inputs['bus_cap'] = QLineEdit("150") # 150 pF
        self.inputs['vol'] = QLineEdit("0.4")
        self.inputs['iol'] = QLineEdit("3.0") # 3 mA
        
        form.addRow(loc.get("i2cwidget_vdd"), self.inputs['vdd'])
        form.addRow(loc.get("i2cwidget_bus_speed"), self.inputs['bus_speed'])
        form.addRow(loc.get("i2cwidget_bus_cap"), self.inputs['bus_cap'])
        form.addRow(loc.get("i2cwidget_vol"), self.inputs['vol'])
        form.addRow(loc.get("i2cwidget_iol"), self.inputs['iol'])
        
        btn = QPushButton(loc.get("i2cwidget_calculate_button"))
        btn.clicked.connect(self.calculate)
        
        self.lbl_res = QLabel(loc.get("i2cwidget_result_label"))
        self.lbl_res.setStyleSheet("font-family: Monospace; font-size: 13px;")
        
        layout.addLayout(form)
        layout.addWidget(btn)
        layout.addWidget(self.lbl_res)
        layout.addStretch()
        self.setLayout(layout)
        
    def calculate(self):
        try:
            vdd = float(self.inputs['vdd'].text().replace(',', '.'))
            speed_khz = self.inputs['bus_speed'].currentData()
            bus_cap_pf = float(self.inputs['bus_cap'].text().replace(',', '.'))
            vol = float(self.inputs['vol'].text().replace(',', '.'))
            iol_ma = float(self.inputs['iol'].text().replace(',', '.'))
            
            res = calculate_i2c_pullup(vdd, speed_khz, bus_cap_pf, vol, iol_ma)
            if res:
                txt = (
                    f"{loc.get('i2cwidget_min_resistor')} {res.min_r_ohm:.0f} Ω ({res.min_r_ohm/1000:.2f} kΩ)\n"
                    f"{loc.get('i2cwidget_max_resistor')} {res.max_r_ohm:.0f} Ω ({res.max_r_ohm/1000:.2f} kΩ)\n"
                    f"{loc.get('i2cwidget_rec_resistor')} {res.recommended_r_ohm:.0f} Ω ({res.recommended_r_ohm/1000:.2f} kΩ)"
                )
                self.lbl_res.setText(txt)
            else:
                self.lbl_res.setText(loc.get("i2cwidget_error_invalid"))
        except ValueError:
            self.lbl_res.setText(loc.get("i2cwidget_error_input"))
