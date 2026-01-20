
import struct

def int_to_formats(val):
    return {
        'dec': str(val),
        'hex': f"{val:X}",
        'bin': f"{val:b}",
        'oct': f"{val:o}"
    }

def float_to_hex(val):
    try:
        
        return struct.pack('>f', val).hex().upper()
    except:
        return "Error"

def hex_to_float(hex_str):
    try:
        
        clean_hex = hex_str.replace('0x', '').replace(' ', '')
        if len(clean_hex) != 8: return None
        
        
        return struct.unpack('>f', bytes.fromhex(clean_hex))[0]
    except:
        return None