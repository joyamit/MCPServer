
# My First MCP Server — LeaveManager

A minimal example MCP (Modular Chat Protocol) server implemented using the `FastMCP` helper.
This repository contains a tiny leave-management example that exposes tools, resources,
and a prompt handler via an MCP-compatible server.

## Features

- Tools
	- `apply_leave(emp_id, start_date, end_date, reason)` — submit a leave request and update leave balances.
	- `check_balance(emp_id)` — return remaining leave days.
	- `get_leave_history(emp_id)` — return past leave requests for an employee.
- Resources
	- `holidays://upcoming` — list upcoming holidays.
	- `greeting://{name}` — return a personalized greeting.
- Prompt
	- `leave_email(emp_id, start_date, end_date, reason)` — generate a leave request email template.

## Files

- `main.py` — main server implementation and in-memory example data (in this directory).
- `pyproject.toml` — project metadata and (optional) dependencies.

## Requirements

- Python 3.11+ recommended (project uses modern datetime features).
- No external dependencies required by default; if you add packages, update `pyproject.toml`.

## Quick start (macOS / Linux)

1. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Run the server locally (example uses stdio transport):

```bash
python main.py
```

This starts `FastMCP("LeaveManager")` and listens on stdio as configured in `main.py`.

### Run with `uv` (MCP client)

If you have an MCP-capable client named `uv` installed, you can install/run the example with:

```bash
uv run mcp install main.py
```

This runs the MCP module from `main.py` via the `uv` client; exact behavior depends on your `uv` installation.

## Usage

The example exposes a small set of tools/resources. Interact with them from any MCP-capable client
or from a stdio-based test harness that speaks the MCP protocol.

- Apply for leave
	- Tool: `apply_leave`
	- Parameters: `emp_id` (string), `start_date` (YYYY-MM-DD), `end_date` (YYYY-MM-DD), `reason` (string)
	- Behavior: validates employee, checks leave balance, updates balance and appends the request to in-memory history.

- Check balance
	- Tool: `check_balance`
	- Parameters: `emp_id`
	- Returns remaining leave days.

- Get leave history
	- Tool: `get_leave_history`
	- Parameters: `emp_id`
	- Returns a list of past leave requests for the employee.

- Upcoming holidays
	- Resource: `holidays://upcoming`
	- Returns holidays on or after today's date (uses ISO `YYYY-MM-DD`).

- Greeting
	- Resource: `greeting://{name}` — returns a simple personalized greeting string.

- Generate leave email
	- Prompt: `leave_email(emp_id, start_date, end_date, reason)` — returns a ready-to-send email body for the requestor.

## Example data and limitations

- The example stores `employees`, `leave_balance`, `leave_requests`, and `holidays` in-memory inside `main.py` for simplicity.
- For real-world use, replace the in-memory structures with a persistent datastore (database, cloud store, etc.).
- Dates are parsed with `datetime.fromisoformat()`; pass ISO-format dates (YYYY-MM-DD).

## Development notes

- To run quick manual tests, you can invoke the tools programmatically if you wire an MCP client to stdio.
- Consider adding unit tests and a small integration harness if you plan to evolve this into a production service.

## License

Add a license file or include license text as needed.
