from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QLineEdit, QComboBox, QPushButton, QLabel, QGroupBox, QProgressBar)
from PyQt6.QtCore import Qt
from .logic import calculate_drop, AWG_TABLE
from core.localization import loc

class CableToolWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        grp = QGroupBox(loc.get("cabletoolwidget_dc_parameters"))
        form = QFormLayout()
        
        self.inputs = {}
        self.inputs['volts'] = QLineEdit("12.0")
        self.inputs['amps'] = QLineEdit("2.0")
        self.inputs['len'] = QLineEdit("10.0")
        
        self.combo_awg = QComboBox()
        self.combo_awg.addItems(AWG_TABLE.keys())
        self.combo_awg.setCurrentText("18 AWG (0.82 mm²)") 

        form.addRow(loc.get("cabletoolwidget_volts"), self.inputs['volts'])
        form.addRow(loc.get("cabletoolwidget_amps"), self.inputs['amps'])
        form.addRow(loc.get("cabletoolwidget_len"), self.inputs['len'])
        form.addRow(loc.get("cabletoolwidget_awg"), self.combo_awg)
        
        grp.setLayout(form)
        layout.addWidget(grp)
        
        btn = QPushButton(loc.get("cabletoolwidget_calculate_button"))
        btn.setStyleSheet("background-color: #22b28b; color: white; font-weight: bold; height: 40px;")
        btn.clicked.connect(self.calculate)
        layout.addWidget(btn)
        

        self.lbl_drop = QLabel(loc.get("cabletoolwidget_v_loss_short"))
        self.lbl_remain = QLabel(loc.get("cabletoolwidget_v_remain_short"))
        self.lbl_percent = QLabel(loc.get("cabletoolwidget_percent"))

        res_layout = QVBoxLayout()
        res_layout.addWidget(QLabel(loc.get("cabletoolwidget_v_loss")))
        res_layout.addWidget(self.lbl_drop)
        res_layout.addWidget(QLabel(loc.get("cabletoolwidget_v_remain")))
        res_layout.addWidget(self.lbl_remain)
        res_layout.addWidget(self.lbl_percent)
        
        self.prog_bar = QProgressBar()
        self.prog_bar.setRange(0, 100)
        self.prog_bar.setValue(0)
        self.prog_bar.setTextVisible(False)
        res_layout.addWidget(self.prog_bar)
        
        layout.addLayout(res_layout)
        layout.addStretch()
        self.setLayout(layout)

    def calculate(self):
        try:
            v = float(self.inputs['volts'].text().replace(',', '.'))
            i = float(self.inputs['amps'].text().replace(',', '.'))
            l = float(self.inputs['len'].text().replace(',', '.'))
            
            awg_key = self.combo_awg.currentText()
            area = AWG_TABLE[awg_key]
            
            drop, remain, percent = calculate_drop(v, i, l, area)
            
            self.lbl_drop.setText(f"{drop:.2f} V")
            self.lbl_remain.setText(f"{remain:.2f} V")
            self.lbl_percent.setText(f"%{percent:.1f}")
            
            val_int = min(int(percent), 100)
            self.prog_bar.setValue(val_int)
            
            if percent < 3.0:
                style = "QProgressBar::chunk { background-color: #5cb85c; }" 
                self.lbl_percent.setStyleSheet("color: green; font-weight: bold;")
            elif percent < 10.0:
                style = "QProgressBar::chunk { background-color: #f0ad4e; }" 
                self.lbl_percent.setStyleSheet("color: orange; font-weight: bold;")
            else:
                style = "QProgressBar::chunk { background-color: #d9534f; }" 
                self.lbl_percent.setStyleSheet("color: red; font-weight: bold;")
                
            self.prog_bar.setStyleSheet(style)
            
        except ValueError:
            self.lbl_drop.setText(loc.get("cabletoolwidget_error_invalid_input"))