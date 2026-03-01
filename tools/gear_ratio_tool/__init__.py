from .ui import GearRatioWidget
from core.localization import loc

TOOL_METADATA = {
    "id": "gear_ratio_tool",
    "name": loc.get("gear_ratio_tool_name"),
    "categories": [
        loc.get("cat_mechanical"),
        loc.get("cat_analysis")
    ],
    "widget_class": GearRatioWidget
}
