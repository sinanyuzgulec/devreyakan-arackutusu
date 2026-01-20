
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QSlider, QLabel, QGroupBox, QPushButton)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPainter, QPen, QColor, QPainterPath
from .logic import PidModel
from core.localization import loc

class PidWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.model = PidModel()
        self.history = []
        self.setpoint = 50.0
        self.time_step = 0
        
        self.kp = 1.0
        self.ki = 0.0
        self.kd = 0.0
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.sim_step)
        
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        
        self.canvas = GraphCanvas()
        layout.addWidget(self.canvas, 1) 
        
        
        ctrl_layout = QHBoxLayout()
        
        ctrl_layout.addLayout(self.create_slider(loc.get("pid_tool_proportional"), 0, 100, self.set_kp))
        ctrl_layout.addLayout(self.create_slider(loc.get("pid_tool_integral"), 0, 50, self.set_ki))
        ctrl_layout.addLayout(self.create_slider(loc.get("pid_tool_derivative"), 0, 100, self.set_kd))
        
        layout.addLayout(ctrl_layout)
        
        
        btn_layout = QHBoxLayout()
        btn_start = QPushButton(loc.get("pid_tool_restart_simulation"))
        btn_start.clicked.connect(self.restart_sim)
        btn_layout.addWidget(btn_start)
        
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
        self.restart_sim()

    def create_slider(self, label, min_val, max_val, callback):
        l = QVBoxLayout()
        lbl = QLabel(f"{label}: 0.0")
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setRange(min_val, max_val)
        slider.setValue(0)
        
        def on_change(val):
            real_val = val / 10.0
            lbl.setText(f"{label.split(' ')[0]}: {real_val}")
            callback(real_val)
            
        slider.valueChanged.connect(on_change)
        l.addWidget(lbl)
        l.addWidget(slider)
        return l

    def set_kp(self, v): self.kp = v
    def set_ki(self, v): self.ki = v
    def set_kd(self, v): self.kd = v

    def restart_sim(self):
        self.model.reset()
        self.history = []
        self.time_step = 0
        self.timer.start(30) 

    def sim_step(self):
        val = self.model.update(self.setpoint, self.kp, self.ki, self.kd)
        self.history.append(val)
        

        if len(self.history) > 300:
            self.history.pop(0)
            
        self.canvas.update_data(self.history, self.setpoint)
        self.time_step += 1

class GraphCanvas(QWidget):
    def __init__(self):
        super().__init__()
        self.data = []
        self.setpoint = 0
        self.setStyleSheet("background-color: #222; border: 1px solid #555;")
        self.setMinimumHeight(200)

    def update_data(self, data, setpoint):
        self.data = data
        self.setpoint = setpoint
        self.update() 

    def paintEvent(self, event):
        qp = QPainter(self)
        qp.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        w = self.width()
        h = self.height()
        
        
        scale_y = h / 100.0 
        sp_y = h - (self.setpoint * scale_y)
        
        qp.setPen(QPen(QColor("#00FF00"), 1, Qt.PenStyle.DashLine))
        qp.drawLine(0, int(sp_y), w, int(sp_y))
        
        
        if len(self.data) > 1:
            path = QPainterPath()
            step_x = w / 300.0
            
            start_y = h - (self.data[0] * scale_y)
            path.moveTo(0, start_y)
            
            for i, val in enumerate(self.data):
                x = i * step_x
                y = h - (val * scale_y)
                
                y = max(0, min(h, y))
                path.lineTo(x, y)
                
            qp.setPen(QPen(QColor("#FFFF00"), 2))
            qp.drawPath(path)
