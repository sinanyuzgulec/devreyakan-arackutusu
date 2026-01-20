import os

PINOUT_DIR = os.path.join("resources", "pinouts")

PINOUT_MAP = {
    "Uno": "uno.png",
    "Nano": "nano.png",
    "Mega": "mega.png",
    "Pro Mini": "promini.png",
    "Leonardo": "leonardo.png",
    "Micro": "micro.png",
    "LilyPad": "lilypad.png",
    "Sanguino": "sanguino.png"
}

def get_pinout_path(board_name):

    if not os.path.exists(PINOUT_DIR):
        return None

    
    filename = None
    for key, val in PINOUT_MAP.items():
        if key.lower() in board_name.lower():
            filename = val
            break
    
    if filename:
        full_path = os.path.join(PINOUT_DIR, filename)
        if os.path.exists(full_path):
            return full_path
            
    return None