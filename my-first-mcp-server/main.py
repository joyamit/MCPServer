from mcp.server.fastmcp import FastMCP
from datetime import datetime
from typing import List

# Create the MCP server
mcp = FastMCP("LeaveManager")

# ✅ Sample employee data
employees = {
    "E001": "Amit",
    "E002": "Sneha",
    "E003": "Rahul"
}

leave_balance = {
    "E001": 12,
    "E002": 8,
    "E003": 15
}

leave_requests = []

holidays = [
    {"date": "2025-08-15", "name": "Independence Day"},
    {"date": "2025-10-02", "name": "Gandhi Jayanti"},
    {"date": "2025-12-25", "name": "Christmas"}
]

# ✅ Helper: Validate employee ID
def is_valid_employee(emp_id: str) -> bool:
    return emp_id in employees

# 🛠 Tool: Apply for leave
@mcp.tool()
def apply_leave(emp_id: str, start_date: str, end_date: str, reason: str) -> str:
    """Apply for leave"""
    if not is_valid_employee(emp_id):
        return "❌ Invalid employee ID."

    days = (datetime.fromisoformat(end_date) - datetime.fromisoformat(start_date)).days + 1
    balance = leave_balance.get(emp_id, 0)

    if days > balance:
        return f"❌ Leave denied. You only have {balance} days left."

    leave_balance[emp_id] -= days
    leave_requests.append({
        "emp_id": emp_id,
        "name": employees[emp_id],
        "start": start_date,
        "end": end_date,
        "reason": reason
    })

    return f"✅ Leave approved for {employees[emp_id]} from {start_date} to {end_date}."

# 🛠 Tool: Check leave balance
@mcp.tool()
def check_balance(emp_id: str) -> str:
    """Check remaining leave balance"""
    if not is_valid_employee(emp_id):
        return "❌ Invalid employee ID."

    balance = leave_balance.get(emp_id, 0)
    return f"🧾 {employees[emp_id]} has {balance} days of leave remaining."

# 🛠 Tool: Get leave history
@mcp.tool()
def get_leave_history(emp_id: str) -> list:
    """Get leave history for an employee"""
    if not is_valid_employee(emp_id):
        return ["❌ Invalid employee ID."]

    history = [
        f"{r['start']} to {r['end']} - {r['reason']}"
        for r in leave_requests if r["emp_id"] == emp_id
    ]
    return history or ["ℹ️ No leave history found."]

# 📚 Resource: List upcoming holidays
@mcp.resource("holidays://upcoming")
def get_upcoming_holidays() -> list:
    """List upcoming holidays"""
    today = datetime.today().date()
    return [h for h in holidays if datetime.fromisoformat(h["date"]).date() >= today]

# 📢 Resource: Greeting
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"👋 Hello, {name}! How can I assist you with leave management today?"

# 🧠 Prompt: Write a leave request email
@mcp.prompt()
def leave_email(emp_id: str, start_date: str, end_date: str, reason: str) -> str:
    """Generate a leave request email"""
    if not is_valid_employee(emp_id):
        return "❌ Invalid employee ID."

    name = employees[emp_id]
    return (
        f"Dear Manager,\n\n"
        f"I would like to request leave from {start_date} to {end_date} "
        f"due to {reason}. Please let me know if this can be approved.\n\n"
        f"Regards,\n{name}"
    )

# 🚀 Run the server
if __name__ == "__main__":
    mcp.run(transport="stdio")
