from dataclasses import dataclass

@dataclass
class DcDcResult:
    duty_cycle: float
    inductance_uh: float
    peak_current_a: float
    min_capacitance_uf: float

def calculate_dcdc(mode: str, vin: float, vout: float, iout: float, fsw: float, ripple_percent: float = 30.0) -> DcDcResult:
    if vin <= 0 or vout <= 0 or iout <= 0 or fsw <= 0 or ripple_percent <= 0:
        return None
        
    if mode == "Buck":
        if vout >= vin:
            return None # Buck için Vin > Vout olmalı
        duty = vout / vin
        delta_i = iout * (ripple_percent / 100.0)
        # L = (Vin - Vout) * Duty / (fsw * Delta_I)
        l_h = ((vin - vout) * duty) / (fsw * delta_i)
        peak_i = iout + (delta_i / 2.0)
        # C_min = Delta_I / (8 * fsw * Delta_Vout), %1 ripple kabul edilirse
        delta_v = vout * 0.01
        c_f = delta_i / (8 * fsw * delta_v)
        
    elif mode == "Boost":
        if vout <= vin:
            return None # Boost için Vout > Vin olmalı
        duty = 1.0 - (vin / vout)
        iin = iout / (1.0 - duty)
        delta_i = iin * (ripple_percent / 100.0)
        # L = Vin * Duty / (fsw * Delta_I)
        l_h = (vin * duty) / (fsw * delta_i)
        peak_i = iin + (delta_i / 2.0)
        # C_min = Iout * Duty / (fsw * Delta_Vout)
        delta_v = vout * 0.01
        c_f = (iout * duty) / (fsw * delta_v)
    else:
        return None
        
    return DcDcResult(
        duty_cycle=duty,
        inductance_uh=l_h * 1e6,
        peak_current_a=peak_i,
        min_capacitance_uf=c_f * 1e6
    )
