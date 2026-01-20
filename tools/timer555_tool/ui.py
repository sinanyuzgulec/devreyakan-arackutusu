from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QGroupBox, QFormLayout, QComboBox)
from PyQt6.QtCore import Qt
from .logic import calc_555_astable, calc_555_monostable
from core.localization import loc

class Timer555Widget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        
        self.mode_combo = QComboBox()
        self.mode_combo.addItems([loc.get("timer555_mode_astable"), loc.get("timer555_mode_monostable")])
        self.mode_combo.currentIndexChanged.connect(self.toggle_mode)
        layout.addWidget(QLabel(loc.get("timer555_mode_label")))
        layout.addWidget(self.mode_combo)

        
        input_group = QGroupBox(loc.get("timer555_input_parameters"))
        form = QFormLayout()
        
        self.input_r1 = QLineEdit()
        self.input_r1.setPlaceholderText(loc.get("timer555_input_r1_placeholder"))
        self.input_r2 = QLineEdit()
        self.input_r2.setPlaceholderText(loc.get("timer555_input_r2_placeholder"))
        self.input_c = QLineEdit()
        self.input_c.setPlaceholderText(loc.get("timer555_input_c_placeholder"))
        form.addRow("R1 (Ohm):", self.input_r1)
        self.label_r2 = QLabel("R2 (Ohm):") 
        self.field_r2 = self.input_r2
        form.addRow(self.label_r2, self.field_r2)
        form.addRow("C (Farad):", self.input_c)
        
        input_group.setLayout(form)
        layout.addWidget(input_group)

        
        btn_calc = QPushButton(loc.get("timer555_button_calculate"))
        btn_calc.setStyleSheet("background-color: #22b28b; color: white; font-weight: bold; padding: 10px;")
        btn_calc.clicked.connect(self.calculate)
        layout.addWidget(btn_calc)

        
        self.result_label = QLabel(loc.get("timer555_result_placeholder"))
        self.result_label.setStyleSheet("font-size: 14px; padding: 10px; background-color: #333; color: #ddd; border-radius: 5px;")
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.result_label)
        
        layout.addStretch()
        self.setLayout(layout)

    def toggle_mode(self):
        is_astable = (self.mode_combo.currentIndex() == 0)
        self.label_r2.setVisible(is_astable)
        self.field_r2.setVisible(is_astable)
        self.result_label.setText(loc.get("timer555_modchange_placeholder"))   

    def calculate(self):
        try:
            r1 = float(self.input_r1.text())
            c = float(self.input_c.text())
            
            if self.mode_combo.currentIndex() == 0: 
                # Astable Mod
                r2 = float(self.input_r2.text())
                res = calc_555_astable(r1, r2, c)
                
                msg = loc.get("timer555_astable_result").format(
                    freq=f"{res.freq:.2f}",
                    period=f"{res.period:.4f}",
                    duty=f"{res.duty_cycle:.1f}",
                    high=f"{res.high_time:.4f}",
                    low=f"{res.low_time:.4f}"
                )

            else: 
                # Monostable Mod
                t = calc_555_monostable(r1, c)
                
                msg = loc.get("timer555_monostable_result").format(
                    time=f"{t:.4f}"
                )
                        
            self.result_label.setText(msg)
            
        except ValueError:
            self.result_label.setText(loc.get("timer555_error_value"))
        except Exception as e:
            self.result_label.setText(loc.get("timer555_error_generic").format(msg=str(e)))