
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QLabel, QGroupBox)
from PyQt6.QtCore import Qt
from .logic import calculate_battery_life
from core.localization import loc

class BatteryToolWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        grp = QGroupBox(loc.get('batterytoolwidget_parameters_group'))
        form = QFormLayout()
        
        self.inputs = {}
        self.inputs['cap'] = QLineEdit("2500")
        self.inputs['sleep'] = QLineEdit("10")
        self.inputs['active'] = QLineEdit("80")
        self.inputs['dur'] = QLineEdit("5")
        self.inputs['int'] = QLineEdit("10")
        
        
        form.addRow(loc.get('batterytoolwidget_capacity_label'), self.inputs['cap'])
        form.addRow(loc.get('batterytoolwidget_sleep_current_label'), self.inputs['sleep'])
        form.addRow(loc.get('batterytoolwidget_active_current_label'), self.inputs['active'])
        form.addRow(loc.get('batterytoolwidget_active_duration_label'), self.inputs['dur'])
        form.addRow(loc.get('batterytoolwidget_wake_frequency_label'), self.inputs['int'])
        
        
        grp.setLayout(form)
        layout.addWidget(grp)
        
        btn = QPushButton(loc.get('batterytoolwidget_calculate_button'))
        btn.setStyleSheet("background-color: #22b28b; color: white; font-weight: bold; height: 40px;")
        btn.clicked.connect(self.calculate)
        layout.addWidget(btn)
        
        
        self.lbl_result = QLabel("-")
        self.lbl_result.setStyleSheet("font-size: 16px; font-weight: bold; color: #333; padding: 10px; border: 1px solid #ddd; background-color: #f9f9f9;")
        self.lbl_result.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_result.setWordWrap(True) 
        
        res_layout = QVBoxLayout()
        res_layout.addWidget(QLabel(loc.get('batterytoolwidget_result_label')))
        res_layout.addWidget(self.lbl_result)
        res_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addLayout(res_layout)
        
        layout.addWidget(QLabel(loc.get('batterytoolwidget_info_text')))
        
        self.setLayout(layout)

    def calculate(self):
        try:
            
            vals = [float(self.inputs[k].text().replace(',', '.')) for k in ['cap', 'sleep', 'active', 'dur', 'int']]
            
            
            y, m, d, h, mn = calculate_battery_life(*vals)
            
            
            parts = []
            if y > 0: parts.append(f"{y} {loc.get('batterytoolwidget_time_year')}")
            if m > 0: parts.append(f"{m} {loc.get('batterytoolwidget_time_month')}")
            if d > 0: parts.append(f"{d} {loc.get('batterytoolwidget_time_day')}")
            if h > 0: parts.append(f"{h} {loc.get('batterytoolwidget_time_hour')}")
            if mn > 0: parts.append(f"{mn} {loc.get('batterytoolwidget_time_min')}")
            
            if not parts:
                self.lbl_result.setText(loc.get('batterytoolwidget_result_instant'))
            else:
                
                final_text = ", ".join(parts)
                self.lbl_result.setText(final_text)
                self.lbl_result.setStyleSheet("font-size: 18px; font-weight: bold; color: #22b28b; padding: 10px; border: 2px solid #22b28b; background-color: #eafff5;")

        except ValueError:
            self.lbl_result.setText(loc.get('batterytoolwidget_error_invalid_input'))
            self.lbl_result.setStyleSheet("color: red;")