from .ui import SystemWidget
from core.localization import loc

TOOL_METADATA = {
    "id": "system_tool",
    "name": loc.get("system_tool_name"),
    "categories": [
        loc.get("cat_general"),
    ],
    "widget_class": SystemWidget
}