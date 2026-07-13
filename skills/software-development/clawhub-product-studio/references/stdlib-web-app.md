# Zero-dependency web app (stdlib http.server + sqlite3)

For the user's ~600MB-RAM box, prefer **no pip installs**. A complete web app
needs only the Python stdlib: `http.server` (REST + static) and `sqlite3`.

## SPA static serving from the same server
In your `BaseHTTPRequestHandler`, separate API from assets:

```python
def do_GET(self):
    if self.path.startswith("/api/"):
        return self._api_get()
    return self._serve_static()

def _serve_static(self):
    rel = self.path.split("?", 1)[0].lstrip("/")
    if rel in ("", "index.html"):
        rel = "index.html"
    target = os.path.normpath(os.path.join(web_root, rel))
    # PATH-TRAVERSAL GUARD — mandatory, not optional:
    if not target.startswith(web_root) or not os.path.isfile(target):
        return _json(self, 404, {"error": "not found"})
    ext = os.path.splitext(target)[1].lower()
    ctypes = {".html":"text/html; charset=utf-8", ".css":"text/css; charset=utf-8",
              ".js":"application/javascript; charset=utf-8", ".json":"application/json"}
    with open(target, "rb") as f:
        body = f.read()
    self.send_response(200)
    self.send_header("Content-Type", ctypes.get(ext, "application/octet-stream"))
    self.send_header("Content-Length", str(len(body)))
    self.end_headers()
    self.wfile.write(body)
```
`web_root` = `os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "web"))`.

## Why the traversal guard matters
Without `target.startswith(web_root)`, a request to `/../server.py` reads your
source. `os.path.normpath` + the prefix check closes it. Verify with a probe:
`urllib.request.urlopen(base + "/../server.py")` must return 404.

## Threading server + free port
```python
from http.server import ThreadingHTTPServer
srv = ThreadingHTTPServer(("127.0.0.1", port), Handler)
```
Pick a free port in tests via `socket.bind(("127.0.0.1", 0)).getsockname()[1]`.

## Auth without a password store
Login mints a signed token `<exp>.<nonce>.<hmac>` (HMAC-SHA256 over a per-data-dir
random secret, or `CLAWHUB_STUDIO_SECRET` env). No plaintext creds. Verify with
`hmac.compare_digest`. Token TTL ~12h.

## Test the server without a browser
Spin it up in a daemon thread against a `tempfile.mkdtemp()` data dir, then
`urllib.request` the endpoints. Assert status codes + JSON. This is how the
canonical suite (`tests/test_server.py`) proves the API works — no Selenium.
