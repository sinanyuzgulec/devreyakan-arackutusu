from dataclasses import dataclass
from typing import Optional

@dataclass
class LedResult:
    resistor_ohm: float
    resistor_power: float
    actual_current: float

def calculate_led(vs: float, vl: float, il: float, count: int = 1) -> Optional[LedResult]:
    if il <= 0: return None
    total_led_voltage = vl * count
    voltage_drop = vs - total_led_voltage
    
    if voltage_drop < 0:
        return None
        
    resistor = voltage_drop / il
    power = voltage_drop * il
    return LedResult(resistor, power, il)