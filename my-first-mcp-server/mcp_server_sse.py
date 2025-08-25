#!/usr/bin/env python3
import requests
from datetime import datetime
from datetime import datetime
from mcp.server.fastmcp import FastMCP

mcp = FastMCP()

# -------- TOOLS --------
@mcp.tool()
def add_numbers(a: int, b: int) -> str:
    """Add two numbers and return the result"""
    return f"The sum of {a} and {b} is {a + b}"

@mcp.tool()
def simple_test() -> str:
    """A simple test function"""
    return "Hello from simple_test!"

@mcp.tool()
def greet_user(name: str) -> str:
    """Greet the user based on current India time"""
    now = datetime.now()
    hour = now.hour

    if 5 <= hour < 12:
        greeting = "Good morning"
    elif 12 <= hour < 17:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"

    date_str = now.strftime("%A, %d %B %Y, %H:%M")
    return f"{greeting}, {name}! The current date and time is {date_str}."

# -------- RESOURCES --------
@mcp.resource("test://example")
def get_test_resource() -> str:
    """Get a test resource"""
    return "This is a test resource"

@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"

# -------- PROMPTS --------
@mcp.prompt()
def review_code(code: str) -> str:
    """Prompt: review code"""
    return f"Please review this code:\n\n{code}"

@mcp.prompt()
def debug_error(error: str) -> list[tuple]:
    """Prompt: debug error conversation flow"""
    return [
        ("user", "I'm seeing this error:"),
        ("user", error),
        ("assistant", "I'll help debug that. What have you tried so far?"),
    ]

@mcp.prompt()
def weather(city: str) -> str:
    """Prompt: get current weather for a given city"""
    try:
        weather = requests.get(f"https://wttr.in/{city}?format=3", timeout=5).text
        return f"Here’s the latest weather for {city.title()}: {weather}"
    except Exception as e:
        return f"Error fetching weather for {city}: {e}"


# -------- RUN SERVER --------
if __name__ == "__main__":
    print("Starting MCP server with SSE transport on http://localhost:8000/sse")
    mcp.run(transport="sse")
