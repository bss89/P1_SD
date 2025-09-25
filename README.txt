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

