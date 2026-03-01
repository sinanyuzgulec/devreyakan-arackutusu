from .ui import MechanicalResonanceWidget
from core.localization import loc

TOOL_METADATA = {
    "id": "mechanical_resonance_tool",
    "name": loc.get("mechanical_resonance_tool_name"),
    "categories": [
        loc.get("cat_mechanical"),
        loc.get("cat_analysis")
    ],
    "widget_class": MechanicalResonanceWidget
}
