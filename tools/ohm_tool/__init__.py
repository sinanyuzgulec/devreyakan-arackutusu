from .ui import OhmWidget
from core.localization import loc

TOOL_METADATA = {
    "id": "ohm_tool",
    "name": loc.get("ohm_tool_name"),
    "categories": [
        loc.get("cat_electronic"), 
        loc.get("cat_circuit")
    ],
    "widget_class": OhmWidget
}