from dataclasses import dataclass
from typing import Optional

@dataclass
class GearRatioResult:
    gear_ratio: float
    output_speed: float
    output_torque: float
    power_loss: float

def calculate_gear_ratio(input_speed: float, input_torque: float, teeth_input: int, teeth_output: int, efficiency: float) -> Optional[GearRatioResult]:
    """
    Calculates gear ratio and output parameters.
    
    Args:
        input_speed: Input speed in rpm
        input_torque: Input torque in Nm
        teeth_input: Input gear teeth count
        teeth_output: Output gear teeth count
        efficiency: Gearbox efficiency in percent (0-100)
    
    Returns:
        GearRatioResult with gear ratio, output speed, torque, and power loss
    """
    if input_speed <= 0 or input_torque < 0 or teeth_input <= 0 or teeth_output <= 0 or efficiency < 0 or efficiency > 100:
        return None
    
    # Gear ratio
    gear_ratio = teeth_output / teeth_input
    
    # Output speed (inverted ratio due to speed reduction/increase)
    output_speed = input_speed / gear_ratio
    
    # Output torque (ideal: T_out = T_in * gear_ratio)
    ideal_output_torque = input_torque * gear_ratio
    
    # Actual output torque considering efficiency
    efficiency_factor = efficiency / 100
    output_torque = ideal_output_torque * efficiency_factor
    
    # Input power
    input_power = (input_speed / 60) * input_torque * 2 * 3.14159265359  # Convert rpm to rad/s
    
    # Output power (with losses)
    output_power = (output_speed / 60) * output_torque * 2 * 3.14159265359
    
    # Power loss (Watts)
    power_loss = input_power - output_power
    
    return GearRatioResult(gear_ratio, output_speed, output_torque, power_loss)
