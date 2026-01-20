from PyQt6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QListWidget, QStackedWidget, QLabel, QListWidgetItem)
from PyQt6.QtCore import Qt
from core.updater import UpdateChecker
from gui.widgets.update_bar import UpdateBar
from core.version import CURRENT_VERSION
from core.tool_manager import ToolManager
from gui.settings_page import SettingsPage
from core.localization import loc



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("devreyakan Araç Kutusu (OSE) v {version}".format(version=CURRENT_VERSION))
        self.resize(1000, 600)
        
        
        self.tool_manager = ToolManager()
        self.tool_manager.discover_tools()

        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)

        
        self.sidebar = QListWidget()
        self.sidebar.setFixedWidth(220)
        self.sidebar.setStyleSheet("""
            QListWidget { background-color: #2d2d2d; color: #ddd; font-size: 14px; border: none; outline: none;}
            QListWidget::item { padding: 12px; border-bottom: 1px solid #3d3d3d; }
            QListWidget::item:selected { background-color: #22b28b; color: white; font-weight: bold;}
            QListWidget::item:hover { background-color: #3d3d3d; }
        """)
        main_layout.addWidget(self.sidebar)

        
        self.content_area = QStackedWidget()
        main_layout.addWidget(self.content_area)

        
        
        self.sidebar_items = {} 
        
        self.tool_categories_map = {}

        self.init_system()

    def init_system(self):
        
        self.add_static_page(loc.get("main_page_home"), self.create_home_page())

        
        self.settings_page = SettingsPage(self.tool_manager)
        self.settings_page.filter_changed.connect(self.apply_filter)
        self.add_static_page(loc.get("main_page_settings"), self.settings_page)
        self.load_dynamic_tools()
        self.sidebar.currentRowChanged.connect(self.content_area.setCurrentIndex)
        self.sidebar.setCurrentRow(0)

    def create_home_page(self):
        label = QLabel(loc.get("main_page_welcome_message").format(version=CURRENT_VERSION))
        label.setStyleSheet("font-size: 18px; color: #777; padding: 20px;")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return label

    def add_static_page(self, name, widget):
        item = QListWidgetItem(name)
        self.sidebar.addItem(item)
        self.content_area.addWidget(widget)

    

    def load_dynamic_tools(self):
        sorted_ids = sorted(self.tool_manager.loaded_tools.keys(), key=lambda x: self.tool_manager.loaded_tools[x]['name'])

        for tool_id in sorted_ids:
            meta = self.tool_manager.loaded_tools[tool_id]
            widget_instance = self.tool_manager.get_tool_instance(tool_id)
            
            if widget_instance:                
                display_name = meta['name']
                if meta.get('verified', False):
                    display_name = f"✓ {display_name}" 
                else:  
                    display_name = f"* {display_name}" 
                item = QListWidgetItem(display_name)
                if meta.get('verified', False):
                    item.setForeground(Qt.GlobalColor.white) 
                else:
                    item.setForeground(Qt.GlobalColor.yellow)
                    item.setToolTip(loc.get("main_page_unverified_tooltip"))

                self.sidebar.addItem(item)
                self.content_area.addWidget(widget_instance)
                
                self.sidebar_items[tool_id] = item
                self.tool_categories_map[tool_id] = set(meta.get('categories', []))

    def apply_filter(self, selected_categories):       
        for tool_id, item in self.sidebar_items.items():
            tool_cats = self.tool_categories_map.get(tool_id, set())
            
            
            
            if not selected_categories or tool_cats.intersection(selected_categories):
                item.setHidden(False)
            else:
                item.setHidden(True)
    def check_updates(self):
        self.updater = UpdateChecker()
        self.updater.update_available.connect(self.on_update_found)
        self.updater.start()

    def on_update_found(self, new_version, url):
        
        is_modified = False
        for tool in self.tool_manager.loaded_tools.values():
            if not tool.get('verified', True):
                is_modified = True
                break
        
        self.update_bar.show_update(new_version, url, is_modified)
