from .ui import CoilWidget
from core.localization import loc

TOOL_METADATA = {
    "id": "coil_tool",
    "name": loc.get("coil_tool_name"),
    "categories": [
        loc.get("cat_amateur_radio"), 
        loc.get("cat_tools")
    ],
    "widget_class": CoilWidget
}
