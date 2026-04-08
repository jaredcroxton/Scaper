"""
Local development server for the Scaper dashboard.
Serves the dashboard and data files with proper CORS headers.

Usage:
  python serve.py          # Start on port 8080
  python serve.py 3000     # Start on custom port
"""

import http.server
import os
import sys

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))


class CORSHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()


if __name__ == "__main__":
    with http.server.HTTPServer(("", PORT), CORSHandler) as httpd:
        print(f"\n  Scaper Dashboard")
        print(f"  ================")
        print(f"  Dashboard:  http://localhost:{PORT}/dashboard/")
        print(f"  Data API:   http://localhost:{PORT}/data/articles.json")
        print(f"\n  Press Ctrl+C to stop.\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")
