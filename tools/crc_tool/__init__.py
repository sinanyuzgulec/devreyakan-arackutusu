from .ui import CrcWidget
from core.localization import loc

TOOL_METADATA = {
    "id": "crc_tool",
    "name": loc.get("crcwidget_tool_name"),
    "categories": [
        loc.get("cat_data"),
        loc.get("cat_embedded"),
        loc.get("cat_software")
    ],
    "widget_class": CrcWidget
}
