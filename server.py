import http.server
import socketserver
import json
import os

PORT = int(os.environ.get("PORT", 8000))

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.path = "/templates/index.html"
        elif self.path == "/admin":
            self.path = "/templates/admin.html"
        elif self.path == "/config":
            with open("config.json", "r", encoding="utf-8") as f:
                config = f.read().encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(config)
            return
        return super().do_GET()

    def do_POST(self):
        if self.path == "/update_config":
            length = int(self.headers.get("Content-Length", 0))
            data = self.rfile.read(length)
            new_config = json.loads(data.decode("utf-8"))

            if new_config.get("password") != "admin":
                self.send_response(403)
                self.end_headers()
                return

            with open("config.json", "w", encoding="utf-8") as f:
                json.dump({
                    "welcome_message": new_config.get("welcome_message"),
                    "dice_faces": new_config.get("dice_faces")
                }, f, indent=2, ensure_ascii=False)

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"status": "ok"}')

os.chdir(os.path.dirname(__file__))
with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
    print(f"🎲 Servidor corriendo en el puerto {PORT}")
    httpd.serve_forever()
