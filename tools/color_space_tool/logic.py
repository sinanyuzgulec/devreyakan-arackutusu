import colorsys
from dataclasses import dataclass

@dataclass
class ColorResult:
    r8: int
    g8: int
    b8: int
    hex24: str
    rgb565_hex: str
    rgb565_dec: int
    hsv: tuple
    cmyk: tuple

def calculate_rgb565(r: int, g: int, b: int) -> ColorResult:
    if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
        return None
        
    # RGB565 16-bit paketi: RRRRRGGGGGBBBBB
    r5 = (r >> 3) & 0x1F
    g6 = (g >> 2) & 0x3F
    b5 = (b >> 3) & 0x1F
    
    val565 = (r5 << 11) | (g6 << 5) | b5
    hex565 = f"0x{val565:04X}"
    hex24 = f"#{r:02X}{g:02X}{b:02X}"
    
    # HSV
    hsv = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
    hsv_formatted = (hsv[0]*360.0, hsv[1], hsv[2])
    
    # CMYK
    if (r, g, b) == (0, 0, 0):
        cmyk = (0.0, 0.0, 0.0, 1.0)
    else:
        c = 1.0 - (r / 255.0)
        m = 1.0 - (g / 255.0)
        y = 1.0 - (b / 255.0)
        k = min(c, m, y)
        c = (c - k) / (1.0 - k)
        m = (m - k) / (1.0 - k)
        y = (y - k) / (1.0 - k)
        cmyk = (c, m, y, k)
        
    return ColorResult(
        r8=r, g8=g, b8=b,
        hex24=hex24,
        rgb565_hex=hex565,
        rgb565_dec=val565,
        hsv=hsv_formatted,
        cmyk=cmyk
    )
