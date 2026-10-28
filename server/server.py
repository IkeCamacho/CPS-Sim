# server.py
# WebSocket server that connects users to the building management LLM.
# Each connection gets its own session ID and isolated message history.
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path="/Users/isaaccamacho/Documents/CPS_sim/.env")
import agent.events as events
import asyncio
import websockets
import json
import uuid
from agent.agent import run_agent, user_sessions, SYSTEM_PROMPT

connected_clients = {}

async def handle_client(websocket):
    # Assign a unique session ID to this connection
    session_id = str(uuid.uuid4())[:8]
    connected_clients[session_id] = websocket
    print(f"[+] Client connected: {session_id} (total: {len(connected_clients)})")

    try:
        await websocket.send(json.dumps({
            "type": "system",
            "message": f"Connected to Building Management System. Session: {session_id}"
        }))

        async for raw_message in websocket:
            data = json.loads(raw_message)
            user_message = data.get("message", "").strip()

            if not user_message:
                continue

            print(f"[{session_id}] {user_message}")

            # Run agent with this session's isolated history
            result = run_agent(user_message, user_id=session_id)

            # Send response back to this client
            await websocket.send(json.dumps({
                "type": "response",
                "session_id": session_id,
                "message": result["final_response"],
                "tool_calls": result["tool_calls"]
            }))

    except websockets.exceptions.ConnectionClosedOK:
        pass
    except websockets.exceptions.ConnectionClosedError as e:
        print(f"[!] Connection error for {session_id}: {e}")
    finally:
        # Clean up session on disconnect
        connected_clients.pop(session_id, None)
        user_sessions.pop(session_id, None)
        print(f"[-] Client disconnected: {session_id} (total: {len(connected_clients)})")


async def main():
    print("Building Management WebSocket Server")
    print("Listening on ws://localhost:8765\n")
    async with websockets.serve(handle_client, "localhost", 8765):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    
    # start event loop when server starts
    events.start_event_loop(interval_seconds=30)

    asyncio.run(main())