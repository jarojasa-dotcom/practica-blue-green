import json
import os
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.request import urlopen
from urllib.error import URLError

STATE_FILE = "active.json"

VERSIONS = {
    "blue": {"version": "1.3.0", "port": 8001},
    "green": {"version": "1.4.0", "port": 8002},
}

def active_environment():
    try:
        with open(STATE_FILE) as f:
            env = json.load(f)["active"]
        return env if env in VERSIONS else "blue"
    except (OSError, ValueError, KeyError):
        return "blue"

class BackendHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        env = self.server.environment
        version = VERSIONS[env]["version"]

        if self.path == "/health":
            status, body = 200, {"status": "ok"}
        elif self.path == "/readiness":
            status, body = 200, {"ready": True}
        elif self.path == "/version":
            status, body = 200, {
                "environment": env,
                "version": version
            }
        else:
            status, body = 200, {
                "message": "Aplicacion Blue/Green funcionando",
                "environment": env,
                "version": version
            }

        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(body).encode())

    def log_message(self, *args):
        pass

class RouterHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        env = active_environment()
        target = VERSIONS[env]
        url = f"http://127.0.0.1:{target['port']}{self.path}"

        try:
            with urlopen(url, timeout=2) as response:
                status = response.status
                body = response.read()
        except (URLError, TimeoutError, OSError):
            status = 502
            body = json.dumps({
                "error": "backend_unavailable",
                "environment": env
            }).encode()

        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("X-Active-Environment", env)
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass

def start_server(port, handler, environment=None):
    server = ThreadingHTTPServer(("0.0.0.0", port), handler)
    if environment:
        server.environment = environment
    threading.Thread(target=server.serve_forever, daemon=True).start()
    print(f"Servidor iniciado en puerto {port}")

if __name__ == "__main__":
    if not os.path.exists(STATE_FILE):
        with open(STATE_FILE, "w") as f:
            json.dump({"active": "blue"}, f)

    for env, config in VERSIONS.items():
        start_server(config["port"], BackendHandler, env)

    start_server(8000, RouterHandler)
    print("Router disponible en puerto 8000")
    print("Pulsa Ctrl+C para detener todos los servidores.")

    try:
        threading.Event().wait()
    except KeyboardInterrupt:
        print("Fin de la practica.")
