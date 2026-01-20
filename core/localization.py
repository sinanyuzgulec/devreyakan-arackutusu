import json
import os
import locale

class LocalizationManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LocalizationManager, cls).__new__(cls)
            cls._instance.init_manager()
        return cls._instance

    def init_manager(self):
        self.languages = {}
        self.current_lang_code = "tr"
        self.loaded_strings = {}
        self.base_path = os.path.join(os.getcwd(), "localization")
        
        
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)

        self.load_available_languages()
        self.load_config()

    def load_available_languages(self):
        self.languages.clear()
        if os.path.exists(self.base_path):
            for filename in os.listdir(self.base_path):
                if filename.endswith(".json"):
                    code = filename.split(".")[0]
                    
                    self.languages[code] = code.upper() 

    def load_language(self, code):
        path = os.path.join(self.base_path, f"{code}.json")
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    self.loaded_strings = json.load(f)
                self.current_lang_code = code
                self.save_config()
            except Exception as e:
                print(f"Dil yükleme hatası: {e}")

    def get(self, key, default=None):
        val = self.loaded_strings.get(key, default)
        return val if val else key 

    def save_config(self):
        try:
            with open("config.json", "w") as f:
                json.dump({"language": self.current_lang_code}, f)
        except:
            pass

    def load_config(self):
        """Kaydedilmiş dili geri yükle."""
        try:
            if os.path.exists("config.json"):
                with open("config.json", "r") as f:
                    data = json.load(f)
                    lang = data.get("language", "en") 
                    self.load_language(lang)
            else:
                
                self.load_language("en") 
        except:
            self.load_language("en")


loc = LocalizationManager()