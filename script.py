import datetime
import time
import xmlrpc.client
import natpmp
import sys
import schedule

def log(msg, err = False):
    date = datetime.datetime.now()
    print(f"[{date}] {msg}", file=sys.stderr if err else sys.stdout)

def set_port(port):
    with xmlrpc.client.ServerProxy("http://192.168.1.100:1313/RPC2") as s:
        s.network.port_range.set("", f"{port}-{port}")

def run():
    previous_port = 0

    try:
        with open("/tmp/assigned_port", "r") as f:
            previous_port = int(f.read())
    except:
        previous_port = 0

    res = natpmp.map_port(natpmp.NATPMP_PROTOCOL_TCP, 0, 0, 60, "10.2.0.1")

    if res.result != 0:
        log("Error: " + res, True)
    else:
        set_port(res.public_port)
        if res.public_port != previous_port:
            with open("/tmp/assigned_port", "w") as f:
                f.write(str(res.public_port))
            log("Assigned new port: " + str(res.public_port))

schedule.every(30).seconds.do(run)

while True:
    schedule.run_pending()
    time.sleep(1)
