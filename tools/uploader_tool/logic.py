import subprocess
from .boards import BOARD_PRESETS  
from core.localization import loc

def upload_hex(hex_path, port, board_name):

    if board_name not in BOARD_PRESETS:
        return False, loc.get("uploader_error_unknown_board")

    cfg = BOARD_PRESETS[board_name]
    
    cmd = [
        "avrdude",
        "-v",
        "-p", cfg["mcu"],
        "-c", cfg["programmer"],
        "-P", port,
        "-b", cfg["baud"],
        "-D",
        "-U", f"flash:w:{hex_path}:i"
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        
        # Log Başlıklarını Çek
        header_cmd = loc.get("uploader_log_header_cmd")
        header_out = loc.get("uploader_log_header_out")
        header_err = loc.get("uploader_log_header_err")

        # Logu Oluştur
        log = f"{header_cmd}\n{' '.join(cmd)}\n\n"
        log += f"{header_out}\n{result.stdout}\n"
        log += f"{header_err}\n{result.stderr}"

        if result.returncode == 0:
            return True, log
        else:
            # Hata İpuçları
            if "Permission denied" in result.stderr:
                log += f"\n\n{loc.get('uploader_hint_permission')}"
            
            if "programmer is not responding" in result.stderr:
                log += f"\n\n{loc.get('uploader_hint_not_responding')}"
            
            if "ser_open" in result.stderr:
                log += f"\n\n{loc.get('uploader_hint_port_busy')}"
                
            return False, log

    except FileNotFoundError:
        return False, loc.get("uploader_error_avrdude_not_found")
        
    except Exception as e:
        return False, loc.get("uploader_error_unexpected").format(msg=str(e))