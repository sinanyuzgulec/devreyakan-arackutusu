from .ui import StructBitToolWidget
from core.localization import loc

TOOL_METADATA = {
    "id": "bit_tool",
    "name": loc.get("structbittoolwidget_tool_name"),
    "categories": [
        loc.get("cat_software"), 
        loc.get("cat_embedded"), 
        loc.get("cat_analysis")
    ],
    "widget_class": StructBitToolWidget
}