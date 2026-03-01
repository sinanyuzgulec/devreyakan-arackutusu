from .ui import HeatSinkWidget
from core.localization import loc

TOOL_METADATA = {
    "id": "heat_sink_tool",
    "name": loc.get("heat_sink_tool_name"),
    "categories": [
        loc.get("cat_thermal"),
        loc.get("cat_analysis")
    ],
    "widget_class": HeatSinkWidget
}
