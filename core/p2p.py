import socket
import threading
import json

class P2PNode:
    def __init__(self, port):
        self.port = port
        self.peers = []
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.bind(('127.0.0.1', port))
        except:
            print(f"❌ المنفذ {port} مشغول!")
            return
            
        self.socket.listen(5)
        self.on_msg = None
        threading.Thread(target=self.listen, daemon=True).start()
        print(f"🌐 العقدة تعمل على المنفذ: {port}")

    def listen(self):
        while True:
            try:
                conn, _ = self.socket.accept()
                threading.Thread(target=self.handle, args=(conn,), daemon=True).start()
            except: break

    def handle(self, conn):
        try:
            data = conn.recv(4096)
            if data and self.on_msg:
                msg = json.loads(data.decode('utf-8'))
                self.on_msg(msg)
        except: pass
        conn.close()

    def connect(self, port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(('127.0.0.1', int(port)))
            self.peers.append(int(port))
            s.close()
            return True
        except: return False

    def broadcast(self, data):
        for p in self.peers:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(('127.0.0.1', p))
                s.send(json.dumps(data).encode('utf-8'))
                s.close()
            except: pass