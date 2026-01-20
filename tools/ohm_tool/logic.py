from dataclasses import dataclass
from typing import Optional
from core.localization import loc

@dataclass
class OhmResult:
    val: float
    unit: str

def calculate_ohm(v: Optional[float] = None, i: Optional[float] = None, 
                  r: Optional[float] = None, p: Optional[float] = None) -> dict:
    results = {}
    if v is None and i is not None and r is not None:
        results['voltage'] = OhmResult(i * r, loc.get("ohm_tool_voltage_unit"))
    if i is None and v is not None and r is not None and r != 0:
        results['current'] = OhmResult(v / r, loc.get("ohm_tool_current_unit"))
    if p is None and v is not None and i is not None:
        results['power'] = OhmResult(v * i, loc.get("ohm_tool_power_unit"))
    return results