from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QLabel, QComboBox
)
from .logic import convert_unit, CATEGORIES
from core.localization import loc

class UnitConverterWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        form = QFormLayout()
        
        self.inputs = {}
        self.inputs['val'] = QLineEdit("1.0")
        
        self.inputs['cat'] = QComboBox()
        self.inputs['cat'].addItems(list(CATEGORIES.keys()))
        self.inputs['cat'].currentTextChanged.connect(self.on_category_changed)
        
        self.inputs['from_unit'] = QComboBox()
        self.inputs['to_unit'] = QComboBox()
        
        form.addRow(loc.get("unitwidget_value"), self.inputs['val'])
        form.addRow(loc.get("unitwidget_category"), self.inputs['cat'])
        form.addRow(loc.get("unitwidget_from_unit"), self.inputs['from_unit'])
        form.addRow(loc.get("unitwidget_to_unit"), self.inputs['to_unit'])
        
        btn = QPushButton(loc.get("unitwidget_convert_button"))
        btn.clicked.connect(self.calculate)
        
        self.lbl_res = QLabel(loc.get("unitwidget_result_label"))
        self.lbl_res.setStyleSheet("font-family: Monospace; font-size: 14px; font-weight: bold;")
        
        layout.addLayout(form)
        layout.addWidget(btn)
        layout.addWidget(self.lbl_res)
        layout.addStretch()
        self.setLayout(layout)
        
        self.on_category_changed(self.inputs['cat'].currentText())
        
    def on_category_changed(self, cat_name):
        units = list(CATEGORIES.get(cat_name, {}).keys())
        self.inputs['from_unit'].clear()
        self.inputs['to_unit'].clear()
        self.inputs['from_unit'].addItems(units)
        self.inputs['to_unit'].addItems(units)
        if len(units) > 1:
            self.inputs['to_unit'].setCurrentIndex(1)
            
    def calculate(self):
        try:
            val = float(self.inputs['val'].text().replace(',', '.'))
            cat = self.inputs['cat'].currentText()
            u_from = self.inputs['from_unit'].currentText()
            u_to = self.inputs['to_unit'].currentText()
            
            res = convert_unit(val, cat, u_from, u_to)
            if res is not None:
                self.lbl_res.setText(f"{val} {u_from} = {res:.6g} {u_to}")
            else:
                self.lbl_res.setText(loc.get("unitwidget_error_invalid"))
        except ValueError:
            self.lbl_res.setText(loc.get("unitwidget_error_input"))
