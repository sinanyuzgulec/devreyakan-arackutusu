from .ui import AdcWidget
from core.localization import loc

TOOL_METADATA = {
    "id": "adc_tool",
    "name": loc.get("adcwidget_tool_name"),
    "categories": [
        loc.get("cat_embedded"), 
        loc.get("cat_data"), 
        loc.get("cat_sensor")
    ],
    "widget_class": AdcWidget
}