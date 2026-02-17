"""Цей код створює простий багатопотоковий HTTP сервер, який відповідає на GET запити."""

import http.server
import socketserver
import threading


class MyHandler(http.server.SimpleHTTPRequestHandler):
    """Обробник HTTP запитів, який відповідає на GET запити."""

    def do_GET(self):
        if self.path == "/shutdown":
            self.send_response(200)
            self.send_header("Content-type", "text/plain; charset=utf-8")
            self.end_headers()
            msg = f"Сервер зупиняється... (потік: {threading.current_thread().name})\n"
            self.wfile.write(msg.encode("utf-8"))
            threading.Thread(target=self.server.shutdown).start()
        else:
            self.send_response(200)
            self.send_header("Content-type", "text/plain; charset=utf-8")
            self.end_headers()
            msg = f"Привіт! Ви підключені з потоку: {threading.current_thread().name}\n"
            self.wfile.write(msg.encode("utf-8"))


class ThreadingHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    """HTTP сервер, який підтримує багатопоточність."""
    daemon_threads = True


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080
    with ThreadingHTTPServer((HOST, PORT), MyHandler) as server:
        print(f"Сервер запущено на http://{HOST}:{PORT}")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nСервер зупинено.")
