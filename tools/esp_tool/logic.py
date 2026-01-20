import subprocess
import sys
from core.localization import loc

def upload_esp_bin(bin_path, port, baud, chip_type, address):
    cmd = [
        sys.executable, "-m", "esptool",
        "--port", port,
        "--baud", str(baud),
        "--before", "default_reset",
        "--after", "hard_reset",
        "write_flash",
        "-z",
        "--flash_mode", "dio",
        "--flash_freq", "40m",
        "--flash_size", "detect",
        address, bin_path
    ]

    if chip_type and chip_type.lower() != "auto":
        cmd.insert(3, "--chip")
        cmd.insert(4, chip_type.lower())

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        
        header_cmd = "--- COMMAND ---"
        header_out = "--- OUTPUT ---"
        header_err = "--- ERROR / INFO ---"

        log = f"{header_cmd}\n{' '.join(cmd)}\n\n"
        log += f"{header_out}\n{result.stdout}\n"
        
        if result.stderr:
            log += f"{header_err}\n{result.stderr}"

        if result.returncode == 0:
            return True, log
        else:
            if "ModuleNotFoundError" in result.stderr:
                log += f"\n\n{loc.get('esp_tool_uploader_error_esptool_not_found')}"
            elif "Permission denied" in result.stderr:
                log += f"\n\n{loc.get('esp_tool_uploader_hint_permission')}"
            elif "could not open port" in result.stderr:
                log += f"\n\n{loc.get('esp_tool_uploader_hint_port_busy')}"
                
            return False, log

    except Exception as e:
        return False, loc.get("esp_tool_uploader_error_unexpected").format(msg=str(e))