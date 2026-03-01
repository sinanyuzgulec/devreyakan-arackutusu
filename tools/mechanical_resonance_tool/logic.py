from dataclasses import dataclass
from typing import Optional
import math

@dataclass
class ResonanceResult:
    natural_frequency: float
    damped_frequency: float
    quality_factor: float

def calculate_resonance(mass: float, stiffness: float, damping_ratio: float) -> Optional[ResonanceResult]:
    """
    Calculates mechanical resonance parameters.
    
    Args:
        mass: Mass in kg
        stiffness: Stiffness coefficient in N/m
        damping_ratio: Damping factor (ζ) - between 0 and 1 for underdamped
    
    Returns:
        ResonanceResult with natural frequency, damped frequency, and quality factor
    """
    if mass <= 0 or stiffness <= 0 or damping_ratio < 0:
        return None
    
    # Natural angular frequency (ωn = sqrt(k/m))
    omega_n = math.sqrt(stiffness / mass)
    
    # Natural frequency in Hz (fn = ωn / 2π)
    natural_freq_hz = omega_n / (2 * math.pi)
    
    # Damped angular frequency (ωd = ωn * sqrt(1 - ζ²))
    if damping_ratio >= 1:
        # Overdamped case
        damped_freq_hz = 0.0
    else:
        omega_d = omega_n * math.sqrt(1 - damping_ratio ** 2)
        damped_freq_hz = omega_d / (2 * math.pi)
    
    # Quality factor (Q = 1 / (2ζ))
    if damping_ratio > 0:
        quality_factor = 1 / (2 * damping_ratio)
    else:
        quality_factor = float('inf')
    
    return ResonanceResult(natural_freq_hz, damped_freq_hz, min(quality_factor, 9999))
