import math

RESISTOR_DATA = {
    "Black":  (0, 1e0,  None, 250, "#000000"),
    "Brown":  (1, 1e1,  1.0,  100, "#8B4513"),
    "Red":    (2, 1e2,  2.0,  50,  "#FF0000"),
    "Orange": (3, 1e3,  None, 15,  "#FF8C00"),
    "Yellow": (4, 1e4,  None, 25,  "#FFFF00"),
    "Green":  (5, 1e5,  0.5,  20,  "#008000"),
    "Blue":   (6, 1e6,  0.25, 10,  "#0000FF"),
    "Violet": (7, 1e7,  0.1,  5,   "#EE82EE"),
    "Grey":   (8, 1e8,  0.05, 1,   "#808080"),
    "White":  (9, 1e9,  None, None,"#FFFFFF"),
    "Gold":   (None, 0.1,  5.0,  None, "#FFD700"),
    "Silver": (None, 0.01, 10.0, None, "#C0C0C0"),
}

COLOR_LIST = list(RESISTOR_DATA.keys())

def calculate_value_from_colors(bands):

    num = len(bands)
    if num not in [4, 5, 6]: return None

    
    digits = []
    multiplier = 1
    tolerance = 20 
    ppm = None

    try:
        if num == 4:
            
            digits.append(RESISTOR_DATA[bands[0]][0])
            digits.append(RESISTOR_DATA[bands[1]][0])
            multiplier = RESISTOR_DATA[bands[2]][1]
            if bands[3]: tolerance = RESISTOR_DATA[bands[3]][2]

        elif num in [5, 6]:
            
            digits.append(RESISTOR_DATA[bands[0]][0])
            digits.append(RESISTOR_DATA[bands[1]][0])
            digits.append(RESISTOR_DATA[bands[2]][0])
            multiplier = RESISTOR_DATA[bands[3]][1]
            if bands[4]: tolerance = RESISTOR_DATA[bands[4]][2]
            
            if num == 6:
                ppm = RESISTOR_DATA[bands[5]][3]

        
        val_num = int("".join(map(str, digits)))
        total_ohm = val_num * multiplier
        
        return total_ohm, tolerance, ppm
        
    except:
        return None

def calculate_colors_from_value(ohm_val, num_bands):

    if ohm_val == 0: return ["Black"] * num_bands
    
    
    
    exponent = int(math.log10(ohm_val))
    
    
    
    
    if num_bands == 4:
        
        
        
        
        val_str = f"{float(ohm_val):.2e}" 
        base, pwr = val_str.split('e')
        pwr = int(pwr)
        
        
        base = float(base)
        d1 = int(base) 
        d2 = int((base * 10) % 10) 
        
        
        
        
        multiplier_idx = pwr - 1
        
        
        if multiplier_idx == -1: multiplier_color = "Gold"
        elif multiplier_idx == -2: multiplier_color = "Silver"
        else: multiplier_color = get_color_by_multiplier_pow(multiplier_idx)
            
        return [
            get_color_by_digit(d1),
            get_color_by_digit(d2),
            multiplier_color,
            "Gold" 
        ]

    else: 
        
        val_str = f"{float(ohm_val):.3e}"
        base, pwr = val_str.split('e')
        pwr = int(pwr)
        
        base = float(base)
        d1 = int(base)
        d2 = int((base * 10) % 10)
        d3 = int((base * 100) % 10)
        
        multiplier_idx = pwr - 2
        
        if multiplier_idx == -1: multiplier_color = "Gold"
        elif multiplier_idx == -2: multiplier_color = "Silver"
        else: multiplier_color = get_color_by_multiplier_pow(multiplier_idx)
            
        res = [
            get_color_by_digit(d1),
            get_color_by_digit(d2),
            get_color_by_digit(d3),
            multiplier_color,
            "Brown" 
        ]
        if num_bands == 6:
            res.append("Red") 
        return res

def get_color_by_digit(d):
    for k, v in RESISTOR_DATA.items():
        if v[0] == d: return k
    return "Black"

def get_color_by_multiplier_pow(p):
    
    target = pow(10, p)
    for k, v in RESISTOR_DATA.items():
        if v[1] == target: return k
    return "Black"