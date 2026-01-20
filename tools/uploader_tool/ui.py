from tools.serial_tool.logic import get_serial_ports
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QPushButton, QComboBox, QLabel, QFileDialog, QTextEdit, QMessageBox, QHBoxLayout, QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from .logic import upload_hex
from .boards import BOARD_PRESETS
from .pinout_manager import get_pinout_path  
from core.localization import loc

class UploaderWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.hex_path = ""
        self.init_ui()

    def init_ui(self):
        
        main_layout = QHBoxLayout()
        
        
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        form = QFormLayout()
        
        
        self.lbl_file = QLabel(loc.get("hex_uploader_no_file_selected"))
        self.lbl_file.setStyleSheet("color: #666; font-style: italic;")
        btn_file = QPushButton(loc.get("hex_uploader_select_hex_file"))
        btn_file.clicked.connect(self.select_file)
        form.addRow(btn_file, self.lbl_file)
        
        
        self.combo_board = QComboBox()
        self.combo_board.addItems(BOARD_PRESETS.keys())
        self.combo_board.currentTextChanged.connect(self.update_pinout_image) 
        form.addRow(loc.get("hex_uploader_board_type"), self.combo_board)
        
        
        self.combo_port = QComboBox()
        self.btn_refresh = QPushButton(loc.get("hex_uploader_refresh_ports"))
        self.btn_refresh.setFixedWidth(80)
        self.btn_refresh.clicked.connect(self.refresh_ports)
        self.refresh_ports()
        
        port_layout = QHBoxLayout()
        port_layout.addWidget(self.combo_port)
        port_layout.addWidget(self.btn_refresh)
        form.addRow(loc.get("hex_uploader_port"), port_layout)
        
        left_layout.addLayout(form)
        
        
        self.btn_upload = QPushButton(loc.get("hex_uploader_start_upload"))
        self.btn_upload.setFixedHeight(45)
        self.btn_upload.setStyleSheet("background-color: #f0ad4e; color: white; font-weight: bold; font-size: 14px; margin-top: 10px;")
        self.btn_upload.clicked.connect(self.start_upload)
        left_layout.addWidget(self.btn_upload)


        left_layout.addWidget(QLabel(loc.get("hex_uploader_log_output")))
        self.txt_log = QTextEdit()
        self.txt_log.setReadOnly(True)
        self.txt_log.setStyleSheet("font-family: monospace; font-size: 11px; background: #fafafa;")
        left_layout.addWidget(self.txt_log)
        
        
        right_panel = QFrame()
        right_panel.setFrameShape(QFrame.Shape.StyledPanel)
        right_panel.setStyleSheet("background-color: white; border: 1px solid #ddd; border-radius: 5px;")
        right_layout = QVBoxLayout(right_panel)
        
        lbl_title = QLabel(loc.get("hex_uploader_pinout_image"))
        lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_title.setStyleSheet("font-weight: bold; color: #333; margin-bottom: 5px;")
        right_layout.addWidget(lbl_title)
        
        self.lbl_image = QLabel(loc.get("hex_uploader_no_pinout_image"))
        self.lbl_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_image.setMinimumSize(300, 400) 
        self.lbl_image.setStyleSheet("color: #aaa;")
        right_layout.addWidget(self.lbl_image)
        
        
        
        main_layout.addWidget(left_panel, 40)
        main_layout.addWidget(right_panel, 60)
        
        self.setLayout(main_layout)
        
        
        self.update_pinout_image(self.combo_board.currentText())

    def update_pinout_image(self, board_name):
        path = get_pinout_path(board_name)
        
        if path:
            pixmap = QPixmap(path)
            
            scaled_pixmap = pixmap.scaled(self.lbl_image.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.lbl_image.setPixmap(scaled_pixmap)
        else:
            self.lbl_image.clear()
            self.lbl_image.setText(loc.get("hex_uploader_pinout_not_found"))

    def resizeEvent(self, event):
        self.update_pinout_image(self.combo_board.currentText())
        super().resizeEvent(event)

    def select_file(self):
        path, _ = QFileDialog.getOpenFileName(self, loc.get("hex_uploader_select_hex_file"), "", "HEX Files (*.hex)")
        if path:
            self.hex_path = path
            self.lbl_file.setText(path.split('/')[-1])
            self.lbl_file.setStyleSheet("color: #22b28b; font-weight: bold;")

    def refresh_ports(self):
        self.combo_port.clear()
        
        
        ports_info = get_serial_ports() 
        
        found_match = False
        
        for device, description in ports_info:
            
            self.combo_port.addItem(device)
            self.combo_port.setItemText(self.combo_port.count()-1, f"{device} - {description}")
            self.combo_port.setItemData(self.combo_port.count()-1, device) 
            
            
            
            if not found_match:
                for board_name in BOARD_PRESETS.keys():
                    clean_name = board_name.split('(')[0].strip()
                    
                    if clean_name.lower() in description.lower():
                        
                        print(loc.get("hex_uploader_auto_select_port").format(port=device, board=board_name))
                        
                        
                        index = self.combo_board.findText(board_name)
                        if index >= 0:
                            self.combo_board.setCurrentIndex(index)
                            found_match = True
                            
                            
                            self.combo_port.setCurrentIndex(self.combo_port.count()-1)
                        break

    def start_upload(self):
        if not self.hex_path:
            QMessageBox.warning(self, loc.get("hex_uploader_warning"), loc.get("hex_uploader_no_hex_selected"))
            return
            
        port = self.combo_port.currentData()
        
        
        if not port:
            full_text = self.combo_port.currentText()
            if " - " in full_text:
                port = full_text.split(" - ")[0] 
            else:
                port = full_text

        if not port:
            QMessageBox.warning(self, loc.get("hex_uploader_warning"), loc.get("hex_uploader_no_port_selected"))
            return
            
        board = self.combo_board.currentText()
        
        self.btn_upload.setEnabled(False)
        self.btn_upload.setText(loc.get("hex_uploader_start_upload") + "...")
        self.txt_log.setText(loc.get("hex_uploader_start_upload") + "...\n")
        
        
        from PyQt6.QtWidgets import QApplication
        QApplication.processEvents()
        
        success, log = upload_hex(self.hex_path, port, board)
        
        self.txt_log.setText(log)
        self.btn_upload.setEnabled(True)
        self.btn_upload.setText(loc.get("hex_uploader_start_upload"))
        
        if success:
            QMessageBox.information(self, loc.get("hex_uploader_settings"), loc.get("hex_uploader_upload_success"))
        else:
            QMessageBox.critical(self, loc.get("hex_uploader_settings"), loc.get("hex_uploader_upload_failed"))