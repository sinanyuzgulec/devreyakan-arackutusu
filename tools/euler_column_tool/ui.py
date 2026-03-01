from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QLabel, QGroupBox, QComboBox)
from .logic import calculate_euler_column, get_k_factor
from core.localization import loc

class EulerColumnWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        form = QFormLayout()
        self.inputs = {}
        
        # Modulus of elasticity
        self.inputs['modulus'] = QLineEdit()
        self.inputs['modulus'].setPlaceholderText("Örn: 200e9")
        form.addRow(loc.get("euler_modulus"), self.inputs['modulus'])
        
        # Moment of inertia
        self.inputs['inertia'] = QLineEdit()
        self.inputs['inertia'].setPlaceholderText("Örn: 1e-6")
        form.addRow(loc.get("euler_inertia"), self.inputs['inertia'])
        
        # Column length
        self.inputs['length'] = QLineEdit()
        self.inputs['length'].setPlaceholderText("Örn: 2")
        form.addRow(loc.get("euler_length"), self.inputs['length'])
        
        # End conditions
        self.inputs['condition'] = QComboBox()
        self.inputs['condition'].addItem(loc.get("euler_pinned"), "pinned")
        self.inputs['condition'].addItem(loc.get("euler_fixed"), "fixed")
        self.inputs['condition'].addItem(loc.get("euler_fixed_free"), "fixed_free")
        self.inputs['condition'].addItem(loc.get("euler_fixed_pinned"), "fixed_pinned")
        form.addRow(loc.get("euler_end_condition"), self.inputs['condition'])
        
        grp = QGroupBox(loc.get("euler_modulus"))
        grp.setLayout(form)
        layout.addWidget(grp)
        
        # Calculate button
        btn = QPushButton(loc.get("euler_calculate_button"))
        btn.setStyleSheet("background-color: #1971c2; color: white; font-weight: bold; padding: 10px;")
        btn.clicked.connect(self.calculate)
        layout.addWidget(btn)
        
        # Result label
        self.lbl_result = QLabel(loc.get("euler_result_placeholder"))
        self.lbl_result.setStyleSheet("font-size: 13px; margin-top: 10px; padding: 10px; background-color: #f8f9fa; border-radius: 5px;")
        self.lbl_result.setWordWrap(True)
        layout.addWidget(self.lbl_result)
        
        layout.addStretch()
        self.setLayout(layout)
        
    def calculate(self):
        try:
            modulus = float(self.inputs['modulus'].text().replace(',', '.'))
            inertia = float(self.inputs['inertia'].text().replace(',', '.'))
            length = float(self.inputs['length'].text().replace(',', '.'))
            
            condition_str = self.inputs['condition'].currentData()
            k_factor = get_k_factor(condition_str)
            
            if k_factor is None:
                self.lbl_result.setText(loc.get("euler_error_invalid"))
                self.lbl_result.setStyleSheet("color: red; font-weight: bold; padding: 10px;")
                return
            
            result = calculate_euler_column(modulus, inertia, length, k_factor)
            
            if result:
                result_text = loc.get("euler_result_success").format(
                    pcr=result.critical_load,
                    le=result.effective_length,
                    ratio=result.slenderness_ratio
                )
                self.lbl_result.setText(result_text)
                self.lbl_result.setStyleSheet("color: #1971c2; font-weight: bold; padding: 10px; background-color: #e7f5ff; border-left: 4px solid #1971c2;")
            else:
                self.lbl_result.setText(loc.get("euler_error_invalid"))
                self.lbl_result.setStyleSheet("color: red; font-weight: bold; padding: 10px;")
                
        except ValueError:
            self.lbl_result.setText(loc.get("euler_error"))
            self.lbl_result.setStyleSheet("color: red; font-weight: bold; padding: 10px;")
