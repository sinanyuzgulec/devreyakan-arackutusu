
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QLabel, QTabWidget)
from PyQt6.QtCore import Qt
from .logic import latlon_to_locator, locator_to_latlon
from core.localization import loc

class QthToolWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        tabs = QTabWidget()
        
        tabs.addTab(self.create_gps_to_loc(), "GPS -> Locator")
        tabs.addTab(self.create_loc_to_gps(), "Locator -> GPS")
        
        layout.addWidget(tabs)
        self.setLayout(layout)

    def create_gps_to_loc(self):
        w = QWidget()
        l = QVBoxLayout()
        form = QFormLayout()
        
        self.inp_lat = QLineEdit("41.0082")
        self.inp_lon = QLineEdit("28.9784")
        
        form.addRow(loc.get("qth_tool_latitude"), self.inp_lat)
        form.addRow(loc.get("qth_tool_longitude"), self.inp_lon)
        
        btn = QPushButton(loc.get("qth_tool_calculate_button"))
        btn.clicked.connect(self.calc_to_loc)
        
        self.res_loc = QLabel("-")
        self.res_loc.setStyleSheet("font-size: 36px; font-weight: bold; color: #d9534f;")
        self.res_loc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.res_loc.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        
        l.addLayout(form)
        l.addWidget(btn)
        l.addWidget(self.res_loc)
        l.addStretch()
        w.setLayout(l)
        return w

    def create_loc_to_gps(self):
        w = QWidget()
        l = QVBoxLayout()
        
        self.inp_loc = QLineEdit("KN41bd")
        self.inp_loc.setPlaceholderText(loc.get("qth_tool_locator_label"))
        self.inp_loc.setStyleSheet("font-size: 20px; text-transform: uppercase;")
        
        btn = QPushButton(loc.get("qth_tool_calculate_button"))
        btn.clicked.connect(self.calc_to_gps)
        
        self.res_gps = QLabel("-")
        self.res_gps.setStyleSheet("font-size: 20px; font-weight: bold; color: #22b28b;")
        self.res_gps.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.res_gps.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        
        l.addWidget(QLabel(loc.get("qth_tool_locator_six_chars_info")))
        l.addWidget(self.inp_loc)
        l.addWidget(btn)
        l.addWidget(self.res_gps)
        l.addStretch()
        w.setLayout(l)
        return w

    def calc_to_loc(self):
        try:
            lat = float(self.inp_lat.text().replace(',', '.'))
            lon = float(self.inp_lon.text().replace(',', '.'))
            res = latlon_to_locator(lat, lon)
            self.res_loc.setText(res)
        except:
            self.res_loc.setText(loc.get("qth_tool_invalid_input"))

    def calc_to_gps(self):
        try:
            
            
            qth_input = self.inp_loc.text()
            
            
            lat, lon = locator_to_latlon(qth_input)
            
            if lat == 0 and lon == 0:
                self.res_gps.setText(loc.get("qth_tool_invalid_input"))
            else:
                self.res_gps.setText(f"{lat:.6f}, {lon:.6f}")
                
        except Exception as e:
            print(f"Error: {e}") 
            self.res_gps.setText(loc.get("qth_tool_invalid_input"))