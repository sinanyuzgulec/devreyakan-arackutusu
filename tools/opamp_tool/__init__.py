from .ui import OpAmpWidget
from core.localization import loc

TOOL_METADATA = {
    "id": "opamp_tool",
    "name": loc.get("opamp_tool_name"),
    "categories": [
        loc.get("cat_electronic"), 
        loc.get("cat_circuit")
    ],
    "widget_class": OpAmpWidget
}