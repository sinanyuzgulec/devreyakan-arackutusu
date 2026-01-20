
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPlainTextEdit, QLabel, QRadioButton, QButtonGroup, QTableWidget, QTableWidgetItem, QHeaderView, QPushButton)
from PyQt6.QtCore import Qt
from .logic import calculate_checksums
from core.localization import loc
class ChecksumToolWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        type_layout = QHBoxLayout()
        self.type_group = QButtonGroup(self)
        
        rb_ascii = QRadioButton(loc.get("checksumtoolwidget_ascii_input"))
        rb_hex = QRadioButton(loc.get("checksumtoolwidget_hex_input"))
        rb_ascii.setChecked(True)
        
        self.type_group.addButton(rb_ascii, 1)
        self.type_group.addButton(rb_hex, 2)
        
        type_layout.addWidget(QLabel(loc.get("checksumtoolwidget_input_type")))
        type_layout.addWidget(rb_ascii)
        type_layout.addWidget(rb_hex)
        type_layout.addStretch()
        
        layout.addLayout(type_layout)
        
        
        self.txt_input = QPlainTextEdit()
        self.txt_input.setPlaceholderText(loc.get("checksumtoolwidget_input_placeholder"))
        self.txt_input.setMaximumHeight(100)
        self.txt_input.textChanged.connect(self.calculate)
        layout.addWidget(self.txt_input)
        
        
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(loc.get("checksumtoolwidget_result_table_headers"))
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        
        layout.addWidget(QLabel(loc.get("checksumtoolwidget_result_label")))
        
        layout.addWidget(self.table)
        
        
        btn_clear = QPushButton(loc.get("checksumtoolwidget_clear_button"))
        btn_clear.clicked.connect(self.txt_input.clear)
        layout.addWidget(btn_clear)
        
        self.setLayout(layout)

    def calculate(self):
        text = self.txt_input.toPlainText()
        if not text:
            self.table.setRowCount(0)
            return
            
        data_bytes = b""
        try:
            if self.type_group.checkedId() == 1: 
                data_bytes = text.encode('utf-8')
            else: 
                
                clean_hex = text.replace(' ', '').replace('0x', '').replace('\n', '')
                data_bytes = bytes.fromhex(clean_hex)
        except Exception:
            
            return

        
        results = calculate_checksums(data_bytes)
        
        
        self.table.setRowCount(0)
        for algo, val in results.items():
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(algo))
            self.table.setItem(row, 1, QTableWidgetItem(val))