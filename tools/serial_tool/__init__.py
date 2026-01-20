from .ui import SerialWidget
from core.localization import loc

TOOL_METADATA = {
    "id": "serial_tool",
    "name": loc.get("serial_tool_name"),
    "categories": [
        loc.get("cat_electronic"),
        loc.get("cat_embedded"),
    ],
    "widget_class": SerialWidget
}