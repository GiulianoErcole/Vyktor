import asyncio, json, os
from http.server import SimpleHTTPRequestHandler, HTTPServer
from threading import Thread
import websockets
LOG_PATH = "results/live_feed.log"
connected = set()
def read_last_lines(path, n=50):
    if not os.path.exists(path): return []
    try:
        with open(path, "rb") as f:
            f.seek(0, os.SEEK_END); size = f.tell(); block=4096; data=b""
            while size > 0 and data.count(b"\n") <= n:
                step=min(block,size); size-=step; f.seek(size); data=f.read(step)+data
            return [l.decode("utf-8","ignore") for l in data.splitlines()[-n:]]
    except Exception: return []
async def ws_handler(websocket):
    connected.add(websocket)
    for line in read_last_lines(LOG_PATH, n=50):
        try: await websocket.send(line.strip())
        except Exception: pass
    try:
        with open("results/vyktor_summary.json","r",encoding="utf-8") as f:
            await websocket.send(json.dumps({"event":"summary","data":json.load(f)}))
    except Exception: pass
    try: await websocket.wait_closed()
    finally: connected.discard(websocket)
async def tail_log():
    last_size=0
    while True:
        try:
            if os.path.exists(LOG_PATH):
                cur_size=os.path.getsize(LOG_PATH)
                if cur_size < last_size: last_size = 0
                with open(LOG_PATH,"r",encoding="utf-8") as f:
                    f.seek(last_size); chunk=f.read(); last_size=f.tell()
                if chunk:
                    for line in chunk.splitlines():
                        msg=line.strip()
                        for ws in list(connected):
                            try: await ws.send(msg)
                            except Exception: connected.discard(ws)
        except Exception as e:
            print("Log tail error:", e)
        await asyncio.sleep(0.5)
class StaticServer(SimpleHTTPRequestHandler):
    def __init__(self,*args,**kwargs): super().__init__(*args,directory="dashboard/static",**kwargs)
    def do_GET(self):
        if self.path == "/api/summary":
            try:
                with open("results/vyktor_summary.json","r",encoding="utf-8") as f:
                    data=f.read().encode("utf-8")
                self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers(); self.wfile.write(data); return
            except Exception:
                self.send_response(404); self.send_header("Content-Type","application/json"); self.end_headers(); self.wfile.write(b"{}"); return
        return super().do_GET()
def http_server():
    httpd = HTTPServer(("127.0.0.1",8080), StaticServer); print("Dashboard (HTTP) at http://127.0.0.1:8080"); httpd.serve_forever()
async def main_ws():
    async with websockets.serve(ws_handler,"127.0.0.1",8765):
        print("Dashboard (WebSocket) on ws://127.0.0.1:8765"); await tail_log()
if __name__ == "__main__":
    Thread(target=http_server, daemon=True).start(); asyncio.run(main_ws())
