from http.server import BaseHTTPRequestHandler, HTTPServer
import sqlite3
import urllib.parse

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('index.html', 'r') as file:
                self.wfile.write(file.read().encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Page not found')

    def do_POST(self):
        if self.path == '/submit':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode()
            data = urllib.parse.parse_qs(post_data)

            name = data.get('name', [''])[0]
            email = data.get('email', [''])[0]

            self.save_to_db(name, email)

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Form submitted successfully!')

    def save_to_db(self, name, email):
        # Connect to SQLite database
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        # Insert user data into the users table
        cursor.execute('''
            INSERT INTO users (name, email)
            VALUES (?, ?)
        ''', (name, email))

        # Commit changes and close connection
        conn.commit()
        conn.close()

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()