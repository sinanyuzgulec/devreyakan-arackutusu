import os
import json
import hashlib

SIGNATURE_FILE = "signatures.json"

class IntegrityManager:
    def __init__(self):
        self.signatures = self._load_signatures()

    def _load_signatures(self):
        if os.path.exists(SIGNATURE_FILE):
            try:
                with open(SIGNATURE_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def calculate_tool_hash(self, tool_path):
        sha256_hash = hashlib.sha256()
        
        files_to_hash = []
        for root, _, files in os.walk(tool_path):
            for file in files:
                if file.endswith(".py"):
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, tool_path)
                    files_to_hash.append((rel_path, full_path))
        
        files_to_hash.sort(key=lambda x: x[0].replace("\\", "/"))

        for rel_path, full_path in files_to_hash:
            try:
                with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                
                content = content.replace("\r\n", "\n").replace("\r", "\n")
                
                sha256_hash.update(content.encode("utf-8"))
                
                normalized_path = rel_path.replace("\\", "/")
                sha256_hash.update(normalized_path.encode("utf-8"))
                
            except Exception:
                pass 

        return sha256_hash.hexdigest()

    def verify_tool(self, tool_id, tool_path):
        if tool_id not in self.signatures:
            return False 
            
        current_hash = self.calculate_tool_hash(tool_path)
        expected_hash = self.signatures[tool_id]
        
        return current_hash == expected_hash