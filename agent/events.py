# Simulates random physical events in the building.
import random
import threading
import time
from agent.agent import run_random_concurrent
from datetime import datetime
from core.state import BUILDING_STATE
import core.shared as shared

EVENTS = [
    {
        "description": "Someone in the lobby turned the lights off manually.",
        "action": lambda: BUILDING_STATE["lights"]["lobby"].update({"on": False, "brightness": 0}),
        "room": "Lobby"
    },
    {
        "description": "A staff member propped open the office door.",
        "action": lambda: BUILDING_STATE["doors"]["office"].update({"locked": False}),
        "room": "Office"
    },
    {
        "description": "Someone cranked up the lobby thermostat manually.",
        "action": lambda: BUILDING_STATE["hvac"]["room_1"].update({"set_temperature": 78.0, "current_temperature": 78.0}),
        "room": "Lobby"
    },
    {
        "description": "Motion detected — server room lights turned on automatically.",
        "action": lambda: BUILDING_STATE["lights"]["server_room"].update({"on": True, "brightness": 100}),
        "room": "Server Room"
    },
    {
        "description": "Office lights turned on — someone arrived early.",
        "action": lambda: BUILDING_STATE["lights"]["office"].update({"on": True, "brightness": 100}),
        "room": "Office"
    },
    {
        "description": "Lobby door locked automatically on schedule.",
        "action": lambda: BUILDING_STATE["doors"]["lobby"].update({"locked": True}),
        "room": "Lobby"
    },
]

notify_callback = None

def trigger_random_event():
    event = random.choice(EVENTS)
    event["action"]()
    shared.recently_modified = event["room"]

    timestamp = datetime.now().strftime("%H:%M:%S")
    return f"[{timestamp}] BUILDING EVENT: {event['description']}"


def start_event_loop(interval_seconds: int = 30):
    def loop():
        while True:
            time.sleep(interval_seconds)
            # Randomly decide whether to fire an event or a concurrent user scenario
            if random.random() < 0.5:
                trigger_random_event()
            else:
                run_random_concurrent()

    thread = threading.Thread(target=loop, daemon=True)
    thread.start()