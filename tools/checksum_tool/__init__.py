from .ui import ChecksumToolWidget
from core.localization import loc

TOOL_METADATA = {
    "id": "checksum_tool",
    "name": loc.get("checksumtoolwidget_name"),
    "categories": [
        loc.get("cat_general"),
        loc.get("cat_software"),
    ],
    "widget_class": ChecksumToolWidget
}