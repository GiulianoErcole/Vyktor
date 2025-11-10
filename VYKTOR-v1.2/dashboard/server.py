from wsgiref.simple_server import make_server
import json

HTML = b"""<!doctype html>
<html><head><meta charset="utf-8"><title>Vyktor Dashboard</title>
<style>body{font-family:system-ui;margin:24px} pre{background:#111;color:#eee;padding:12px;border-radius:8px;overflow:auto}</style>
</head><body>
<h1>Vyktor Dashboard</h1>
<p>Auto-refreshing every 2s.</p>
<pre id="out">Loading...</pre>
<script>
async function tick(){
  try{
    const r = await fetch('/api/summary');
    const j = await r.json();
    document.getElementById('out').textContent = JSON.stringify(j, null, 2);
  }catch(e){
    document.getElementById('out').textContent = 'No summary yet.';
  }
}
setInterval(tick, 2000); tick();
</script>
</body></html>"""

def app(environ, start_response):
    path = environ.get('PATH_INFO','/')
    if path == '/':
        start_response('200 OK', [('Content-Type','text/html')])
        return [HTML]
    if path == '/api/summary':
        try:
            with open('results/vyktor_summary.json','r',encoding='utf-8') as f:
                data = f.read().encode('utf-8')
            start_response('200 OK', [('Content-Type','application/json')])
            return [data]
        except Exception:
            start_response('404 Not Found', [('Content-Type','application/json')])
            return [b'{}']
    start_response('404 Not Found', [('Content-Type','text/plain')])
    return [b'Not found']

if __name__ == '__main__':
    with make_server('127.0.0.1', 8080, app) as httpd:
        print("Dashboard on http://127.0.0.1:8080")
        httpd.serve_forever()
