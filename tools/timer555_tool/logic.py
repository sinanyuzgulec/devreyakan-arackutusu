from dataclasses import dataclass
from core.localization import loc

@dataclass
class AstableResult:
    freq: float         
    period: float       
    high_time: float    
    low_time: float     
    duty_cycle: float   

def calc_555_monostable(r: float, c: float) -> float:
    return 1.1 * r * c

def calc_555_astable(r1: float, r2: float, c: float) -> AstableResult: 
    th = 0.693 * (r1 + r2) * c
    tl = 0.693 * r2 * c
    period = th + tl
    freq = 1 / period if period > 0 else 0
    duty = (th / period * 100) if period > 0 else 0
    
    return AstableResult(freq, period, th, tl, duty)