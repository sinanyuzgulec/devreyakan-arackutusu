import math

def calculate_ntc_temp(r_measured, beta, r25=10000, t25_c=25.0):
    try:
        t0_k = t25_c + 273.15
        inv_t = (1.0 / t0_k) + (1.0 / beta) * math.log(r_measured / r25)
        
        temp_k = 1.0 / inv_t
        temp_c = temp_k - 273.15
        
        return temp_c
    except:
        return None