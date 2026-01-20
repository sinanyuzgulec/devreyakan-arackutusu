from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QGridLayout, QLabel, QLineEdit, QPushButton, QMessageBox)
from .logic import calculate_ohm
from core.localization import loc

class OhmWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QGridLayout()
        
        self.inputs = {}
        labels = [loc.get("ohm_tool_voltage"), loc.get("ohm_tool_current"), loc.get("ohm_tool_resistance"), loc.get("ohm_tool_power")]
        keys = ['v', 'i', 'r', 'p']
        
        for idx, (text, key) in enumerate(zip(labels, keys)):
            layout.addWidget(QLabel(text), idx, 0)
            le = QLineEdit()
            le.setPlaceholderText(loc.get("ohm_tool_input_placeholder"))
            self.inputs[key] = le
            layout.addWidget(le, idx, 1)

        btn_calc = QPushButton(loc.get("ohm_tool_calculate_button"))
        btn_calc.clicked.connect(self.on_calculate)
        layout.addWidget(btn_calc, 4, 0, 1, 2)
        
        self.lbl_result = QLabel(loc.get("ohm_tool_result_label"))
        layout.addWidget(self.lbl_result, 5, 0, 1, 2)
        
        self.setLayout(layout)

    def on_calculate(self):
        
        vals = {}
        for key, le in self.inputs.items():
            text = le.text().replace(',', '.') 
            vals[key] = float(text) if text else None
            
        try:
            res = calculate_ohm(**vals)
            if not res:
                self.lbl_result.setText(loc.get("ohm_tool_insufficient_data"))
                return
                
            out_str = loc.get("ohm_tool_results") + "\n"
            for k, v in res.items():
                out_str += f"{k.title()}: {v.val:.2f} {v.unit}\n"
            self.lbl_result.setText(out_str)
            
        except Exception as e:
            QMessageBox.critical(self, loc.get("ohm_tool_error_title"), str(e))