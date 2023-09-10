import datetime
import time
import xmlrpc.client
import natpmp
import sys
import schedule
import os
from dotenv import load_dotenv

load_dotenv()

RPC_URL=os.getenv("RPC_URL") or "http://localhost/RPC2"
GATEWAY=os.getenv("GATEWAY") or "10.2.0.1"

def log(msg, err = False):
    date = datetime.datetime.now()
    print(f"[{date}] {msg}", file=sys.stderr if err else sys.stdout)

def set_port(port):
    with xmlrpc.client.ServerProxy(RPC_URL) as s:
        s.network.port_range.set("", f"{port}-{port}")

def run():
    try:
        res = natpmp.map_port(natpmp.NATPMP_PROTOCOL_TCP, 0, 0, 60, GATEWAY)
    except Exception as e:
        log("An error occured while requesting a port.", err=True)
        log(e, err=True)
        return


    if res.result != 0:
        log("Error: " + res, True)
        return
    
    try:
        set_port(res.public_port)
        log("Assigned port: " + str(res.public_port))
    except Exception as e:
        log("An error occured while trying to update port.", err=True)
        log(e, err=True)



log ("Starting")
log(f"RPC_URL={RPC_URL}")
log(f"GATEWAY={GATEWAY}")

run()
schedule.every(30).seconds.do(run)

while True:
    schedule.run_pending()
    time.sleep(1)
