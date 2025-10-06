	Commands
- To start the server
	 uv run server.py
- To start the help requester agent
	uv run agent_invoker.py requester 2
- To start any agent that says OK, NO or NOTHING
	uv run agent_invoker.py worker 3
	uv run agent_invoker.py worker 4
	uv run agent_invoker.py worker 5

IMPORTANT: The last parameter is the agent id, therefore it has to be unique.

-----------------------------------------------------------------------------------------------------
						FUNCTIONAL DESCRIPTION 
-----------------------------------------------------------------------------------------------------
This project uses TCP sockets to let agents talk to a central server.

Each agent connects to the server and sends a simple message like HELLO <id> <role>, saying who it is and what it does — for example, a requester (the one who asks for help) or a simple agent (the one who gives answers).

The server reads that message and keeps every connection stored, so it knows which agents are connected and what role each one has.

When the requester wants help, it sends a "HELP" message to the server. The server then forwards that message to all the workers.
Each worker waits a random time and decides (based on the percentages the exercise says) whether to answer with OK, NO, or stay silent.

The server collects those replies and sends them back to the requester, who counts how many OKs it got to see if it reached the amount needed.

Everything happens asynchronously; the server runs each connection in its own thread, and the agents send and receive messages independently without waiting for each other (being therefore non-blocking threads).

-----------------------------------------------------------------------------------------------------
						CODE STRUCTURE
-----------------------------------------------------------------------------------------------------

- server.py
  Creates a threaded TCP server that listens for connections. Each connected agent is registered through the message `HELLO <id> <role>`.  
  The server then acts as a communication hub: when it receives `HELP` from the requester, it forwards that message to all workers.  
  Later, it receives the `OK` or `NO` messages from the workers and sends them back to the requester.

- agent_help.py
  Connects to the server and periodically sends `HELP` messages.  
  It waits for responses and counts how many `OK` have arrived to check if the quorum is reached.  

- agent.py
  Connects to the same server and listens for incoming `HELP` messages.  
  After a small random delay, each worker answers following the required probabilities: 40% OK, 50% NO, 10% silence.  

