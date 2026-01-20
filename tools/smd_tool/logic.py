
from .data import EIA96_TABLE, EIA96_MULTIPLIERS
from core.localization import loc

def calculate_smd_code(code_str):

    code = code_str.strip().upper()
    if not code: return None, "", ""
    
    
    if 'R' in code:
        try:
            val = float(code.replace('R', '.'))
            
            fmt_val, fmt_unit = format_resistor(val)
            return fmt_val, fmt_unit, loc.get("smd_tool_decimal_notation")
        except:
            pass

    
    
    if code.isdigit():
        if len(code) in [3, 4]:
            try:
                base = int(code[:-1])
                multiplier = int(code[-1])
                val = base * (10 ** multiplier)
                
                algo_name = loc.get("smd_tool_3_digit_standard") if len(code)==3 else loc.get("smd_tool_4_digit_precise")
                
                
                fmt_val, fmt_unit = format_resistor(val)
                return fmt_val, fmt_unit, algo_name
            except:
                pass
            
    
    
    if len(code) == 3:
        digits = code[:2]
        letter = code[2]
        
        if digits in EIA96_TABLE and letter in EIA96_MULTIPLIERS:
            base_val = EIA96_TABLE[digits]
            mult_val = EIA96_MULTIPLIERS[letter]
            val = base_val * mult_val
            
            
            fmt_val, fmt_unit = format_resistor(val)
            return fmt_val, fmt_unit, loc.get("smd_tool_eia96_standard")

    return None, loc.get("smd_tool_format_not_recognized"), loc.get("smd_tool_invalid_code")

def format_resistor(val):
    if val >= 1e6:
        return val / 1e6, "MΩ"
    elif val >= 1e3:
        return val / 1e3, "kΩ"
    else:
        return val, "Ω"