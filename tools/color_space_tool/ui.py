from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QLabel, QHBoxLayout
)
from PyQt6.QtGui import QColor
from .logic import calculate_rgb565
from core.localization import loc

class ColorSpaceWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        form = QFormLayout()
        
        self.inputs = {}
        self.inputs['r'] = QLineEdit("255")
        self.inputs['g'] = QLineEdit("128")
        self.inputs['b'] = QLineEdit("0")
        
        form.addRow(loc.get("colorwidget_red"), self.inputs['r'])
        form.addRow(loc.get("colorwidget_green"), self.inputs['g'])
        form.addRow(loc.get("colorwidget_blue"), self.inputs['b'])
        
        btn = QPushButton(loc.get("colorwidget_convert_button"))
        btn.clicked.connect(self.calculate)
        
        self.lbl_res = QLabel(loc.get("colorwidget_result_label"))
        self.lbl_res.setStyleSheet("font-family: Monospace; font-size: 13px;")
        
        self.preview_box = QLabel()
        self.preview_box.setFixedSize(60, 60)
        self.preview_box.setStyleSheet("border: 1px solid #888; background-color: rgb(255, 128, 0);")
        
        res_layout = QHBoxLayout()
        res_layout.addWidget(self.lbl_res)
        res_layout.addStretch()
        res_layout.addWidget(self.preview_box)
        
        layout.addLayout(form)
        layout.addWidget(btn)
        layout.addLayout(res_layout)
        layout.addStretch()
        self.setLayout(layout)
        
        self.calculate()
        
    def calculate(self):
        try:
            r = int(self.inputs['r'].text())
            g = int(self.inputs['g'].text())
            b = int(self.inputs['b'].text())
            
            res = calculate_rgb565(r, g, b)
            if res:
                self.preview_box.setStyleSheet(f"border: 1px solid #888; background-color: rgb({res.r8}, {res.g8}, {res.b8});")
                txt = (
                    f"HEX (24-bit): {res.hex24}\n"
                    f"RGB565 (16-bit): {res.rgb565_hex} (Dec: {res.rgb565_dec})\n"
                    f"HSV: H={res.hsv[0]:.1f}° S={res.hsv[1]*100:.1f}% V={res.hsv[2]*100:.1f}%\n"
                    f"CMYK: C={res.cmyk[0]*100:.0f}% M={res.cmyk[1]*100:.0f}% Y={res.cmyk[2]*100:.0f}% K={res.cmyk[3]*100:.0f}%"
                )
                self.lbl_res.setText(txt)
            else:
                self.lbl_res.setText(loc.get("colorwidget_error_range"))
        except ValueError:
            self.lbl_res.setText(loc.get("colorwidget_error_input"))
