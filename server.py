import socketserver, threading

# ========= Estado global del broker =========
CLIENTS = {}     # id -> wfile
ROLES   = {}     # id -> "requester"|"worker"
LOCK    = threading.Lock()

def send_line(wfile, text: str):
    try:
        wfile.write((text.strip() + "\n").encode("utf-8"))
        wfile.flush()
    except Exception:
        pass

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    allow_reuse_address = True

class AgentHandler(socketserver.StreamRequestHandler):
    def setup(self):
        super().setup()
        self.me_id = None
        self.me_role = None
        print(f"Connected: {self.client_address} on {threading.current_thread().name}")

    def handle(self):
        try:
            for raw in self.rfile:
                if not raw: break
                line = raw.decode("utf-8").strip()
                if not line: continue
                parts = line.split()
                cmd = parts[0].upper()

                if cmd == "HELLO":
                    # HELLO <id> <role>
                    self.me_id = int(parts[1]); self.me_role = parts[2]
                    with LOCK:
                        CLIENTS[self.me_id] = self.wfile
                        ROLES[self.me_id]   = self.me_role
                    send_line(self.wfile, f"WELCOME {self.me_id} {self.me_role}")

                elif cmd == "HELP":
                    # HELP <req_id> <requester_id>
                    req_id = parts[1]; requester_id = int(parts[2])
                    # fan-out a todos los workers
                    with LOCK:
                        for aid, wf in CLIENTS.items():
                            if ROLES.get(aid) == "agent":
                                send_line(wf, f"HELP {req_id} {requester_id}")

                elif cmd in ("OK", "NO"):
                    # OK/NO <req_id> <from_id> <to_id>
                    req_id, from_id, to_id = parts[1], int(parts[2]), int(parts[3])
                    with LOCK:
                        wf = CLIENTS.get(to_id)
                    if wf:
                        send_line(wf, f"{cmd} {req_id} {from_id} {to_id}")
                else:
                    send_line(self.wfile, f"ERROR UnknownCommand {cmd}")
        finally:
            # Limpieza al desconectar
            if self.me_id is not None:
                with LOCK:
                    CLIENTS.pop(self.me_id, None)
                    ROLES.pop(self.me_id, None)
            print(f"Closed: {self.client_address} on {threading.current_thread().name}")

if __name__ == "__main__":
    server = ThreadedTCPServer(('', 8088), AgentHandler)
    try:
        print("Broker TCP listening on :8088")
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()