
def calc_non_inverting(r1, r2, vin):
    
    gain = 1 + (r2 / r1)
    vout = vin * gain
    return vout, gain

def calc_inverting(r1, r2, vin):
    
    gain = -(r2 / r1)
    vout = vin * gain
    return vout, gain
