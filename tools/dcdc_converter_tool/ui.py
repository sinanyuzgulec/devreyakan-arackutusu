from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QLabel, QComboBox
)
from .logic import calculate_dcdc
from core.localization import loc

class DcDcConverterWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        form = QFormLayout()
        
        self.inputs = {}
        self.inputs['mode'] = QComboBox()
        self.inputs['mode'].addItem("Buck (Step-Down)", "Buck")
        self.inputs['mode'].addItem("Boost (Step-Up)", "Boost")
        
        self.inputs['vin'] = QLineEdit("12.0")
        self.inputs['vout'] = QLineEdit("5.0")
        self.inputs['iout'] = QLineEdit("2.0")
        self.inputs['fsw'] = QLineEdit("300000") # 300 kHz
        self.inputs['ripple'] = QLineEdit("30") # %30
        
        form.addRow(loc.get("dcdcwidget_mode"), self.inputs['mode'])
        form.addRow(loc.get("dcdcwidget_vin"), self.inputs['vin'])
        form.addRow(loc.get("dcdcwidget_vout"), self.inputs['vout'])
        form.addRow(loc.get("dcdcwidget_iout"), self.inputs['iout'])
        form.addRow(loc.get("dcdcwidget_fsw"), self.inputs['fsw'])
        form.addRow(loc.get("dcdcwidget_ripple"), self.inputs['ripple'])
        
        btn = QPushButton(loc.get("dcdcwidget_calculate_button"))
        btn.clicked.connect(self.calculate)
        
        self.lbl_res = QLabel(loc.get("dcdcwidget_result_label"))
        self.lbl_res.setStyleSheet("font-family: Monospace; font-size: 13px;")
        
        layout.addLayout(form)
        layout.addWidget(btn)
        layout.addWidget(self.lbl_res)
        layout.addStretch()
        self.setLayout(layout)
        
    def calculate(self):
        try:
            mode = self.inputs['mode'].currentData()
            vin = float(self.inputs['vin'].text().replace(',', '.'))
            vout = float(self.inputs['vout'].text().replace(',', '.'))
            iout = float(self.inputs['iout'].text().replace(',', '.'))
            fsw = float(self.inputs['fsw'].text().replace(',', '.'))
            ripple = float(self.inputs['ripple'].text().replace(',', '.'))
            
            res = calculate_dcdc(mode, vin, vout, iout, fsw, ripple)
            if res:
                txt = (
                    f"{loc.get('dcdcwidget_duty_cycle')} {res.duty_cycle * 100:.1f}%\n"
                    f"{loc.get('dcdcwidget_min_inductor')} {res.inductance_uh:.2f} µH\n"
                    f"{loc.get('dcdcwidget_peak_current')} {res.peak_current_a:.2f} A\n"
                    f"{loc.get('dcdcwidget_min_capacitor')} {res.min_capacitance_uf:.2f} µF"
                )
                self.lbl_res.setText(txt)
            else:
                self.lbl_res.setText(loc.get("dcdcwidget_error_invalid_voltages"))
        except ValueError:
            self.lbl_res.setText(loc.get("dcdcwidget_error_input"))
