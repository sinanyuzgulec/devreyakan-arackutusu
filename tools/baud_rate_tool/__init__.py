from .ui import BaudRateWidget
from core.localization import loc

TOOL_METADATA = {
    "id": "baud_rate_tool",
    "name": loc.get("baudwidget_tool_name"),
    "categories": [
        loc.get("cat_embedded"),
        loc.get("cat_software"),
        loc.get("cat_analysis")
    ],
    "widget_class": BaudRateWidget
}
