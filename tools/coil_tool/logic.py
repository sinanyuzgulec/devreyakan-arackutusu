
def calc_air_core(diameter_mm, length_mm, turns):
    try:
        d_in = diameter_mm / 25.4
        l_in = length_mm / 25.4
        n = turns
        
        numerator = (d_in * d_in) * (n * n)
        denominator = (18 * d_in) + (40 * l_in)
        
        inductance_uh = numerator / denominator
        return inductance_uh
    except:
        return 0
