from .ui import UploaderWidget
from core.localization import loc

TOOL_METADATA = {
    "id": "uploader_tool",
    "name": loc.get("hex_uploader_tool_name"),
    "categories": [
        loc.get("cat_embedded"),
    ],
    "widget_class": UploaderWidget
}