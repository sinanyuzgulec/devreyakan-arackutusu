
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QLineEdit, QLabel, QTableWidget, QTableWidgetItem, QHeaderView)
from .logic import analyze_struct_format, get_format_help
from core.localization import loc

class StructToolWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel(loc.get("struct_tool_format_label")))
        
        self.inp_fmt = QLineEdit("<H I f")
        self.inp_fmt.setPlaceholderText(loc.get("struct_tool_format_placeholder"))
        self.inp_fmt.textChanged.connect(self.analyze)
        self.inp_fmt.setStyleSheet("font-size: 16px; padding: 5px;")
        layout.addWidget(self.inp_fmt)

        self.lbl_result = QLabel(loc.get("struct_tool_result_size"))
        self.lbl_result.setStyleSheet("font-size: 18px; font-weight: bold; color: #22b28b;")
        layout.addWidget(self.lbl_result)
        
        
        layout.addWidget(QLabel(loc.get("struct_tool_format_help")))
        table = QTableWidget()
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels([loc.get("struct_tool_help_column_format"), loc.get("struct_tool_help_column_description")])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        help_data = get_format_help()
        table.setRowCount(len(help_data))
        
        for i, (k, v) in enumerate(help_data.items()):
            table.setItem(i, 0, QTableWidgetItem(k))
            table.setItem(i, 1, QTableWidgetItem(v))
            
        layout.addWidget(table)
        
        self.setLayout(layout)
        self.analyze()

    def analyze(self):
        fmt = self.inp_fmt.text()
        size, msg = analyze_struct_format(fmt)
        
        if size > 0:
            # Başarılı sonuç şablonu
            res_text = loc.get("struct_tool_total_size").format(size=size)
            self.lbl_result.setText(res_text)
            self.lbl_result.setStyleSheet("font-size: 18px; font-weight: bold; color: #22b28b;")
        else:
            # Hata şablonu
            err_text = loc.get("struct_tool_analysis_error").format(msg=msg)
            self.lbl_result.setText(err_text)
            self.lbl_result.setStyleSheet("color: red;")