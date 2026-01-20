import math


def calculate_trace_width(current_amps, temp_rise_c, thickness_oz, layer="external"):

    
    if layer == "internal":
        k, b, c = 0.024, 0.44, 0.725
    else: 
        k, b, c = 0.048, 0.44, 0.725

    
    thickness_mil = thickness_oz * 1.378

    
    try:
        area_mils2 = (current_amps / (k * (temp_rise_c ** b))) ** (1 / c)
        
        
        width_mil = area_mils2 / thickness_mil
        width_mm = width_mil * 0.0254
        
        return width_mil, width_mm
    except:
        return 0, 0