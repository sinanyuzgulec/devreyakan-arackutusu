import math

# Dönüşüm Oranları (Standart SI birimine göre çarpan)
CATEGORIES = {
    "Güç / RF (Power & RF)": {
        "W": lambda val, to: val if to == "W" else (10 * math.log10(val * 1000) if to == "dBm" else val * 1000),
        "mW": lambda val, to: val / 1000 if to == "W" else (10 * math.log10(val) if to == "dBm" else val),
        "dBm": lambda val, to: (10 ** (val / 10)) / 1000 if to == "W" else (10 ** (val / 10) if to == "mW" else val)
    },
    "Frekans (Frequency)": {
        "Hz": 1.0,
        "kHz": 1e3,
        "MHz": 1e6,
        "GHz": 1e9
    },
    "Sıcaklık (Temperature)": {
        "Celsius (°C)": "C",
        "Fahrenheit (°F)": "F",
        "Kelvin (K)": "K"
    },
    "Uzunluk / Mesafe": {
        "mm": 0.001,
        "cm": 0.01,
        "m": 1.0,
        "inch": 0.0254,
        "mil": 0.0000254
    },
    "Kapasitans": {
        "pF": 1e-12,
        "nF": 1e-9,
        "uF": 1e-6,
        "mF": 1e-3,
        "F": 1.0
    },
    "Endüktans": {
        "nH": 1e-9,
        "uH": 1e-6,
        "mH": 1e-3,
        "H": 1.0
    }
}

def convert_unit(value: float, category: str, from_unit: str, to_unit: str) -> float:
    if category not in CATEGORIES:
        return None
        
    cat_data = CATEGORIES[category]
    
    # Sıcaklık özel durumu
    if category == "Sıcaklık (Temperature)":
        # Kelvin'e çevir
        if from_unit.startswith("Celsius"): k = value + 273.15
        elif from_unit.startswith("Fahrenheit"): k = (value - 32) * 5/9 + 273.15
        else: k = value
        
        # Hedefe çevir
        if to_unit.startswith("Celsius"): return k - 273.15
        elif to_unit.startswith("Fahrenheit"): return (k - 273.15) * 9/5 + 32
        else: return k
        
    # Power / RF özel durumu
    if category.startswith("Güç"):
        func = cat_data.get(from_unit)
        if callable(func):
            return func(value, to_unit)
        return value
        
    # Standart SI çarpanı ile hesaplama
    factor_from = cat_data.get(from_unit, 1.0)
    factor_to = cat_data.get(to_unit, 1.0)
    
    base_val = value * factor_from
    return base_val / factor_to
