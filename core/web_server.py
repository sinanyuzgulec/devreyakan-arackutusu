import sys
import os
import base64
import importlib
import inspect
import dataclasses
import json
from urllib.parse import urlparse, parse_qs
from http.server import HTTPServer, BaseHTTPRequestHandler
from PyQt6.QtCore import QThread, pyqtSignal
from core.localization import loc

class DynamicToolAdapter:
    """
    Bu sınıf, araçların logic.py dosyasını derinlemesine analiz eder.
    Fonksiyonları ve Sınıfları (Class) otomatik keşfeder.
    """
    def __init__(self, tool_id):
        self.tool_id = tool_id
        self.logic_module = None
        self.functions = {}
        self.load_logic()

    def load_logic(self):
        try:
            module_path = f"tools.{self.tool_id}.logic"
            self.logic_module = importlib.import_module(module_path)
            
            for name, func in inspect.getmembers(self.logic_module, inspect.isfunction):
                if name.startswith("_") or func.__module__ != self.logic_module.__name__:
                    continue
                self.register_function(name, func)

            for name, cls in inspect.getmembers(self.logic_module, inspect.isclass):
                if cls.__module__ == self.logic_module.__name__:
                    try:
                        instance = cls()
                        for mname, method in inspect.getmembers(instance, inspect.ismethod):
                            if not mname.startswith("_"):
                                self.register_function(f"{name}.{mname}", method)
                    except:
                        pass
        except Exception as e:
            print(f"Logic yükleme hatası ({self.tool_id}): {e}")

    def register_function(self, name, func):
        """Fonksiyonu ve imzasını kaydeder."""
        try:
            sig = inspect.signature(func)
            self.functions[name] = {"func": func, "sig": sig}
        except ValueError:
            pass 

    def generate_input_field(self, name, param):
        """Akıllı input alanı oluşturucu."""
        default_val = ""
        placeholder = f"{name}"
        if param.default != inspect.Parameter.empty:
            default_val = str(param.default)
        
        label = name.replace('_', ' ').title()
        
        is_numeric = False
        if param.annotation in [int, float] or "ohm" in name or "volt" in name or "curr" in name or "freq" in name:
            is_numeric = True

        if is_numeric:
            return f"""
            <div class="form-group">
                <label>{label}:</label>
                <input type="number" step="any" name="{name}" value="{default_val}" placeholder="0.0">
            </div>
            """
        elif "list" in str(param.annotation).lower() or name in ["bands", "colors"]:
             return f"""
            <div class="form-group">
                <label>{label} {loc.get("web_input_separator_hint")}:</label>
                <input type="text" name="{name}" value="{default_val}" placeholder="{loc.get("web_input_placeholder_list")}">
            </div>
            """
        else:
            return f"""
            <div class="form-group">
                <label>{label}:</label>
                <input type="text" name="{name}" value="{default_val}" placeholder="{placeholder}">
            </div>
            """

    def handle_get(self, selected_func_name=None):
        if not self.functions:
            return f"<div class='error'>{loc.get('web_err_no_func_logic')}</div>"

        if not selected_func_name or selected_func_name not in self.functions:
            priorities = [f for f in self.functions.keys() if "calc" in f.lower()]
            selected_func_name = priorities[0] if priorities else list(self.functions.keys())[0]

        func_selector = ""
        if len(self.functions) > 1:
            options = ""
            for fname in sorted(self.functions.keys()):
                sel = "selected" if fname == selected_func_name else ""
                clean_name = fname.replace("_", " ").title()
                options += f"<option value='{fname}' {sel}>{clean_name}</option>"
            
            func_selector = f"""
            <div class="form-group" style="background: #252525; padding: 10px; border-radius: 5px;">
                <label style="color:#22b28b;">{loc.get('web_lbl_select_action')}</label>
                <select onchange="window.location.href='?func='+this.value" style="margin-top:5px;">
                    {options}
                </select>
            </div>
            """

        target_func_data = self.functions[selected_func_name]
        inputs_html = ""
        for param_name, param in target_func_data['sig'].parameters.items():
            if param_name != "self": 
                inputs_html += self.generate_input_field(param_name, param)

        # Tool adını localize etmeye çalış, yoksa ID kullan
        tool_name = loc.get(f"{self.tool_id}_name")
        if tool_name == f"{self.tool_id}_name" or not tool_name: # Key bulunamadıysa
             tool_name = self.tool_id.replace('_', ' ').title()

        return f"""
        <div class="tool-container">
            <h2>{tool_name}</h2>
            {func_selector}
            <form method="POST" action="/tool/{self.tool_id}?func={selected_func_name}">
                {inputs_html}
                <button type="submit">{loc.get('web_btn_calculate')}</button>
            </form>
        </div>
        """

    def handle_post(self, params, func_name):
        if func_name not in self.functions:
            return self.handle_get()

        func_data = self.functions[func_name]
        func = func_data['func']
        sig = func_data['sig']
        
        args = []
        try:
            for param_name, param in sig.parameters.items():
                raw_val = params.get(param_name, [None])[0]
                
                if raw_val is None or raw_val == "":
                    if param.default != inspect.Parameter.empty:
                        args.append(param.default)
                    else:
                        args.append(None)
                    continue

                if "list" in str(param.annotation).lower() or param_name in ["bands"]:
                    if "," in raw_val:
                        list_val = [x.strip() for x in raw_val.split(",")]
                        args.append(list_val)
                    else:
                        args.append([raw_val.strip()])
                
                elif param.annotation == int:
                    args.append(int(float(raw_val)))
                elif param.annotation == float:
                    args.append(float(raw_val))
                
                else:
                    try:
                        if "." in raw_val: args.append(float(raw_val))
                        elif raw_val.isdigit(): args.append(int(raw_val))
                        else: args.append(raw_val) 
                    except:
                        args.append(raw_val)
            
            result = func(*args)
            return self.render_result(result, func_name)
            
        except Exception as e:
            return self.handle_get(func_name) + f"<div class='error'><b>{loc.get('web_err_prefix')}</b> {str(e)}<br><small>{loc.get('web_err_check_format')}</small></div>"

    def render_result(self, result, func_name):
        html = self.handle_get(func_name)
        
        if result is None:
            return html + f"<div class='result'>{loc.get('web_msg_no_result')}</div>"

        content = ""
        
        if dataclasses.is_dataclass(result):
            res_dict = dataclasses.asdict(result)
            content += "<ul class='result-list'>"
            for k, v in res_dict.items():
                content += f"<li><span class='label'>{k.replace('_', ' ').title()}:</span> <span class='value'>{v}</span></li>"
            content += "</ul>"
        
        elif isinstance(result, dict):
            content += "<ul class='result-list'>"
            for k, v in result.items():
                val_display = f"{v.val:.4f} {v.unit}" if hasattr(v, 'val') else str(v)
                content += f"<li><span class='label'>{k.title()}:</span> <span class='value'>{val_display}</span></li>"
            content += "</ul>"
            
        elif isinstance(result, (list, tuple)):
            items_str = ", ".join([str(x) for x in result])
            content += f"<div class='value-large' style='font-size:18px;'>[{items_str}]</div>"
            
        else:
            val_str = f"{result:.4f}" if isinstance(result, float) else str(result)
            content += f"<div class='value-large'>{val_str}</div>"

        return html + f"<div class='result'><h3>{loc.get('web_lbl_result')}</h3>{content}</div>"


class ToolRequestHandler(BaseHTTPRequestHandler):
    USERNAME = ""
    PASSWORD = ""
    TOOL_MANAGER = None
    ADAPTER_CACHE = {}

    def get_adapter(self, tool_id):
        if tool_id not in self.ADAPTER_CACHE:
            adapter = DynamicToolAdapter(tool_id)
            if adapter.functions:
                self.ADAPTER_CACHE[tool_id] = adapter
            else:
                self.ADAPTER_CACHE[tool_id] = None 
        return self.ADAPTER_CACHE[tool_id]

    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm=\"Engineering Tool Server\"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def check_auth(self):
        if not self.USERNAME or not self.PASSWORD: return True
        auth_header = self.headers.get('Authorization')
        if not auth_header: return False
        encoded = auth_header.split(' ')[1]
        decoded = base64.b64decode(encoded).decode('utf-8')
        return decoded == f"{self.USERNAME}:{self.PASSWORD}"

    def get_common_css(self):
        return """
        <style>
            body { font-family: 'Segoe UI', Tahoma, sans-serif; background: #121212; color: #ddd; max-width: 900px; margin: 0 auto; padding: 20px; }
            a { text-decoration: none; color: inherit; }
            h1, h2 { color: #22b28b; }
            
            /* Grid */
            .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 15px; margin-top:20px;}
            .card { background: #1e1e1e; padding: 20px; border-radius: 8px; border: 1px solid #333; text-align: center; transition: all 0.2s; cursor: pointer; }
            .card:hover { transform: translateY(-3px); border-color: #22b28b; background: #252525; }
            .card h3 { margin: 10px 0; color: #fff; font-size: 1.1em; }
            .card small { color: #888; font-size: 0.9em; }

            /* Form */
            .tool-container { background: #1e1e1e; padding: 30px; border-radius: 10px; border: 1px solid #333; }
            .form-group { margin-bottom: 15px; }
            label { display: block; margin-bottom: 8px; font-weight: 600; color: #bbb; }
            input, select { width: 100%; padding: 12px; background: #2d2d2d; border: 1px solid #444; color: white; border-radius: 5px; box-sizing: border-box; font-size: 16px; }
            input:focus { border-color: #22b28b; outline: none; }
            
            button { background: #22b28b; color: white; padding: 15px; border: none; border-radius: 5px; cursor: pointer; width: 100%; font-size: 16px; font-weight: bold; margin-top: 20px; transition: background 0.3s; }
            button:hover { background: #1a8a6b; }
            
            /* Results */
            .result { margin-top: 30px; padding: 20px; background: #1a332a; border-left: 5px solid #22b28b; border-radius: 5px; }
            .error { margin-top: 30px; padding: 20px; background: #331a1a; border-left: 5px solid #d9534f; border-radius: 5px; }
            
            .result-list { list-style: none; padding: 0; }
            .result-list li { display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #2d4a3e; }
            .result-list li:last-child { border-bottom: none; }
            .label { color: #88d4c6; }
            .value { font-weight: bold; font-family: monospace; font-size: 1.1em; color: white; }
            .value-large { font-size: 2em; font-weight: bold; text-align: center; color: white; margin-top: 10px; }
            
            .nav-bar { margin-bottom: 20px; padding-bottom: 10px; border-bottom: 1px solid #333; }
            .nav-link { color: #22b28b; font-weight: bold; display: inline-flex; align-items: center; }
        </style>
        """

    def do_GET(self):
        if not self.check_auth():
            self.do_AUTHHEAD()
            self.wfile.write(loc.get("web_auth_required").encode('utf-8'))
            return

        parsed = urlparse(self.path)
        path_parts = parsed.path.strip('/').split('/')
        query_params = parse_qs(parsed.query)

        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

        html = f"<html><head><title>{loc.get('web_html_title')}</title><meta name='viewport' content='width=device-width, initial-scale=1'>{self.get_common_css()}</head><body>"

        if len(path_parts) == 2 and path_parts[0] == 'tool':
            tool_id = path_parts[1]
            adapter = self.get_adapter(tool_id)
            html += f"<div class='nav-bar'><a href='/' class='nav-link'>&larr; {loc.get('web_nav_main_menu')}</a></div>"
            
            if adapter:
                func_name = query_params.get('func', [None])[0]
                html += adapter.handle_get(func_name)
            else:
                html += f"<div class='error'>{loc.get('web_err_adapter_no_func')}</div>"
        else:
            html += f"<h1>{loc.get('web_page_title')}</h1><p>{loc.get('web_page_subtitle')}</p><div class='grid'>"
            
            if self.TOOL_MANAGER:
                sorted_tools = sorted(self.TOOL_MANAGER.loaded_tools.items(), key=lambda x: x[0])
                
                for tid, meta in sorted_tools:
                    if self.get_adapter(tid):
                        # Tool adını ve açıklamasını localized meta'dan almaya çalış
                        # Eğer meta'da yoksa veya key ise fallback yap
                        name = meta.get('name', tid.replace('_', ' ').title())
                        
                        desc_key = f"{tid}_description"
                        desc = loc.get(desc_key)
                        if desc == desc_key: # Key dönmüşse yani çeviri yoksa
                            desc = meta.get('description', loc.get("web_tool_default_desc"))
                            
                        if len(desc) > 60: desc = desc[:57] + "..."
                        
                        html += f"""
                        <div class='card' onclick="window.location.href='/tool/{tid}'">
                            <h3>{name}</h3>
                            <small>{desc}</small>
                        </div>
                        """
            html += "</div>"
            
            html += f"<div style='margin-top:50px; text-align:center; color:#555; font-size:12px;'>{loc.get('web_footer_running_on')} {self.headers.get('Host')}</div>"

        html += "</body></html>"
        self.wfile.write(html.encode('utf-8'))

    def do_POST(self):
        if not self.check_auth():
            self.do_AUTHHEAD()
            return

        parsed = urlparse(self.path)
        path_parts = parsed.path.strip('/').split('/')
        query_params = parse_qs(parsed.query)
        
        try:
            length = int(self.headers.get('content-length', 0))
            field_data = self.rfile.read(length).decode('utf-8')
            form_params = parse_qs(field_data)
        except:
            form_params = {}

        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

        html = f"<html><head>{self.get_common_css()}</head><body>"
        html += f"<div class='nav-bar'><a href='/' class='nav-link'>&larr; {loc.get('web_nav_main_menu')}</a></div>"

        if len(path_parts) == 2 and path_parts[0] == 'tool':
            tool_id = path_parts[1]
            adapter = self.get_adapter(tool_id)
            if adapter:
                func_name = query_params.get('func', [None])[0]
                
                if not func_name and adapter.functions:
                    func_name = list(adapter.functions.keys())[0]
                    
                html += adapter.handle_post(form_params, func_name)
        
        html += "</body></html>"
        self.wfile.write(html.encode('utf-8'))

class ServerThread(QThread):
    status_log = pyqtSignal(str)
    
    def __init__(self, ip, port, username, password, tool_manager):
        super().__init__()
        self.ip = ip
        self.port = int(port)
        self.httpd = None
        ToolRequestHandler.USERNAME = username
        ToolRequestHandler.PASSWORD = password
        ToolRequestHandler.TOOL_MANAGER = tool_manager

    def run(self):
        try:
            self.httpd = HTTPServer((self.ip, self.port), ToolRequestHandler)
            self.status_log.emit(loc.get("web_log_live").format(ip=self.ip, port=self.port))
            self.httpd.serve_forever()
        except OSError:
            self.status_log.emit(loc.get("web_log_port_busy").format(port=self.port))
        except Exception as e:
            self.status_log.emit(loc.get("web_log_server_error").format(msg=str(e)))

    def stop_server(self):
        if self.httpd:
            self.httpd.shutdown()
            self.httpd.server_close()