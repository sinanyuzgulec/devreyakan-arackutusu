from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QTableWidget, QTableWidgetItem, QLabel, QHeaderView, QSplitter)
from PyQt6.QtCore import Qt
from .logic import CircuitSolver
from core.localization import loc

DEFAULT_NETLIST = """* Voltage Divider Example
* Format: Type Name Node1 Node2 Value

V1 1 0 10
R1 1 2 1k
R2 2 0 1k

* Current Source Example
* I1 2 0 0.005
"""

class CircuitSimWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.solver = CircuitSolver()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        
        
        info_lbl = QLabel(loc.get("circuit_sim_name"))
        info_lbl.setStyleSheet("font-weight: bold; font-size: 14px; color: #555;")
        main_layout.addWidget(info_lbl)
        
        
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        
        editor_widget = QWidget()
        editor_layout = QVBoxLayout(editor_widget)
        editor_layout.setContentsMargins(0,0,0,0)
        
        self.txt_netlist = QTextEdit()
        self.txt_netlist.setPlaceholderText(loc.get("circuit_sim_netlist_placeholder"))
        self.txt_netlist.setText(DEFAULT_NETLIST)
        self.txt_netlist.setStyleSheet("font-family: monospace; font-size: 12px; color: #333;")
        
        btn_solve = QPushButton(loc.get("circuit_sim_solve_button"))
        btn_solve.setFixedHeight(40)
        btn_solve.setStyleSheet("background-color: #22b28b; color: white; font-weight: bold;")
        btn_solve.clicked.connect(self.run_simulation)
        
        editor_layout.addWidget(QLabel(loc.get("circuit_sim_netlist_label")))
        editor_layout.addWidget(self.txt_netlist)
        editor_layout.addWidget(btn_solve)
        
        
        result_widget = QWidget()
        result_layout = QVBoxLayout(result_widget)
        result_layout.setContentsMargins(0,0,0,0)
        
        self.table_res = QTableWidget()
        self.table_res.setColumnCount(2)
        self.table_res.setHorizontalHeaderLabels([loc.get("circuit_sim_result_parameter"), loc.get("circuit_sim_result_value")])
        self.table_res.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        self.lbl_status = QLabel(loc.get("circuit_sim_status_ready"))
        self.lbl_status.setStyleSheet("color: gray; font-style: italic;")
        
        result_layout.addWidget(QLabel(loc.get("circuit_sim_results_label")))
        result_layout.addWidget(self.table_res)
        result_layout.addWidget(self.lbl_status)
        
        
        splitter.addWidget(editor_widget)
        splitter.addWidget(result_widget)
        splitter.setSizes([400, 400]) 
        
        main_layout.addWidget(splitter)
        self.setLayout(main_layout)

    def run_simulation(self):
        netlist = self.txt_netlist.toPlainText()
        
        try:
            self.solver.parse_netlist(netlist)
            results, msg = self.solver.solve()
            
            if results is None:
                self.lbl_status.setText(f"{loc.get('circuit_sim_status_error', 'circuit_sim_status_error')}: {msg}")
                self.lbl_status.setStyleSheet("color: red; font-weight: bold;")
                return
            
            self.lbl_status.setText(msg)
            self.lbl_status.setStyleSheet("color: green; font-weight: bold;")
            
            
            self.table_res.setRowCount(0)
            for param, value in results.items():
                row = self.table_res.rowCount()
                self.table_res.insertRow(row)
                
                self.table_res.setItem(row, 0, QTableWidgetItem(param))
                
                
                unit = "V" if param.startswith("V") else "A"
                if abs(value) < 1e-3:
                    val_str = f"{value*1e6:.2f} µ{unit}"
                elif abs(value) < 1:
                    val_str = f"{value*1e3:.2f} m{unit}"
                else:
                    val_str = f"{value:.4f} {unit}"
                    
                self.table_res.setItem(row, 1, QTableWidgetItem(val_str))
                
        except Exception as e:
            self.lbl_status.setText(f"{loc.get('circuit_sim_status_error', 'circuit_sim_status_error')}: {e}")
            self.lbl_status.setStyleSheet("color: red;")