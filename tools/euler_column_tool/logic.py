from dataclasses import dataclass
from typing import Optional
import math

@dataclass
class EulerColumnResult:
    critical_load: float
    effective_length: float
    slenderness_ratio: float

def calculate_euler_column(modulus_e: float, inertia_i: float, length_l: float, k: float) -> Optional[EulerColumnResult]:
    """
    Calculates Euler critical load for column buckling.
    
    Args:
        modulus_e: Modulus of elasticity in Pa
        inertia_i: Moment of inertia in m⁴
        length_l: Column length in m
        k: End condition factor (0.5, 0.7, 1, 2)
    
    Returns:
        EulerColumnResult with critical load, effective length, and slenderness ratio
    """
    if modulus_e <= 0 or inertia_i <= 0 or length_l <= 0 or k <= 0:
        return None
    
    # Effective length
    le = k * length_l
    
    # Equivalent radius of gyration (r = sqrt(I/A))
    # For simplicity, we use radius directly
    if inertia_i <= 0:
        return None
    
    # Euler formula: Pcr = (π² * E * I) / (Le)²
    critical_load = (math.pi ** 2 * modulus_e * inertia_i) / (le ** 2)
    
    # Slenderness ratio (L/r)
    # Approximated as L²/I (normalized slenderness)
    slenderness_ratio = le / math.sqrt(inertia_i) if inertia_i > 0 else 0
    
    return EulerColumnResult(critical_load, le, slenderness_ratio)

def get_k_factor(condition_str: str) -> Optional[float]:
    """Returns K factor based on end condition string"""
    conditions = {
        "pinned": 1.0,
        "fixed": 0.5,
        "fixed_free": 2.0,
        "fixed_pinned": 0.7
    }
    return conditions.get(condition_str)
