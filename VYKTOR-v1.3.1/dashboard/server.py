import asyncio, json, os, socket
from http.server import SimpleHTTPRequestHandler, HTTPServer
from threading import Thread
import websockets

LOG_PATH = "results/live_feed.log"
connected = set()
PORTS = {"http": None, "ws": None}

def find_free_port(preferred: int) -> int:
    p = int(preferred)
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("127.0.0.1", p))
                return p
            except OSError:
                p += 1

def read_last_lines(path: str, n: int = 120):
    if not os.path.exists(path): return []
    try:
        with open(path, "rb") as f:
            f.seek(0, 2)
            size = f.tell()
            block = 4096
            data = b""
            while size > 0 and data.count(b"\n") <= n:
                step = min(block, size)
                size -= step
                f.seek(size)
                data = f.read(step) + data
            return [l.decode("utf-8", "ignore") for l in data.splitlines()[-n:]]
    except Exception:
        return []

async def ws_handler(websocket):
    connected.add(websocket)
    for line in read_last_lines(LOG_PATH, n=120):
        try:
            await websocket.send(line.strip())
        except Exception:
            pass
    try:
        with open("results/vyktor_summary.json", "r", encoding="utf-8") as f:
            await websocket.send(json.dumps({"event": "summary", "data": json.load(f)}))
    except Exception:
        pass
    try:
        await websocket.wait_closed()
    finally:
        connected.discard(websocket)

async def tail_log():
    last = 0
    while True:
        try:
            if os.path.exists(LOG_PATH):
                with open(LOG_PATH, "r", encoding="utf-8") as f:
                    f.seek(last)
                    chunk = f.read()
                    last = f.tell()
                if chunk:
                    for line in chunk.splitlines():
                        msg = line.strip()
                        for ws in list(connected):
                            try:
                                await ws.send(msg)
                            except Exception:
                                connected.discard(ws)
        except Exception as e:
            print("tail error:", e)
        await asyncio.sleep(0.5)

class StaticServer(SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory="dashboard/static", **k)
    def do_GET(self):
        if self.path == "/":
            self.path = "/dashboard.html"
        elif self.path == "/favicon.ico":
            self.send_response(204); self.end_headers(); return
        elif self.path == "/api/summary":
            try:
                with open("results/vyktor_summary.json", "r", encoding="utf-8") as f:
                    data = f.read().encode("utf-8")
                self.send_response(200); self.send_header("Content-Type", "application/json")
                self.end_headers(); self.wfile.write(data); return
            except Exception:
                self.send_response(404); self.end_headers(); self.wfile.write(b"{}"); return
        elif self.path == "/api/ports":
            self.send_response(200); self.send_header("Content-Type", "application/json")
            self.end_headers(); self.wfile.write(json.dumps(PORTS).encode("utf-8")); return
        elif self.path == "/api/config":
            title = "Vyktor v1.3.0-DEV (Trident)"
            self.send_response(200); self.send_header("Content-Type","application/json")
            self.end_headers(); self.wfile.write(json.dumps({"title": title}).encode("utf-8")); return
        return super().do_GET()

def http_server(port: int):
    PORTS["http"] = port
    httpd = HTTPServer(("127.0.0.1", port), StaticServer)
    print(f"Dashboard (HTTP) at http://127.0.0.1:{port}")
    httpd.serve_forever()

async def main_ws(ws_port: int):
    PORTS["ws"] = ws_port
    async with websockets.serve(ws_handler, "127.0.0.1", ws_port):
        print(f"Dashboard (WebSocket) on ws://127.0.0.1:{ws_port}")
        await tail_log()

if __name__ == "__main__":
    http_env = int(os.environ.get("HTTP_PORT","8080"))
    ws_env = int(os.environ.get("WS_PORT","8765"))
    http_port = find_free_port(http_env)
    # if WS busy, bump
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("127.0.0.1", ws_env)); ws_port = ws_env
        except OSError:
            ws_port = ws_env + 1
    from threading import Thread
    Thread(target=http_server, args=(http_port,), daemon=True).start()
    import asyncio; asyncio.run(main_ws(ws_port))
