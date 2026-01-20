from dataclasses import dataclass

@dataclass
class AdcResult:
    digital_val: int
    binary_str: str
    resolution_step: float

def calculate_adc(bit_depth: int, v_ref: float, v_in: float) -> AdcResult:
    """bit_depth (n), Vref, Vin -> AdcResult"""
    if v_ref == 0: return None
    
    max_steps = (2 ** bit_depth) - 1
    
    raw_val = (v_in / v_ref) * max_steps
    digital_val = int(round(raw_val))
    
    digital_val = max(0, min(digital_val, max_steps))
    
    binary_str = format(digital_val, f'0{bit_depth}b')
    
    step_voltage = v_ref / max_steps
    
    return AdcResult(digital_val, binary_str, step_voltage)