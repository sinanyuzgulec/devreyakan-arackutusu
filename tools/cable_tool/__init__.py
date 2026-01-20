from .ui import CableToolWidget
from core.localization import loc

TOOL_METADATA = {
    "id": "cable_tool",
    "name": loc.get("cabletoolwidget_name"),
    "categories": [
        loc.get("cat_general")
    ],
    "widget_class": CableToolWidget
}