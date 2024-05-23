from http.server import SimpleHTTPRequestHandler, HTTPServer
import json

class RequestHandler(SimpleHTTPRequestHandler):
    def _set_headers(self):
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'x-api-key, Content-Type')

    def do_OPTIONS(self):
        self.send_response(200)
        self._set_headers()
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        try:
            rssi = int(json.loads(post_data)['rssi'])

            # Calculate location based on RSSI
            location = self.calculate_location(rssi)

            response = {'location': location}
            self.send_response(200)
            self._set_headers()
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
        except Exception as e:
            self.send_response(400)
            self._set_headers()
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())

    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        return super().do_GET()

    def calculate_location(self, rssi):
        if rssi >= -50:
            return "Near the laptop"
        elif rssi >= -70:
            return "Living room"
        elif rssi >= -75:
            return "2nd bedroom"
        elif rssi >= -85:
            return "Kitchen or Bedroom"
        else:
            return "Unknown location"

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting HTTP server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
