import socket, select, time, random
ok_needed = 2
class AgenteRequester:
    def __init__(self, agent_id, host="127.0.0.1", port=8088):
        self.id = agent_id
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, port))
        self._send(f"HELLO {self.id} requester")
        print(f"[{self.id}] help requester connected.")

    def _send(self, text: str):
        self.s.sendall((text.strip()+"\n").encode("utf-8"))

    def _recv_lines(self, timeout):
        out=[]
        r,_,_=select.select([self.s], [], [], timeout)
        if not r: return out
        data = self.s.recv(65535).decode("utf-8")
        for line in data.splitlines():
            line=line.strip()
            if line: out.append(line)
        return out

    def run(self, periods=10, wait_window=3.0):
        satisfied=0
        for req_id in range(1, periods+1):
            self._send(f"HELP {req_id} {self.id}")
            print(f"[help requester {self.id}] asks HELP ")

            oks=0
            t0 = time.time()
            while time.time()-t0 < wait_window and oks < ok_needed:
                remaining = max(0.0, wait_window - (time.time()-t0))
                for line in self._recv_lines(remaining):
                    parts=line.split()
                    if parts[0]=="OK" and parts[1]==str(req_id):
                        oks+=1
                        print(f"[{self.id}] <- OK [{oks}]")
                    elif parts[0]=="NO" and parts[1]==str(req_id):
                        print(f"[{self.id}] <- NO")
            print(f"[{self.id}] Period {req_id}: satisfied={oks>=ok_needed}, OK={oks}\n")
            if oks>=ok_needed:
                satisfied+=1
            time.sleep(random.uniform(1.0, 2.0))
        print(f"=== RESULTS ===\nPERIODS={periods}  SATISFIED={satisfied}")
