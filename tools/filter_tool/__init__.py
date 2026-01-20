from .ui import FilterToolWidget
from core.localization import loc

TOOL_METADATA = {
    "id": "filter_tool",
    "name": loc.get("rc_filter_tool_name"),
    "categories": [
        loc.get("cat_amateur_radio"), 
        loc.get("cat_tools"),
        loc.get("cat_electronic")
    ],
    "widget_class": FilterToolWidget
}