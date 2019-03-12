import http.server
import ssl

class ServerHandler(http.server.SimpleHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        self._set_response()
        f = open('.' + (self.path if self.path != '/' else '/index.html'), 'r')
        self.wfile.write(f.read().encode('utf-8'))
        f.close()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length) 
        f = open('./push.id', 'a')
        f.write(post_data.decode('utf-8') + '\n')
        f.close()
        self._set_response()
        self.wfile.write('ok'.encode('utf-8'))

httpd = http.server.HTTPServer(('localhost', 9443), ServerHandler)
httpd.socket = ssl.wrap_socket (httpd.socket, certfile='./server.pem', server_side=True)
httpd.serve_forever()
