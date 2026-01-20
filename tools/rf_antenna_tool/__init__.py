from .ui import RfAntennaWidget
from core.localization import loc

TOOL_METADATA = {
    "id": "rf_antenna_tool",
    "name": loc.get("rf_antenna_tool_name"),
    "categories": [
        loc.get("cat_amateur_radio")
    ],
    "widget_class": RfAntennaWidget
}