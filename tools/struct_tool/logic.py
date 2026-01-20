import struct
from core.localization import loc

def analyze_struct_format(fmt_str):
    
    try:
        size = struct.calcsize(fmt_str)                     
        dummy_data = []
        clean_fmt = fmt_str.replace('<','').replace('>','').replace('!','').replace('@','')
        
        for char in clean_fmt:
            if char in 'cbB?': dummy_data.append(1)
            elif char in 'hHiIlLqQ': dummy_data.append(1)
            elif char in 'fd': dummy_data.append(1.0)
            elif char == 's': dummy_data.append(b' ')
            
            


        return size, loc.get("struct_tool_valid_format")
    except Exception as e:
        return 0, str(e)

def get_format_help():
    return {
        'x': 'Pad byte',
        'c': 'char (1)',
        'b': 'signed char (1)',
        'B': 'unsigned char (1)',
        'h': 'short (2)',
        'H': 'unsigned short (2)',
        'i': 'int (4)',
        'I': 'unsigned int (4)',
        'f': 'float (4)',
        'd': 'double (8)',
        '<': 'Little Endian',
        '>': 'Big Endian'
    }
