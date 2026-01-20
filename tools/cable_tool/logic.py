AWG_TABLE = {
    "10 AWG (5.26 mm²)": 5.26,
    "12 AWG (3.31 mm²)": 3.31,
    "14 AWG (2.08 mm²)": 2.08,
    "16 AWG (1.31 mm²)": 1.31,
    "18 AWG (0.82 mm²)": 0.82,
    "20 AWG (0.52 mm²)": 0.52,
    "22 AWG (0.33 mm²)": 0.33,
    "24 AWG (0.20 mm²)": 0.20,
    "26 AWG (0.13 mm²)": 0.13,
    "28 AWG (0.08 mm²)": 0.08,
    "0.50 mm²": 0.50,
    "0.75 mm²": 0.75,
    "1.00 mm²": 1.00,
    "1.50 mm²": 1.50,
    "2.50 mm²": 2.50,
    "4.00 mm²": 4.00
}

def calculate_drop(voltage, current, length_m, area_mm2):
    
    rho = 0.0175 
    
    total_length = length_m * 2
    
    resistance = (rho * total_length) / area_mm2
    
    drop_v = current * resistance
    remaining_v = voltage - drop_v
    percent_loss = (drop_v / voltage) * 100
    
    return drop_v, remaining_v, percent_loss