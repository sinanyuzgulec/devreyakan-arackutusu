import importlib
import pkgutil
import os
from .integrity import IntegrityManager

class ToolManager:
    def __init__(self, package_name='tools'):
        self.package_name = package_name
        self.loaded_tools = {} 
        self.all_categories = set()
        self.integrity_checker = IntegrityManager()

    def discover_tools(self):
        self.loaded_tools.clear()
        self.all_categories.clear()

        try:
            package = importlib.import_module(self.package_name)
        except ImportError:
            return

        
        
        
        if hasattr(package, "__path__") and list(package.__path__):
            
            package_path = list(package.__path__)[0]
        elif hasattr(package, "__file__") and package.__file__:
            
            package_path = os.path.dirname(package.__file__)
        else:
            
            package_path = os.path.join(os.getcwd(), self.package_name)
        

        
        for _, name, ispkg in pkgutil.iter_modules(package.__path__):
            if ispkg:
                full_name = f"{self.package_name}.{name}"
                tool_fs_path = os.path.join(package_path, name)

                try:
                    module = importlib.import_module(full_name)
                    if hasattr(module, 'TOOL_METADATA'):
                        meta = module.TOOL_METADATA
                        
                        if 'id' in meta and 'widget_class' in meta:
                            
                            tool_id = meta['id']
                            is_verified = self.integrity_checker.verify_tool(tool_id, tool_fs_path)
                            meta['verified'] = is_verified
                            

                            self.loaded_tools[tool_id] = meta
                            for cat in meta.get('categories', []):
                                self.all_categories.add(cat)
                except Exception as e:
                    print(f"[ERROR] Tool yüklenemedi ({name}): {e}")

    def get_tool_instance(self, tool_id):
        if tool_id in self.loaded_tools:
            return self.loaded_tools[tool_id]['widget_class']()
        return None
