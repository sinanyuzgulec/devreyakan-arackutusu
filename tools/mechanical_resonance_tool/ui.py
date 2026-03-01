from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QLabel, QGroupBox)
from .logic import calculate_resonance
from core.localization import loc

class MechanicalResonanceWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        form = QFormLayout()
        self.inputs = {}
        
        # Mass
        self.inputs['mass'] = QLineEdit()
        self.inputs['mass'].setPlaceholderText("Örn: 0.5")
        form.addRow(loc.get("mechanical_mass"), self.inputs['mass'])
        
        # Stiffness
        self.inputs['stiffness'] = QLineEdit()
        self.inputs['stiffness'].setPlaceholderText("Örn: 1000")
        form.addRow(loc.get("mechanical_stiffness"), self.inputs['stiffness'])
        
        # Damping ratio
        self.inputs['damping'] = QLineEdit()
        self.inputs['damping'].setPlaceholderText("Örn: 0.1")
        form.addRow(loc.get("mechanical_damping"), self.inputs['damping'])
        
        grp = QGroupBox(loc.get("mechanical_mass"))
        grp.setLayout(form)
        layout.addWidget(grp)
        
        # Calculate button
        btn = QPushButton(loc.get("mechanical_calculate_button"))
        btn.setStyleSheet("background-color: #845ef7; color: white; font-weight: bold; padding: 10px;")
        btn.clicked.connect(self.calculate)
        layout.addWidget(btn)
        
        # Result label
        self.lbl_result = QLabel(loc.get("mechanical_result_placeholder"))
        self.lbl_result.setStyleSheet("font-size: 13px; margin-top: 10px; padding: 10px; background-color: #f8f9fa; border-radius: 5px;")
        self.lbl_result.setWordWrap(True)
        layout.addWidget(self.lbl_result)
        
        layout.addStretch()
        self.setLayout(layout)
        
    def calculate(self):
        try:
            mass = float(self.inputs['mass'].text().replace(',', '.'))
            stiffness = float(self.inputs['stiffness'].text().replace(',', '.'))
            damping = float(self.inputs['damping'].text().replace(',', '.'))
            
            result = calculate_resonance(mass, stiffness, damping)
            
            if result:
                result_text = loc.get("mechanical_result_success").format(
                    fn=result.natural_frequency,
                    fd=result.damped_frequency,
                    q=result.quality_factor
                )
                self.lbl_result.setText(result_text)
                self.lbl_result.setStyleSheet("color: #845ef7; font-weight: bold; padding: 10px; background-color: #f3f0ff; border-left: 4px solid #845ef7;")
            else:
                self.lbl_result.setText(loc.get("mechanical_error_invalid"))
                self.lbl_result.setStyleSheet("color: red; font-weight: bold; padding: 10px;")
                
        except ValueError:
            self.lbl_result.setText(loc.get("mechanical_error"))
            self.lbl_result.setStyleSheet("color: red; font-weight: bold; padding: 10px;")
