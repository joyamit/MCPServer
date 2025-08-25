import asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client

async def main():
    async with sse_client("http://localhost:8000/sse") as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as client:
            await client.initialize()

            print("Commands:")
            print("  add X and Y         → uses add_numbers tool")
            print("  greet <name>        → uses greet_user tool")
            print("  resource <name>     → fetch greeting://{name} resource")
            print("  review <code>       → runs review_code prompt")
            print("  debug <error>       → runs debug_error prompt")
            print("  weather kolkata     → runs weather_kolkata prompt")
            print("  exit                → quit")
            print()

            while True:
                user_input = input("> ").strip()
                if user_input.lower() == "exit":
                    break

                # --- TOOLS ---
                if user_input.lower().startswith("add "):
                    try:
                        parts = user_input.split()
                        a = int(parts[1])
                        b = int(parts[3])
                        result = await client.call_tool("add_numbers", {"a": a, "b": b})
                        print(result)
                    except Exception:
                        print("Format: add 2 and 3")

                elif user_input.lower().startswith("greet "):
                    name = user_input.split(" ", 1)[1]
                    result = await client.call_tool("greet_user", {"name": name})
                    print(result)

                # --- RESOURCES ---
                elif user_input.lower().startswith("resource "):
                    name = user_input.split(" ", 1)[1]
                    result = await client.read_resource(f"greeting://{name}")
                    print(result)

                # --- PROMPTS ---
                elif user_input.lower().startswith("review "):
                    code = user_input.split(" ", 1)[1]
                    result = await client.get_prompt("review_code", {"code": code})
                    print(result)

                elif user_input.lower().startswith("debug "):
                    error = user_input.split(" ", 1)[1]
                    result = await client.get_prompt("debug_error", {"error": error})
                    print(result)

                elif user_input.lower().startswith("weather"):
                    parts = user_input.split(" ", 1)
                    if len(parts) == 1:
                        city = input("Which city? ").strip()
                    else:
                        city = parts[1]
                    result = await client.get_prompt("weather", {"city": city})
                    print(result)


                else:
                    print("Sorry, I don't know how to handle that yet.")

if __name__ == "__main__":
    asyncio.run(main())
