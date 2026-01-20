from typing import List

def generate_lcd_code(pixels: List[List[int]]) -> dict:
    hex_codes = []
    binary_codes = []
    for row in pixels:
        row_val = 0
        for i, bit in enumerate(row):
            if bit:
                row_val |= (1 << (4 - i))
        hex_codes.append(f"0x{row_val:02X}")
        binary_codes.append(f"B{row_val:05b}")

    all_code = "byte customChar[8] = {\n  " + ", ".join(hex_codes) + "\n};"
    return {"hex": hex_codes, "bin": binary_codes, "code": all_code}