import os
from http.server import SimpleHTTPRequestHandler, HTTPServer
import urllib.parse as urlparse
import json

class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse.urlparse(self.path)
        path = parsed.path
        params = urlparse.parse_qs(parsed.query)

        if path == "/set":
            slide = params.get("slide", [""])[0]
            with open("current.txt", "w") as f:
                f.write(slide)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")

        elif path == "/imagelist":
            image_folder = "images"
            files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
            files.sort()  # Optional: sort numerically or alphabetically
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(files).encode())

        else:
            super().do_GET()

PORT = 8080
server = HTTPServer(("", PORT), MyHandler)
print(f"Server running at http://localhost:{PORT}")
server.serve_forever()