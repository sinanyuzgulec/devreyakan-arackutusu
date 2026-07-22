from dataclasses import dataclass

@dataclass
class BaudRateResult:
    target_baud: float
    actual_baud: float
    divider_ubrr: int
    error_percent: float
    status_message: str

def calculate_baud_rate_error(clock_hz: float, target_baud: float, oversampling: int = 16) -> BaudRateResult:
    """
    Mikrodenetleyici sistem saati ve hedef baud rate'e göre
    bölücü (UBRR) değerini ve frekans sapma/hata yüzdesini hesaplar.
    """
    if clock_hz <= 0 or target_baud <= 0 or oversampling <= 0:
        return None

    # UBRR = (F_CPU / (Oversampling * TargetBaud)) - 1
    exact_ubrr = (clock_hz / (oversampling * target_baud)) - 1
    divider_ubrr = round(exact_ubrr)
    
    if divider_ubrr < 0:
        divider_ubrr = 0

    # Gerçekleşen Baud Rate = F_CPU / (Oversampling * (UBRR + 1))
    actual_baud = clock_hz / (oversampling * (divider_ubrr + 1))

    # Hata Yüzdesi = ((ActualBaud - TargetBaud) / TargetBaud) * 100
    error_percent = ((actual_baud - target_baud) / target_baud) * 100.0

    if abs(error_percent) <= 2.0:
        status_msg = "Güvenilir iletişim (Hata <%2)"
    elif abs(error_percent) <= 3.5:
        status_msg = "Kritik / Tolerans sınırında (%2 - %3.5)"
    else:
        status_msg = "Yüksek Hata! İletişim kopabilir (>%3.5)"

    return BaudRateResult(
        target_baud=target_baud,
        actual_baud=actual_baud,
        divider_ubrr=divider_ubrr,
        error_percent=error_percent,
        status_message=status_msg
    )
