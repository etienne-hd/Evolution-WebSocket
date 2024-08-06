from Roobet import Roobet
from Evolution import Evolution

roobet = Roobet(sid="Your SID")
evolution = Evolution()

url = roobet.get_entry_url("crazytime")

ws = evolution.get_websocket(
    entry_url=url,
    table_id="CrazyTime0000001"
)

print(ws) # WebSocket