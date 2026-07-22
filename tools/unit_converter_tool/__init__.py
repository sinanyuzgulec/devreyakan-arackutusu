from .ui import UnitConverterWidget
from core.localization import loc

TOOL_METADATA = {
    "id": "unit_converter_tool",
    "name": loc.get("unitwidget_tool_name"),
    "categories": [
        loc.get("cat_math"),
        loc.get("cat_general"),
        loc.get("cat_electronic")
    ],
    "widget_class": UnitConverterWidget
}
