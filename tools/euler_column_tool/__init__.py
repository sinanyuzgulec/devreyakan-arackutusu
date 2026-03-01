from .ui import EulerColumnWidget
from core.localization import loc

TOOL_METADATA = {
    "id": "euler_column_tool",
    "name": loc.get("euler_column_tool_name"),
    "categories": [
        loc.get("cat_mechanical"),
        loc.get("cat_analysis")
    ],
    "widget_class": EulerColumnWidget
}
