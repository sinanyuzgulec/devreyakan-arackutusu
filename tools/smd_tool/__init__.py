from .ui import SmdToolWidget
from core.localization import loc

TOOL_METADATA = {
    "id": "smd_tool",
    "name": loc.get("smd_tool_name"),
    "categories": [
        loc.get("cat_electronic"),
        loc.get("cat_circuit")
    ],
    "widget_class": SmdToolWidget
}
