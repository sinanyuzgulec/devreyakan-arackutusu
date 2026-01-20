from .ui import LcdWidget
from core.localization import loc

TOOL_METADATA = {
    "id": "lcd_tool",
    "name": loc.get("lcd_tool_name"),
    "categories": [
        loc.get("cat_electronic"),
        loc.get("cat_simulation"),
        loc.get("cat_analysis"),
    ],
    "widget_class": LcdWidget
}