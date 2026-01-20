
def calc_lm317_voltage(r1, r2):
    
    try:
        if r1 == 0: return 0
        return 1.25 * (1 + (r2 / r1))
    except:
        return 0

def calc_lm317_resistor(vout, r1):
    
    try:
        if vout < 1.25: return 0
        return r1 * ((vout / 1.25) - 1)
    except:
        return 0

def calc_power_dissipation(vin, vout, current):
    
    try:
        return (vin - vout) * current
    except:
        return 0
