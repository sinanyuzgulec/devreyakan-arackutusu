import math

def calc_cutoff_freq(r_ohm, c_farad):
    """f = 1 / (2 * pi * R * C)"""
    try:
        return 1.0 / (2.0 * math.pi * r_ohm * c_farad)
    except:
        return 0

def calc_required_c(r_ohm, f_hz):
    """C = 1 / (2 * pi * R * f)"""
    try:
        return 1.0 / (2.0 * math.pi * r_ohm * f_hz)
    except:
        return 0