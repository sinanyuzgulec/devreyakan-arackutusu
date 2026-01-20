from .ui import QthToolWidget
from core.localization import loc

TOOL_METADATA = {
    "id": "qth_tool",
    "name": loc.get("qth_tool_name"),
    "categories": [
        loc.get("cat_amateur_radio")
    ],
    "widget_class": QthToolWidget
}