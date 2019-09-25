import socketserver

from readers.reader import Reader


HOST, PORT = "localhost", 9999
READER = None


class Handler_TCPServer(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip()
        READER.parent.enqueue_read(
                (READER.reader_id, str(int(self.data))))


class TCPReader(Reader):
    def run(self):
        global READER
        READER = self
        print('reader started')
        self.tcp_server = socketserver.TCPServer(
                (HOST, PORT),
                Handler_TCPServer)
        self.tcp_server.serve_forever()

    def shutdown(self):
        self.tcp_server.shutdown()
