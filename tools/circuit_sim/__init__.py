from .ui import CircuitSimWidget
from core.localization import loc

TOOL_METADATA = {
    "id": "circuit_sim",
    "name": loc.get("circuit_sim_name"),
    "categories": [
        loc.get("cat_electronic"),
        loc.get("cat_simulation"),
        loc.get("cat_analysis"),
    ],
    "widget_class": CircuitSimWidget
}