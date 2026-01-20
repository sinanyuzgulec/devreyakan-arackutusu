
import zlib
import hashlib

def calculate_checksums(data_bytes):
    """
    Byte array alır, hesaplanmış checksum sonuçlarını sözlük olarak döner.
    """
    results = {}
    
    
    results['CRC-32'] = f"{zlib.crc32(data_bytes) & 0xFFFFFFFF:08X}"
    
    
    results['MD5'] = hashlib.md5(data_bytes).hexdigest().upper()
    
    
    results['SHA-256'] = hashlib.sha256(data_bytes).hexdigest().upper()
    
    
    results['CRC-16 (Modbus)'] = calc_crc16_modbus(data_bytes)
    
    
    results['Sum (8-bit)'] = f"{sum(data_bytes) & 0xFF:02X}"
    
    return results

def calc_crc16_modbus(data):
    """Standart Modbus CRC-16 Hesaplaması"""
    crc = 0xFFFF
    for pos in data:
        crc ^= pos
        for _ in range(8):
            if (crc & 1) != 0:
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    
    
    
    return f"{crc:04X}"