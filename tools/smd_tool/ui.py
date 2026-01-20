from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QTabWidget, QListWidget, QFrame, QSplitter)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QColor, QBrush, QPen, QFont
from .logic import calculate_smd_code
from .data import SMD_PACKAGES
from core.localization import loc

class SmdToolWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        tabs = QTabWidget()
        
        tabs.addTab(self.create_calculator_tab(), loc.get("smd_tool_calculator_tab"))
        tabs.addTab(self.create_package_tab(), loc.get("smd_tool_package_tab"))
        
        layout.addWidget(tabs)
        self.setLayout(layout)

    
    def create_calculator_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
               
        lbl_info = QLabel(loc.get("smd_tool_calculator_info"))
        lbl_info.setStyleSheet("color: #666; font-style: italic;")
        
        self.txt_code = QLineEdit()
        self.txt_code.setPlaceholderText(loc.get("smd_tool_enter_code_placeholder"))
        self.txt_code.setStyleSheet("font-size: 18px; padding: 10px;")
        self.txt_code.textChanged.connect(self.run_calc)
        
        self.lbl_result = QLabel("-")
        self.lbl_result.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_result.setStyleSheet("font-size: 28px; font-weight: bold; color: #22b28b; margin: 20px;")
        
        self.lbl_algo = QLabel("")
        self.lbl_algo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(lbl_info)
        layout.addWidget(self.txt_code)
        layout.addWidget(self.lbl_result)
        layout.addWidget(self.lbl_algo)
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget

    def run_calc(self, text):
        val, unit, algo = calculate_smd_code(text)
        
        if val is not None:
            res_text = loc.get("smd_tool_result_template").format(
                val=f"{val:.2f}", 
                unit=unit
            )
            self.lbl_result.setText(res_text)
            
            algo_text = loc.get("smd_tool_detected_format").format(algo=algo)
            self.lbl_algo.setText(algo_text)
            
            self.lbl_algo.setStyleSheet("color: blue;")
        else:
            self.lbl_result.setText("-")
            self.lbl_algo.setText("")

    
    def create_package_tab(self):
        widget = QWidget()
        layout = QHBoxLayout()
        
        
        self.pkg_list = QListWidget()
        for pkg in SMD_PACKAGES:
            self.pkg_list.addItem(f"{pkg['name']} (Metric: {pkg['metric']})")
        self.pkg_list.currentRowChanged.connect(self.update_drawing)
        
        
        self.canvas = PackageCanvas()
        
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self.pkg_list)
        splitter.addWidget(self.canvas)
        splitter.setSizes([200, 400])
        
        layout.addWidget(splitter)
        widget.setLayout(layout)
        return widget

    def update_drawing(self, index):
        if index >= 0:
            pkg_data = SMD_PACKAGES[index]
            self.canvas.set_package(pkg_data)


class PackageCanvas(QFrame):
    def __init__(self):
        super().__init__()
        self.current_pkg = None
        self.setStyleSheet("background-color: white;")

    def set_package(self, pkg_data):
        self.current_pkg = pkg_data
        self.repaint()

    def paintEvent(self, event):
        qp = QPainter(self)
        qp.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        w = self.width()
        h = self.height()
        
        
        
        SCALE = 40 
        
        
        cx, cy = w // 2, h // 2
        
        
        qp.setPen(QPen(QColor("#eee"), 1))
        for x in range(0, w, SCALE):
            qp.drawLine(x, 0, x, h)
        for y in range(0, h, SCALE):
            qp.drawLine(0, y, w, y)
            
        if not self.current_pkg:
            qp.drawText(cx-50, cy, loc.get("smd_tool_select_package_prompt"))
            return

        
        pw = self.current_pkg['l'] * SCALE
        ph = self.current_pkg['w'] * SCALE
        
        
        
        qp.setBrush(QBrush(QColor("#333")))
        qp.setPen(Qt.PenStyle.NoPen)
        qp.drawRect(int(cx - pw/2), int(cy - ph/2), int(pw), int(ph))
        
        
        pad_size = pw * 0.2 
        qp.setBrush(QBrush(QColor("#C0C0C0")))
        
        
        qp.drawRect(int(cx - pw/2), int(cy - ph/2), int(pad_size), int(ph))
        
        qp.drawRect(int(cx + pw/2 - pad_size), int(cy - ph/2), int(pad_size), int(ph))
        
        
        qp.setPen(QColor("red"))
        qp.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        
        info_txt = f"{self.current_pkg['name']} ({self.current_pkg['metric']})"
        dim_txt = f"{self.current_pkg['l']}mm x {self.current_pkg['w']}mm"
        
        qp.drawText(int(cx - pw/2), int(cy - ph/2 - 25), info_txt)
        qp.drawText(int(cx - pw/2), int(cy - ph/2 - 10), dim_txt)
        
        
        qp.setPen(QColor("#666"))
        qp.setFont(QFont("Arial", 9, QFont.Weight.Normal))
        qp.drawText(10, h - 20, f"Note: {self.current_pkg['desc']}")
        qp.drawText(10, h - 40, loc.get("smd_tool_package_note"))