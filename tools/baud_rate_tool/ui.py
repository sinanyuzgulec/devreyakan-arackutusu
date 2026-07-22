from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QLabel, QComboBox
)
from .logic import calculate_baud_rate_error
from core.localization import loc

class BaudRateWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        form = QFormLayout()
        
        self.inputs = {}
        self.inputs['clock'] = QLineEdit("16000000") # 16 MHz
        
        self.inputs['target_baud'] = QComboBox()
        standard_bauds = ["9600", "19200", "38400", "57600", "115200", "230400", "460800", "921600"]
        self.inputs['target_baud'].addItems(standard_bauds)
        self.inputs['target_baud'].setEditable(True)
        self.inputs['target_baud'].setCurrentText("115200")
        
        self.inputs['oversampling'] = QComboBox()
        self.inputs['oversampling'].addItem("16x (Standart)", 16)
        self.inputs['oversampling'].addItem("8x (Yüksek Hız)", 8)
        
        form.addRow(loc.get("baudwidget_clock_freq"), self.inputs['clock'])
        form.addRow(loc.get("baudwidget_target_baud"), self.inputs['target_baud'])
        form.addRow(loc.get("baudwidget_oversampling"), self.inputs['oversampling'])
        
        btn = QPushButton(loc.get("baudwidget_calculate_button"))
        btn.clicked.connect(self.calculate)
        
        self.lbl_res = QLabel(loc.get("baudwidget_result_label"))
        self.lbl_res.setStyleSheet("font-family: Monospace;")
        
        layout.addLayout(form)
        layout.addWidget(btn)
        layout.addWidget(self.lbl_res)
        layout.addStretch()
        self.setLayout(layout)
        
    def calculate(self):
        try:
            clock = float(self.inputs['clock'].text().replace(',', '.'))
            target_baud = float(self.inputs['target_baud'].currentText().replace(',', '.'))
            oversampling = self.inputs['oversampling'].currentData()
            
            res = calculate_baud_rate_error(clock, target_baud, oversampling)
            if res:
                error_color = "red" if abs(res.error_percent) > 2.5 else "green"
                txt = (
                    f"{loc.get('baudwidget_actual_baud')} {res.actual_baud:.2f} Baud\n"
                    f"{loc.get('baudwidget_ubrr_divider')} {res.divider_ubrr}\n"
                    f"{loc.get('baudwidget_error_percent')} <span style='color:{error_color}; font-weight:bold;'>{res.error_percent:+.2f}%</span>\n"
                    f"{loc.get('baudwidget_status')} {res.status_message}"
                )
                self.lbl_res.setText(txt)
        except ValueError:
            self.lbl_res.setText(loc.get("baudwidget_input_error"))
