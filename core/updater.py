import requests
import zipfile
import os
import shutil
import sys
import tempfile
from PyQt6.QtCore import QThread, pyqtSignal
from .version import CURRENT_VERSION, GITHUB_OWNER, GITHUB_REPO
from .localization import loc

class UpdateChecker(QThread):
    update_available = pyqtSignal(str, str)
    no_update = pyqtSignal()
    error_occurred = pyqtSignal(str)
    status_message = pyqtSignal(str)

    def run(self):
        self.status_message.emit(loc.get("updater_checking"))
        api_url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/releases/latest"
        
        try:
            response = requests.get(api_url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                remote_tag = data.get('tag_name', '').strip()
                remote_version = remote_tag.lstrip('v')
                
                if remote_version and remote_version != CURRENT_VERSION:
                    
                    assets = data.get('assets', [])
                    download_url = None
                    
                    if assets:
                        for asset in assets:
                            if asset['name'].endswith('.zip'):
                                download_url = asset['browser_download_url']
                                break
                        if not download_url:
                            download_url = assets[0]['browser_download_url']
                    
                    if download_url:
                        self.status_message.emit(loc.get("updater_new_version").format(remote=remote_version, local=CURRENT_VERSION))
                        self.update_available.emit(remote_version, download_url)
                    else:
                        self.error_occurred.emit("Release found but no assets available.")
                else:
                    self.status_message.emit(loc.get("updater_uptodate").format(version=CURRENT_VERSION))
                    self.no_update.emit()
            
            elif response.status_code == 404:
                self.error_occurred.emit(f"Repo not found: {GITHUB_OWNER}/{GITHUB_REPO}")
            else:
                self.error_occurred.emit(f"GitHub API Error: {response.status_code}")
                
        except Exception as e:
            self.error_occurred.emit(str(e))
            self.status_message.emit(loc.get("updater_server_error"))

class UpdateDownloader(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal()
    error = pyqtSignal(str)
    status_message = pyqtSignal(str)

    def __init__(self, url):
        super().__init__()
        self.url = url
        self._is_running = True

    def run(self):
        try:
            self.status_message.emit(loc.get("updater_downloading"))
            
            temp_dir = tempfile.gettempdir()
            local_filename = os.path.join(temp_dir, "update_package.zip")
            
            with requests.get(self.url, stream=True) as r:
                r.raise_for_status()
                total_length = r.headers.get('content-length')
                
                with open(local_filename, 'wb') as f:
                    if total_length is None:
                        f.write(r.content)
                    else:
                        dl = 0
                        total_length = int(total_length)
                        for chunk in r.iter_content(chunk_size=8192):
                            if not self._is_running:
                                return
                            if chunk:
                                dl += len(chunk)
                                f.write(chunk)
                                percent = int(100 * dl / total_length)
                                self.progress.emit(percent)

            self.status_message.emit(loc.get("updater_extracting"))
            
            extract_path = os.getcwd()
            
            with zipfile.ZipFile(local_filename, 'r') as zip_ref:
                zip_ref.extractall(extract_path)

            self.status_message.emit(loc.get("updater_ready"))
            
            try:
                os.remove(local_filename)
            except:
                pass
                
            self.finished.emit()
            
        except Exception as e:
            self.status_message.emit(loc.get("updater_failed").format(msg=str(e)))
            self.error.emit(str(e))

    def stop(self):
        self._is_running = False

def restart_application():
    python = sys.executable
    os.execl(python, python, *sys.argv)