from .ui import RegulatorWidget
from core.localization import loc

TOOL_METADATA = {
    "id": "regulator_tool",
    "name": loc.get("regulator_tool_name"),
    "categories": [
        loc.get("cat_electronic"),
        loc.get("cat_circuit")
    ],
    "widget_class": RegulatorWidget
}