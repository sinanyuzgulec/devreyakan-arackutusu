
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QLabel, QRadioButton, QButtonGroup, QTabWidget, QLineEdit, QPushButton, QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QColor, QBrush, QPen
from .logic import RESISTOR_DATA, COLOR_LIST, calculate_value_from_colors, calculate_colors_from_value
from core.localization import loc

class ResistorWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        
        tabs = QTabWidget()
        tabs.addTab(self.create_color_to_val_tab(), loc.get("resistor_tool_color_to_value"))
        tabs.addTab(self.create_val_to_color_tab(), loc.get("resistor_tool_value_to_color"))
        
        layout.addWidget(tabs)
        self.setLayout(layout)

    
    def create_color_to_val_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        h_layout = QHBoxLayout()
        self.band_group = QButtonGroup(self)
        
        for i in [4, 5, 6]:
            rb_text = loc.get("resistor_tool_band_label").format(n=i)
            rb = QRadioButton(rb_text)
            
            if i == 4: rb.setChecked(True)
            self.band_group.addButton(rb, i)
            h_layout.addWidget(rb)
            
        self.band_group.idClicked.connect(self.update_ui_bands)
        layout.addLayout(h_layout)
        
        
        self.combos = []
        combo_layout = QHBoxLayout()
        
        
        labels = [loc.get("resistor_tool_digit_1"), loc.get("resistor_tool_digit_2"),
                  loc.get("resistor_tool_digit_3"), loc.get("resistor_tool_multiplier"),
                  loc.get("resistor_tool_tolerance"), loc.get("resistor_tool_ppm")]
        for i in range(6):
            vbox = QVBoxLayout()
            lbl = QLabel(labels[i])
            cb = QComboBox()
            self.populate_combo(cb, i)
            cb.currentIndexChanged.connect(self.calculate_result)
            
            vbox.addWidget(lbl)
            vbox.addWidget(cb)
            combo_layout.addLayout(vbox)
            self.combos.append((lbl, cb)) 
            
        layout.addLayout(combo_layout)
        
        
        self.canvas = ResistorCanvas()
        self.canvas.setMinimumHeight(150)
        layout.addWidget(self.canvas)
        
        
        self.lbl_result = QLabel(loc.get("resistor_tool_result_display"))
        self.lbl_result.setStyleSheet("font-size: 24px; font-weight: bold; color: #22b28b; margin: 10px;")
        self.lbl_result.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.lbl_result)
        
        layout.addStretch()
        widget.setLayout(layout)
        
        self.update_ui_bands(4) 
        return widget

    
    def create_val_to_color_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        form_layout = QHBoxLayout()
        self.txt_ohm = QLineEdit()
        self.txt_ohm.setPlaceholderText(loc.get("resistor_tool_enter_value_placeholder"))
        
        btn_calc = QPushButton(loc.get("resistor_tool_calculate_colors"))
        btn_calc.clicked.connect(self.reverse_calc)
        
        form_layout.addWidget(QLabel(loc.get("resistor_tool_value_label")))
        form_layout.addWidget(self.txt_ohm)
        form_layout.addWidget(btn_calc)
        layout.addLayout(form_layout)
        
        
        h_layout = QHBoxLayout()
        self.rev_band_group = QButtonGroup(self)
        
        for i in [4, 5]: 
            
            rb_text = loc.get("resistor_tool_band_option").format(n=i)
            rb = QRadioButton(rb_text)
            
            if i == 4: rb.setChecked(True)
            self.rev_band_group.addButton(rb, i)
            h_layout.addWidget(rb)
            
        layout.addLayout(h_layout)
        
        self.lbl_rev_result = QLabel(loc.get("resistor_tool_color_result_display"))
        self.lbl_rev_result.setStyleSheet("font-size: 16px; margin-top: 20px;")
        layout.addWidget(self.lbl_rev_result)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget

    def populate_combo(self, cb, index):
        
        
        
        for color in COLOR_LIST:
            cb.addItem(color)
            
            model_idx = cb.model().index(cb.count()-1, 0)
            cb.model().setData(model_idx, QColor(RESISTOR_DATA[color][4]), Qt.ItemDataRole.DecorationRole)

    def update_ui_bands(self, band_count):
        
        
        
        
        
        
        
        
        for i in range(6):
            visible = True
            if band_count == 4:
                if i == 2 or i == 5: visible = False 
            elif band_count == 5:
                if i == 5: visible = False 
            
            self.combos[i][0].setVisible(visible)
            self.combos[i][1].setVisible(visible)
            
        self.calculate_result()

    def calculate_result(self):
        band_count = self.band_group.checkedId()
        colors = []
        
        
        
        
        
        c_names = [cb.currentText() for _, cb in self.combos]
        
        final_bands = []
        if band_count == 4:
            final_bands = [c_names[0], c_names[1], c_names[3], c_names[4]]
        elif band_count == 5:
            final_bands = [c_names[0], c_names[1], c_names[2], c_names[3], c_names[4]]
        elif band_count == 6:
            final_bands = c_names 
            
        
        res = calculate_value_from_colors(final_bands)
        if res:
            val, tol, ppm = res
            
            
            unit = "Ω"
            if val >= 1e9: val /= 1e9; unit = "GΩ"
            elif val >= 1e6: val /= 1e6; unit = "MΩ"
            elif val >= 1e3: val /= 1e3; unit = "kΩ"
            
            ppm_str = f" {ppm}ppm" if ppm else ""
            self.lbl_result.setText(f"{val:.2f} {unit} ±%{tol}{ppm_str}")
            
            
            self.canvas.update_colors(final_bands)

    def reverse_calc(self):
        text = self.txt_ohm.text().lower().replace(',', '.')
        
        mult = 1
        if 'k' in text: mult = 1000; text = text.replace('k', '')
        if 'm' in text: mult = 1000000; text = text.replace('m', '')
        
        try:
            val = float(text) * mult
            bands = self.rev_band_group.checkedId()
            colors = calculate_colors_from_value(val, bands)
            
            
            html = loc.get("resistor_tool_color_bands")
            for c in colors:
                hex_c = RESISTOR_DATA[c][4]
                html += f"<span style='background-color:{hex_c}; color:white; padding:5px;'>{c}</span> "
            
            self.lbl_rev_result.setText(html)
        except:
            self.lbl_rev_result.setText(loc.get("resistor_tool_invalid_value"))


class ResistorCanvas(QFrame):
    def __init__(self):
        super().__init__()
        self.colors = ["Red", "Red", "Brown", "Gold"] 
        self.setStyleSheet("background-color: white; border: 1px solid #ddd;")

    def update_colors(self, bands):
        self.colors = bands
        self.repaint()

    def paintEvent(self, event):
        qp = QPainter(self)
        qp.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        w = self.width()
        h = self.height()
        
        
        body_color = QColor("#E0D8B0")
        qp.setBrush(QBrush(body_color))
        qp.setPen(Qt.PenStyle.NoPen)
        
        
        rect_w = w * 0.6
        rect_h = h * 0.4
        rect_x = (w - rect_w) / 2
        rect_y = (h - rect_h) / 2
        
        
        qp.setPen(QPen(QColor("#666"), 4))
        qp.drawLine(0, int(h/2), int(w), int(h/2))
        
        
        qp.setPen(Qt.PenStyle.NoPen)
        qp.drawRoundedRect(int(rect_x), int(rect_y), int(rect_w), int(rect_h), 10, 10)
        
        
        if not self.colors: return
        
        num_bands = len(self.colors)
        band_w = rect_w / (num_bands * 2 + 1)
        start_x = rect_x + band_w
        
        for i, c_name in enumerate(self.colors):
            hex_c = RESISTOR_DATA.get(c_name, (0,0,0,0,"#000"))[4]
            qp.setBrush(QBrush(QColor(hex_c)))
            
            
            pos_x = start_x + (i * band_w * 1.5)
            if i == num_bands - 1: 
                pos_x += band_w * 0.5
                
            qp.drawRect(int(pos_x), int(rect_y), int(band_w), int(rect_h))