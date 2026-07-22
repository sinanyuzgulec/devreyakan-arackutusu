from .ui import DcDcConverterWidget
from core.localization import loc

TOOL_METADATA = {
    "id": "dcdc_converter_tool",
    "name": loc.get("dcdcwidget_tool_name"),
    "categories": [
        loc.get("cat_electronic"),
        loc.get("cat_circuit")
    ],
    "widget_class": DcDcConverterWidget
}
