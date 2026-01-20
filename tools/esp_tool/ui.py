from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QPushButton, 
                             QComboBox, QLabel, QFileDialog, QTextEdit, 
                             QMessageBox, QHBoxLayout, QFrame, QLineEdit, 
                             QApplication, QGroupBox)
from PyQt6.QtCore import Qt
from tools.serial_tool.logic import get_serial_ports
from .logic import upload_esp_bin
from core.localization import loc

class EspUploaderWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.bin_path = ""
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout()
        main_layout.setSpacing(10)

        # --- LEFT PANEL (Controls) ---
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        # 1. File Selection Area
        file_group = QGroupBox(loc.get("esp_tool_select_file")) 
        file_layout = QVBoxLayout()
        
        self.lbl_file = QLabel(loc.get("esp_tool_no_file"))
        self.lbl_file.setStyleSheet("color: #666; font-style: italic; margin-bottom: 5px;")
        self.lbl_file.setWordWrap(True)
        
        btn_file = QPushButton(loc.get("esp_tool_select_file"))
        btn_file.clicked.connect(self.select_file)
        
        file_layout.addWidget(self.lbl_file)
        file_layout.addWidget(btn_file)
        file_group.setLayout(file_layout)
        left_layout.addWidget(file_group)

        # 2. Port Selection
        port_layout = QHBoxLayout()
        self.combo_port = QComboBox()
        self.btn_refresh = QPushButton(loc.get("esp_tool_refresh_btn"))
        self.btn_refresh.setFixedWidth(80)
        self.btn_refresh.clicked.connect(self.refresh_ports)
        
        port_layout.addWidget(self.combo_port)
        port_layout.addWidget(self.btn_refresh)
        
        left_layout.addWidget(QLabel(loc.get("esp_tool_port_label")))
        left_layout.addLayout(port_layout)

        # 3. Settings Group
        settings_group = QGroupBox(loc.get("esp_tool_settings_group"))
        form = QFormLayout()
        
        self.combo_chip = QComboBox()
        self.combo_chip.addItems(["auto", "esp32", "esp8266", "esp32s2", "esp32c3", "esp32s3"])
        form.addRow(loc.get("esp_tool_chip_label"), self.combo_chip)

        self.combo_baud = QComboBox()
        self.combo_baud.addItems(["115200", "230400", "460800", "921600", "1500000"])
        self.combo_baud.setCurrentText("460800")
        form.addRow(loc.get("esp_tool_baud_label"), self.combo_baud)

        self.txt_address = QLineEdit("0x0")
        self.txt_address.setPlaceholderText(loc.get("esp_tool_offset_placeholder"))
        form.addRow(loc.get("esp_tool_offset_label"), self.txt_address)
        
        settings_group.setLayout(form)
        left_layout.addWidget(settings_group)

        # 4. Action Button
        self.btn_upload = QPushButton(loc.get("esp_tool_start_btn"))
        self.btn_upload.setFixedHeight(45)
        self.btn_upload.setStyleSheet("""
            QPushButton {
                background-color: #d9534f; 
                color: white; 
                font-weight: bold; 
                font-size: 14px; 
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #c9302c;
            }
            QPushButton:disabled {
                background-color: #e0e0e0;
                color: #888;
            }
        """)
        self.btn_upload.clicked.connect(self.start_upload)
        left_layout.addWidget(self.btn_upload)

        # 5. Log Area
        left_layout.addWidget(QLabel(loc.get("esp_tool_log_label")))
        self.txt_log = QTextEdit()
        self.txt_log.setReadOnly(True)
        self.txt_log.setStyleSheet("font-family: monospace; font-size: 11px; background: #2b2b2b; color: #00ff00; border-radius: 4px;")
        left_layout.addWidget(self.txt_log)

        # --- RIGHT PANEL (Info) ---
        right_panel = QFrame()
        right_panel.setFrameShape(QFrame.Shape.StyledPanel)
        # GÜNCELLEME: Arka plan koyu (#2b2b2b) ve kenarlıklar uyumlu hale getirildi
        right_panel.setStyleSheet("background-color: #2b2b2b; border: 1px solid #444; border-radius: 5px;")
        right_layout = QVBoxLayout(right_panel)
        
        lbl_info_title = QLabel(loc.get("esp_tool_info_title"))
        lbl_info_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # GÜNCELLEME: Başlık rengi beyaza (#ffffff) çevrildi
        lbl_info_title.setStyleSheet("font-weight: bold; font-size: 15px; color: #ffffff; margin-bottom: 10px;")
        
        info_text = QLabel(loc.get("esp_tool_info_content"))
        info_text.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        info_text.setWordWrap(True)
        # GÜNCELLEME: Bilgi metni rengi açık griye (#cccccc) çevrildi
        info_text.setStyleSheet("color: #cccccc; font-size: 13px; line-height: 1.4;")
        
        right_layout.addWidget(lbl_info_title)
        right_layout.addWidget(info_text)
        right_layout.addStretch()

        # Add panels to main layout
        main_layout.addWidget(left_panel, 65)
        main_layout.addWidget(right_panel, 35)

        self.setLayout(main_layout)
        self.refresh_ports()

    def select_file(self):
        path, _ = QFileDialog.getOpenFileName(self, loc.get("esp_tool_select_file"), "", "Binary Files (*.bin);;All Files (*)")
        if path:
            self.bin_path = path
            self.lbl_file.setText(path.split('/')[-1])
            self.lbl_file.setStyleSheet("color: #d9534f; font-weight: bold; margin-bottom: 5px;")

    def refresh_ports(self):
        self.combo_port.clear()
        ports_info = get_serial_ports()
        for device, description in ports_info:
            self.combo_port.addItem(f"{device} - {description}", device)
            if "CP210" in description or "CH340" in description:
                self.combo_port.setCurrentIndex(self.combo_port.count()-1)

    def start_upload(self):
        if not self.bin_path:
            QMessageBox.warning(self, loc.get("esp_tool_msg_warning"), loc.get("esp_tool_msg_no_file_selected"))
            return

        port = self.combo_port.currentData()
        if not port:
            QMessageBox.warning(self, loc.get("esp_tool_msg_warning"), loc.get("esp_tool_msg_no_port_selected"))
            return

        baud = self.combo_baud.currentText()
        chip = self.combo_chip.currentText()
        addr = self.txt_address.text()

        self.btn_upload.setEnabled(False)
        self.btn_upload.setText(loc.get("esp_tool_flashing_btn"))
        self.txt_log.setText(loc.get("esp_tool_log_starting") + "\n")
        QApplication.processEvents()

        success, log = upload_esp_bin(self.bin_path, port, baud, chip, addr)

        self.txt_log.setText(log)
        self.btn_upload.setEnabled(True)
        self.btn_upload.setText(loc.get("esp_tool_start_btn"))

        if success:
            QMessageBox.information(self, loc.get("esp_tool_msg_success_title"), loc.get("esp_tool_msg_success_text"))
        else:
            QMessageBox.critical(self, loc.get("esp_tool_msg_fail_title"), loc.get("esp_tool_msg_fail_text"))