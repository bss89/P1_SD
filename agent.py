import socket, select, time, random

class AgenteWorker:
    def __init__(self, agent_id, host="127.0.0.1", port=8088):
        self.id = agent_id
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, port))
        self._send(f"HELLO {self.id} agent")#We give the server our id so it aknwoledges us
        print(f"[{self.id}] agent connected.")

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

    def run(self):
        while True:
            for line in self._recv_lines(0.5):
                parts = line.split()
                if len(parts)==3 and parts[0]=="HELP":#We treat only HELP requests
                    req_id = int(parts[1]) #Store the iteration number
                    requester_id = int(parts[2])
                    time.sleep(random.uniform(0.1, 0.8))
                    roll = random.random()
                    if roll < 0.40:
                        self._send(f"OK {req_id} {self.id} {requester_id}")
                        print(f"[{self.id}] -> OK")
                    elif roll < 0.90:
                        self._send(f"NO {req_id} {self.id} {requester_id}")
                        print(f"[{self.id}] -> NO")
                    else:
                        print(f"[{self.id}] -> NOTHING")
