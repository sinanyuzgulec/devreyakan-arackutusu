import os
import json
from core.integrity import IntegrityManager

def generate():
    checker = IntegrityManager()
    signatures = {}
    
    tools_dir = "tools"
    
    print("--- İmzalar Oluşturuluyor ---")
    
    for folder in os.listdir(tools_dir):
        path = os.path.join(tools_dir, folder)
        if os.path.isdir(path) and not folder.startswith("__"):
            
            tool_id = folder 
            
            
            tool_hash = checker.calculate_tool_hash(path)
            signatures[tool_id] = tool_hash
            print(f"[OK] {tool_id}: {tool_hash[:10]}...")

    with open("signatures.json", "w", encoding="utf-8") as f:
        json.dump(signatures, f, indent=4)
        
    print(f"\n[BAŞARILI] signatures.json dosyasına {len(signatures)} imza kaydedildi.")

if __name__ == "__main__":
    generate()