from .ui import StructToolWidget
from core.localization import loc

TOOL_METADATA = {
    "id": "struct_tool",
    "name": loc.get("struct_tool_name"),
    "categories": [
        loc.get("cat_other")
    ],
    "widget_class": StructToolWidget
}