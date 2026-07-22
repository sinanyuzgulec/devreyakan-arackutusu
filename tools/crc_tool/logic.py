from dataclasses import dataclass

@dataclass
class CrcResult:
    hex_val: str
    dec_val: int
    bin_val: str

def crc8(data: bytes, poly=0x07, init=0x00) -> int:
    crc = init
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x80:
                crc = ((crc << 1) ^ poly) & 0xFF
            else:
                crc = (crc << 1) & 0xFF
    return crc

def crc16_modbus(data: bytes) -> int:
    crc = 0xFFFF
    for pos in data:
        crc ^= pos
        for _ in range(8):
            if (crc & 0x0001) != 0:
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    return crc

def crc16_ccitt_false(data: bytes) -> int:
    crc = 0xFFFF
    for byte in data:
        crc ^= (byte << 8)
        for _ in range(8):
            if crc & 0x8000:
                crc = ((crc << 1) ^ 0x1021) & 0xFFFF
            else:
                crc = (crc << 1) & 0xFFFF
    return crc

def crc32(data: bytes) -> int:
    import zlib
    return zlib.crc32(data) & 0xFFFFFFFF

def calculate_crc(data: bytes, algorithm: str) -> CrcResult:
    if algorithm == "CRC-8":
        val = crc8(data)
        return CrcResult(f"0x{val:02X}", val, f"{val:08b}")
    elif algorithm == "CRC-16-MODBUS":
        val = crc16_modbus(data)
        return CrcResult(f"0x{val:04X}", val, f"{val:016b}")
    elif algorithm == "CRC-16-CCITT-FALSE":
        val = crc16_ccitt_false(data)
        return CrcResult(f"0x{val:04X}", val, f"{val:016b}")
    elif algorithm == "CRC-32":
        val = crc32(data)
        return CrcResult(f"0x{val:08X}", val, f"{val:032b}")
    return None
