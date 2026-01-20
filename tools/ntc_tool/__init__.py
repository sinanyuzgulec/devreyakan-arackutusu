from .ui import NtcToolWidget
from core.localization import loc

TOOL_METADATA = {
    "id": "ntc_tool",
    "name": loc.get("ntc_tool_name"),
    "categories": [
        loc.get("cat_electronic"), 
        loc.get("cat_circuit")
    ],
    "widget_class": NtcToolWidget
}