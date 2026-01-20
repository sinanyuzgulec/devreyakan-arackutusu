

def calculate_battery_life(capacity_mah, sleep_ua, active_ma, duration_sec, interval_min):
    """
    IoT cihazının pil ömrünü detaylı hesaplar.
    Dönüş: (yıl, ay, gün, saat, dakika)
    """
    try:
        
        total_cycle_sec = interval_min * 60
        active_sec = duration_sec
        sleep_sec = total_cycle_sec - active_sec
        
        if sleep_sec < 0: return 0, 0, 0, 0, 0
        
        
        current_active_a = active_ma / 1000.0
        current_sleep_a = sleep_ua / 1_000_000.0
        
        
        avg_current_a = ((current_active_a * active_sec) + (current_sleep_a * sleep_sec)) / total_cycle_sec
        
        if avg_current_a == 0: return 0, 0, 0, 0, 0

        
        battery_ah = (capacity_mah / 1000.0) * 0.85
        
        
        total_hours = battery_ah / avg_current_a
        
        
        
        years = int(total_hours // 8760)
        remaining_hours = total_hours % 8760
        
        
        months = int(remaining_hours // 720)
        remaining_hours = remaining_hours % 720
        
        
        days = int(remaining_hours // 24)
        remaining_hours = remaining_hours % 24
        
        
        hours = int(remaining_hours)
        minutes = int((remaining_hours - hours) * 60)
        
        return years, months, days, hours, minutes
        
    except (ZeroDivisionError, ValueError):
        return 0, 0, 0, 0, 0