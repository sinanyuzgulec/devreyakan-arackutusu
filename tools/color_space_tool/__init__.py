from .ui import ColorSpaceWidget
from core.localization import loc

TOOL_METADATA = {
    "id": "color_space_tool",
    "name": loc.get("colorwidget_tool_name"),
    "categories": [
        loc.get("cat_data"),
        loc.get("cat_embedded"),
        loc.get("cat_software")
    ],
    "widget_class": ColorSpaceWidget
}
