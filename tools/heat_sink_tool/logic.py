from dataclasses import dataclass
from typing import Optional
import math

@dataclass
class HeatSinkResult:
    required_theta: float
    max_case_temp: float

def calculate_heat_sink(power_w: float, ambient_temp: float, max_junction_temp: float, tj_case_resistance: float) -> Optional[HeatSinkResult]:
    """
    Calculates required thermal resistance for heat sink selection.
    
    Args:
        power_w: Power dissipation in Watts
        ambient_temp: Ambient temperature in °C
        max_junction_temp: Maximum junction temperature in °C
        tj_case_resistance: Thermal resistance Tj-Case in °C/W
    
    Returns:
        HeatSinkResult with required thermal resistance and maximum case temperature
    """
    if power_w <= 0 or ambient_temp < -273.15 or max_junction_temp <= ambient_temp:
        return None
    
    # Calculate maximum case temperature
    # Tj = Ta + (Pd * (Rθj-a))
    # Rθj-a = Rθj-c + Rθc-a
    # Rθc-a = (Tj_max - Ta) / Pd - Rθj-c
    
    max_case_temp = max_junction_temp - (power_w * tj_case_resistance)
    
    if max_case_temp <= ambient_temp:
        return None
    
    # Required thermal resistance from case to ambient
    required_theta = (max_case_temp - ambient_temp) / power_w
    
    return HeatSinkResult(required_theta, max_case_temp)
