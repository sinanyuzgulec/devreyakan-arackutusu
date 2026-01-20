from .ui import LedWidget
from core.localization import loc

TOOL_METADATA = {
    "id": "led_tool",
    "name": loc.get("led_tool_name"),
    "categories": [
        loc.get("cat_electronic"), 
        loc.get("cat_circuit")
    ],
    "widget_class": LedWidget
}