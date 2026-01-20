from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QGridLayout, QPushButton, QTextEdit, QLabel, QHBoxLayout, QGroupBox)
from PyQt6.QtCore import Qt 
from .logic import generate_lcd_code
from core.localization import loc

class LcdWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.pixel_buttons = [] 
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout()
        
        
        draw_group = QGroupBox(loc.get("lcd_tool_drawing_area"))
        grid_layout = QGridLayout()
        grid_layout.setSpacing(2)
        
        
        for row in range(8):
            row_buttons = []
            for col in range(5):
                btn = QPushButton()
                btn.setFixedSize(40, 40)
                btn.setCheckable(True)
                
                btn.setStyleSheet("""
                    QPushButton { background-color: #eee; border: 1px solid #ccc; }
                    QPushButton:checked { background-color: #22b28b; }
                """)
                btn.clicked.connect(self.update_code)
                grid_layout.addWidget(btn, row, col)
                row_buttons.append(btn)
            self.pixel_buttons.append(row_buttons)
            
        draw_group.setLayout(grid_layout)
        main_layout.addWidget(draw_group)
        
        
        code_group = QGroupBox(loc.get("lcd_tool_code_output"))
        right_layout = QVBoxLayout()
        
        self.txt_output = QTextEdit()
        self.txt_output.setReadOnly(True)
        self.txt_output.setStyleSheet("font-family: monospace; font-size: 12px;")
        
        btn_clear = QPushButton(loc.get("lcd_tool_clear_button"))
        btn_clear.clicked.connect(self.clear_grid)
        
        btn_copy = QPushButton(loc.get("lcd_tool_copy_button"))
        btn_copy.clicked.connect(self.copy_code)
        
        right_layout.addWidget(self.txt_output)
        right_layout.addWidget(btn_clear)
        right_layout.addWidget(btn_copy)
        code_group.setLayout(right_layout)
        
        main_layout.addWidget(code_group)
        
        self.setLayout(main_layout)
        self.update_code() 

    def update_code(self):
        
        pixels = []
        for row_btns in self.pixel_buttons:
            row_data = [1 if btn.isChecked() else 0 for btn in row_btns]
            pixels.append(row_data)
            
        result = generate_lcd_code(pixels)
        self.txt_output.setText(result['code'])
        
    def clear_grid(self):
        for row in self.pixel_buttons:
            for btn in row:
                btn.setChecked(False)
        self.update_code()

    def copy_code(self):
        self.txt_output.selectAll()
        self.txt_output.copy()