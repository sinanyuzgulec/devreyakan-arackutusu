import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QCheckBox, QLabel, QGroupBox, QScrollArea, QPushButton, QGridLayout, QFormLayout, QLineEdit, QMessageBox, QComboBox)
from PyQt6.QtCore import pyqtSignal, QTimer, QProcess, QCoreApplication
from core.web_server import ServerThread
from core.localization import loc

class SettingsPage(QWidget):
    filter_changed = pyqtSignal(set) 
    language_changed = pyqtSignal(str) 

    def __init__(self, tool_manager):
        super().__init__()
        self.tool_manager = tool_manager
        self.checkboxes = []
        self.server_thread = None
        self.init_ui()

    def init_ui(self):
        
        if self.layout():
            
            QWidget().setLayout(self.layout())
        
        main_layout = QVBoxLayout()
        
        
        title = QLabel(loc.get("settings_title"))
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #22b28b;")
        main_layout.addWidget(title)
        lang_group = QGroupBox(loc.get("lang_select_title"))
        lang_group.setStyleSheet("QGroupBox { font-weight: bold; border: 1px solid #444; margin-top: 10px; }")
        lang_layout = QHBoxLayout()
        
        self.combo_lang = QComboBox()
        
        for code, name in loc.languages.items():
            self.combo_lang.addItem(name, code)
        
        
        index = self.combo_lang.findData(loc.current_lang_code)
        if index >= 0: 
            self.combo_lang.blockSignals(True) 
            self.combo_lang.setCurrentIndex(index)
            self.combo_lang.blockSignals(False)
        
        self.combo_lang.currentIndexChanged.connect(self.on_lang_change)
        
        lang_layout.addWidget(QLabel(loc.get("settings_lang_select_label")))
        lang_layout.addWidget(self.combo_lang)
        lang_group.setLayout(lang_layout)
        main_layout.addWidget(lang_group)

        
        
        
        filter_group = QGroupBox(loc.get("cat_filter_title"))
        filter_group.setStyleSheet("QGroupBox { font-weight: bold; border: 1px solid #444; margin-top: 10px; }")
        
        grid_widget = QWidget()
        grid_layout = QGridLayout()
        
        cats = sorted(list(self.tool_manager.all_categories))
        columns = 3
        for i, cat in enumerate(cats):
            cb = QCheckBox(cat)
            cb.setChecked(True)
            cb.stateChanged.connect(self.notify_change)
            cb.setStyleSheet("font-size: 13px; padding: 5px;")
            
            row = i // columns
            col = i % columns
            grid_layout.addWidget(cb, row, col)
            self.checkboxes.append(cb)

        grid_widget.setLayout(grid_layout)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(grid_widget)
        scroll.setMinimumHeight(150)
        
        filter_layout = QVBoxLayout()
        filter_layout.addWidget(scroll)
        
        btn_layout = QHBoxLayout()
        btn_all = QPushButton(loc.get("btn_select_all"))
        btn_all.clicked.connect(lambda: self.set_all(True))
        btn_none = QPushButton(loc.get("btn_deselect_all"))
        btn_none.clicked.connect(lambda: self.set_all(False))
        
        btn_layout.addWidget(btn_all)
        btn_layout.addWidget(btn_none)
        filter_layout.addLayout(btn_layout)
        
        filter_group.setLayout(filter_layout)
        main_layout.addWidget(filter_group)

        
        
        
        server_group = QGroupBox(loc.get("web_server_title"))
        server_group.setStyleSheet("QGroupBox { font-weight: bold; border: 1px solid #444; margin-top: 10px; }")
        server_layout = QVBoxLayout()
        
        form = QFormLayout()
        
        self.inp_ip = QLineEdit("0.0.0.0")
        self.inp_ip.setPlaceholderText(loc.get("ph_ip"))
        
        self.inp_port = QLineEdit("8080")
        
        self.inp_user = QLineEdit()
        self.inp_user.setPlaceholderText(loc.get("ph_user"))
        
        self.inp_pass = QLineEdit()
        self.inp_pass.setEchoMode(QLineEdit.EchoMode.Password)
        
        form.addRow(loc.get("lbl_ip"), self.inp_ip)
        form.addRow(loc.get("lbl_port"), self.inp_port)
        form.addRow(loc.get("lbl_user"), self.inp_user)
        form.addRow(loc.get("lbl_pass"), self.inp_pass)
        
        self.lbl_status = QLabel(loc.get("status_passive"))
        self.lbl_status.setStyleSheet("color: gray; font-style: italic;")
        
        self.btn_server = QPushButton(loc.get("btn_start"))
        self.btn_server.setStyleSheet("background-color: #22b28b; color: white; font-weight: bold; padding: 8px;")
        self.btn_server.clicked.connect(self.toggle_server)
        
        server_layout.addLayout(form)
        server_layout.addWidget(self.lbl_status)
        server_layout.addWidget(self.btn_server)
        
        server_group.setLayout(server_layout)
        main_layout.addWidget(server_group)

        self.setLayout(main_layout)

    def set_all(self, state):
        for cb in self.checkboxes:
            cb.setChecked(state)

    def notify_change(self):
        selected = {cb.text() for cb in self.checkboxes if cb.isChecked()}
        self.filter_changed.emit(selected)
        
    def on_lang_change(self, index):
        code = self.combo_lang.itemData(index)
        if code != loc.current_lang_code:
            loc.load_language(code)            
            
            # Restart Application
            QCoreApplication.quit()
            QProcess.startDetached(sys.executable, sys.argv)

    def perform_ui_refresh(self):
        self.init_ui()

    def toggle_server(self):
        if self.server_thread and self.server_thread.isRunning():
            self.server_thread.stop_server()
            self.server_thread.quit()
            self.server_thread.wait()
            self.server_thread = None
            
            self.btn_server.setText(loc.get("btn_start"))
            self.btn_server.setStyleSheet("background-color: #22b28b; color: white; font-weight: bold; padding: 8px;")
            self.lbl_status.setText(loc.get("status_stopped"))
            self.lbl_status.setStyleSheet("color: #d9534f;")
            
            self.inp_ip.setEnabled(True)
            self.inp_port.setEnabled(True)
            self.inp_user.setEnabled(True)
            self.inp_pass.setEnabled(True)
        else:
            ip = self.inp_ip.text()
            port = self.inp_port.text()
            
            if not port.isdigit():
                QMessageBox.warning(self, "Error", "Port must be a number.")
                return

            self.inp_ip.setEnabled(False)
            self.inp_port.setEnabled(False)
            self.inp_user.setEnabled(False)
            self.inp_pass.setEnabled(False)
            
            self.server_thread = ServerThread(ip, port, self.inp_user.text(), self.inp_pass.text(), self.tool_manager)
            self.server_thread.status_log.connect(self.update_status)
            self.server_thread.start()
            
            self.btn_server.setText(loc.get("btn_stop"))
            self.btn_server.setStyleSheet("background-color: #d9534f; color: white; font-weight: bold; padding: 8px;")

    def update_status(self, msg):
        self.lbl_status.setText(msg)
        self.lbl_status.setStyleSheet("color: #22b28b; font-weight: bold;")