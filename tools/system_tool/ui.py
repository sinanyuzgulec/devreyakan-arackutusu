import platform
import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QGroupBox, QFormLayout, QLabel) 
from core.localization import loc

class SystemWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        grp = QGroupBox(loc.get("system_tool_name"))
        form = QFormLayout()
        
        
        infos = [
            (loc.get("system_tool_os"), f"{platform.system()} {platform.release()}"),
            (loc.get("system_tool_version"), platform.version()),
            (loc.get("system_tool_architecture"), platform.machine()),
            (loc.get("system_tool_processor"), platform.processor() or "Bilgi Yok"),
            (loc.get("system_tool_hostname"), platform.node()),
            (loc.get("system_tool_python_version"), sys.version.split()[0]),
            (loc.get("system_tool_python_implementation"), platform.python_implementation())
        ]
        
        for label, value in infos:
            lbl_val = QLabel(value)
            lbl_val.setStyleSheet("font-weight: bold; color: #333;")
            form.addRow(label, lbl_val)
            
        grp.setLayout(form)
        layout.addWidget(grp)
        layout.addStretch()
        self.setLayout(layout)