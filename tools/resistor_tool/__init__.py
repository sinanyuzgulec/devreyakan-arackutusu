from .ui import ResistorWidget
from core.localization import loc

TOOL_METADATA = {
    "id": "resistor_tool",
    "name": loc.get("resistor_tool_name"),
    "categories": [
        loc.get("cat_electronic"),
        loc.get("cat_circuit")
    ],
    "widget_class": ResistorWidget
}