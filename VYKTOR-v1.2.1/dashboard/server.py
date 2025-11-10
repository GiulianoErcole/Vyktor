import asyncio, os
from http.server import SimpleHTTPRequestHandler, HTTPServer
from threading import Thread
import websockets  # third-party; see requirements.txt

LOG_PATH = "results/live_feed.log"
connected = set()

async def tail_log():
    last_size = 0
    while True:
        try:
            if os.path.exists(LOG_PATH):
                with open(LOG_PATH, "r", encoding="utf-8") as f:
                    f.seek(last_size)
                    lines = f.readlines()
                    last_size = f.tell()
                if lines:
                    for line in lines:
                        for ws in connected.copy():
                            try:
                                await ws.send(line.strip())
                            except Exception:
                                connected.discard(ws)
        except Exception as e:
            print("Log tail error:", e)
        await asyncio.sleep(1)

async def ws_handler(websocket):
    connected.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        connected.discard(websocket)

class StaticServer(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="dashboard/static", **kwargs)

def http_server():
    httpd = HTTPServer(("127.0.0.1", 8080), StaticServer)
    print("Dashboard (HTTP) at http://127.0.0.1:8080")
    httpd.serve_forever()

async def main_ws():
    async with websockets.serve(ws_handler, "127.0.0.1", 8765):
        print("Dashboard (WebSocket) on ws://127.0.0.1:8765")
        await tail_log()

if __name__ == "__main__":
    Thread(target=http_server, daemon=True).start()
    asyncio.run(main_ws())
