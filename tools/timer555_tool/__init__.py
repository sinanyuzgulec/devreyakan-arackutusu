from .ui import Timer555Widget
from core.localization import loc

TOOL_METADATA = {
    "id": "timer555_tool",
    "name": loc.get("timer555_tool_name"),
    "categories": [
        loc.get("cat_electronic")
    ],
    "widget_class": Timer555Widget
}
