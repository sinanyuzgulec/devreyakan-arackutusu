from .ui import I2cPullupWidget
from core.localization import loc

TOOL_METADATA = {
    "id": "i2c_pullup_tool",
    "name": loc.get("i2cwidget_tool_name"),
    "categories": [
        loc.get("cat_embedded"),
        loc.get("cat_circuit")
    ],
    "widget_class": I2cPullupWidget
}
