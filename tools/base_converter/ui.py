
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QGridLayout, QLabel, QLineEdit, QGroupBox, QTabWidget, QPushButton)
from PyQt6.QtCore import Qt
from .logic import int_to_formats, float_to_hex, hex_to_float
from core.localization import loc

class BaseConverterWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        tabs = QTabWidget()
        tabs.addTab(self.create_int_tab(), loc.get("baseconverterwidget_integer_tab"))
        tabs.addTab(self.create_float_tab(), loc.get("baseconverterwidget_float_tab"))
        
        layout.addWidget(tabs)
        self.setLayout(layout)

    
    def create_int_tab(self):
        widget = QWidget()
        grid = QGridLayout()
        
        
        self.inputs = {}
        labels = ["Decimal (10)", "Hexadecimal (16)", "Binary (2)", "Octal (8)"]
        keys = ['dec', 'hex', 'bin', 'oct']
        
        for idx, (lbl, key) in enumerate(zip(labels, keys)):
            grid.addWidget(QLabel(lbl), idx, 0)
            le = QLineEdit()
            
            le.textChanged.connect(lambda text, k=key: self.on_int_change(text, k))
            self.inputs[key] = le
            grid.addWidget(le, idx, 1)

        
        btn_clear = QPushButton(loc.get("baseconverterwidget_clear_button"))
        btn_clear.clicked.connect(self.clear_int_inputs)
        grid.addWidget(btn_clear, 4, 1)

        widget.setLayout(grid)
        return widget

    def on_int_change(self, text, source_key):
        if not text: return
        
        
        for le in self.inputs.values():
            le.blockSignals(True)
            
        try:
            val = 0
            if source_key == 'dec':
                val = int(text)
            elif source_key == 'hex':
                val = int(text, 16)
            elif source_key == 'bin':
                val = int(text, 2)
            elif source_key == 'oct':
                val = int(text, 8)
                
            results = int_to_formats(val)
            
            
            if source_key != 'dec': self.inputs['dec'].setText(results['dec'])
            if source_key != 'hex': self.inputs['hex'].setText(results['hex'])
            if source_key != 'bin': self.inputs['bin'].setText(results['bin'])
            if source_key != 'oct': self.inputs['oct'].setText(results['oct'])
            
        except ValueError:
            pass 
            
        
        for le in self.inputs.values():
            le.blockSignals(False)

    def clear_int_inputs(self):
        for le in self.inputs.values():
            le.clear()

    
    def create_float_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        grp = QGroupBox("32-bit Float <-> Hex (Big Endian)")
        form = QGridLayout()
        
        self.le_float = QLineEdit()
        self.le_float.setPlaceholderText(loc.get("baseconverterwidget_example_float"))
        self.le_float.returnPressed.connect(self.calc_float_to_hex)
        
        self.le_hex_float = QLineEdit()
        self.le_hex_float.setPlaceholderText(loc.get("baseconverterwidget_example_hex"))
        self.le_hex_float.returnPressed.connect(self.calc_hex_to_float)
        
        btn_f2h = QPushButton("Float -> Hex")
        btn_f2h.clicked.connect(self.calc_float_to_hex)
        
        btn_h2f = QPushButton("Hex -> Float")
        btn_h2f.clicked.connect(self.calc_hex_to_float)
        
        form.addWidget(QLabel(loc.get("baseconverterwidget_input_label")), 0, 0)
        form.addWidget(self.le_float, 0, 1)
        form.addWidget(btn_f2h, 0, 2)
        
        form.addWidget(QLabel(loc.get("baseconverterwidget_hex_label")), 1, 0)
        form.addWidget(self.le_hex_float, 1, 1)
        form.addWidget(btn_h2f, 1, 2)
        
        grp.setLayout(form)
        layout.addWidget(grp)
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget

    def calc_float_to_hex(self):
        try:
            val = float(self.le_float.text().replace(',', '.'))
            hex_res = float_to_hex(val)
            self.le_hex_float.setText(hex_res)
        except:
            self.le_hex_float.setText(loc.get("baseconverterwidget_error"))

    def calc_hex_to_float(self):
        hex_txt = self.le_hex_float.text()
        val = hex_to_float(hex_txt)
        if val is not None:
            self.le_float.setText(f"{val:.6f}") 
        else:
            self.le_float.setText(loc.get("baseconverterwidget_error"))