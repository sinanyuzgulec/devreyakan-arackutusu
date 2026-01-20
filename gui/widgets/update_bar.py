from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QDesktopServices
from core.localization import loc

class UpdateBar(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(40)
        self.download_url = ""
        self.init_ui()
        self.hide() 

    def init_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 0, 10, 0)
        
        self.lbl_msg = QLabel(loc.get("update_bar_default_msg"))
        self.lbl_msg.setStyleSheet("font-weight: bold; color: #1e1e1e;")
        
        btn_update = QPushButton(loc.get("update_bar_btn_review"))
        btn_update.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_update.setStyleSheet("""
            QPushButton { background-color: #1e1e1e; color: white; border: none; padding: 4px 10px; border-radius: 4px; }
            QPushButton:hover { background-color: #333; }
        """)
        btn_update.clicked.connect(self.open_url)
        
        btn_close = QPushButton("✕")
        btn_close.setFlat(True)
        btn_close.setStyleSheet("color: #1e1e1e; font-weight: bold; border: none;")
        btn_close.clicked.connect(self.hide)

        layout.addWidget(self.lbl_msg)
        layout.addStretch()
        layout.addWidget(btn_update)
        layout.addWidget(btn_close)
        
        self.setLayout(layout)

    def show_update(self, version, url, is_modified):
        self.download_url = url
        
        if is_modified:
            self.setStyleSheet("background-color: #ff9800;") 
            self.lbl_msg.setText(loc.get("update_bar_msg_modified").format(version=version))
        else:
            self.setStyleSheet("background-color: #22b28b;")
            self.lbl_msg.setText(loc.get("update_bar_msg_standard").format(version=version))
            
        self.show()

    def open_url(self):
        if self.download_url:
            QDesktopServices.openUrl(QUrl(self.download_url))