import math
from dataclasses import dataclass

@dataclass
class I2cPullupResult:
    min_r_ohm: float
    max_r_ohm: float
    recommended_r_ohm: float

def calculate_i2c_pullup(vdd: float, speed_khz: int, bus_cap_pf: float, vol: float = 0.4, iol_ma: float = 3.0) -> I2cPullupResult:
    if vdd <= 0 or bus_cap_pf <= 0 or vol >= vdd or iol_ma <= 0:
        return None
        
    iol_a = iol_ma / 1000.0
    c_b_farad = bus_cap_pf * 1e-12
    
    # R_min = (Vdd - Vol) / Iol
    r_min = (vdd - vol) / iol_a
    
    # Maksimum Yükselme Süresi (t_r) spesifikasyonu:
    # Standard-mode (100kHz): max 1000 ns
    # Fast-mode (400kHz): max 300 ns
    # Fast-mode Plus (1MHz): max 120 ns
    if speed_khz <= 100:
        t_r = 1000e-9
    elif speed_khz <= 400:
        t_r = 300e-9
    else:
        t_r = 120e-9
        
    # R_max = t_r / (0.8473 * C_b)   [I2C spec: 0.3Vdd to 0.7Vdd RC charging constant is ~0.8473]
    r_max = t_r / (0.8473 * c_b_farad)
    
    if r_max < r_min:
        # Kapasitans çok yüksek, sınır aşıldı
        r_rec = r_min
    else:
        r_rec = (r_min + r_max) / 2.0
        
    return I2cPullupResult(
        min_r_ohm=r_min,
        max_r_ohm=r_max,
        recommended_r_ohm=r_rec
    )
