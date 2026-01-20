from .ui import EspUploaderWidget
from core.localization import loc

TOOL_METADATA = {
    "id": "esp_tool",
    "name": "ESP Flash Tool", # İsterseniz loc.get("esp_tool_name") yapabilirsiniz
    "categories": [
        loc.get("cat_embedded"),
    ],
    "widget_class": EspUploaderWidget
}