from .ui import PcbToolWidget
from core.localization import loc

TOOL_METADATA = {
    "id": "pcb_tool",
    "name": loc.get("pcb_tool_name"),
    "categories": [
        loc.get("cat_electronic"), 
        loc.get("cat_circuit")
    ],
    "widget_class": PcbToolWidget
}