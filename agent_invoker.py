# agente.py
import sys
import argparse
from agent_help import AgenteRequester
from agent import AgenteWorker

def main():
    p = argparse.ArgumentParser(description="Runner de agentes")
    p.add_argument("role", choices=["requester", "worker"], help="Rol del agente")
    p.add_argument("id", type=int, help="ID del agente")
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=8088)
    p.add_argument("--periods", type=int, default=12, help="(solo requester)")
    p.add_argument("--wait", type=float, default=3.0, help="ventana de espera (solo requester)")
    a = p.parse_args()

    if a.role == "requester":
        AgenteRequester(a.id, a.host, a.port).run(periods=a.periods, wait_window=a.wait)
    else:
        AgenteWorker(a.id, a.host, a.port).run()

if __name__ == "__main__":
    sys.exit(main())
