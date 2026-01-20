from .ui import PidWidget
from core.localization import loc

TOOL_METADATA = {
    "id": "pid_tool",
    "name": loc.get("pid_tool_name"),
    "categories": [
        loc.get("cat_general"), 
        loc.get("cat_circuit")
    ],
    "widget_class": PidWidget
}

