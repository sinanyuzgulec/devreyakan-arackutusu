from .ui import BatteryToolWidget
from core.localization import loc

TOOL_METADATA = {
    "id": "battery_tool",
    "name": loc.get("batterytoolwidget_tool_name"),
    "categories": [
        loc.get("cat_general"), 
        loc.get("cat_tools"), 
        loc.get("cat_other")
    ],
    "widget_class": BatteryToolWidget
}