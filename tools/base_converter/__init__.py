from .ui import BaseConverterWidget
from core.localization import loc

TOOL_METADATA = {
    "id": "base_converter",
    "name": loc.get("baseconverterwidget_tool_name"),
    "categories": [
        loc.get("cat_general"), 
        loc.get("cat_tools"), 
        loc.get("cat_other")
    ],
    "widget_class": BaseConverterWidget
}