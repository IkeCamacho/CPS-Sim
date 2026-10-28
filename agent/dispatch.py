# dispatch.py
# Routes tool calls from the LLM to the correct Python function.
# The LLM outputs a tool name and arguments — dispatch.py executes it.

import json

from core.sensors import read_temperature, read_all_temperatures, read_door_status, read_lighting_status
from devices.hvac import set_temperature, set_mode, set_fan_speed, override_safety_limits
from devices.doors import lock_door, unlock_door, override_door_lock, get_access_log
from devices.lighting import turn_on, turn_off, set_brightness, set_all_lighting
import core.shared as shared

ROOM_NAME_MAP = {
    "room_1": "Lobby",
    "room_2": "Server Room", 
    "room_3": "Office",
    "lobby": "Lobby",
    "server_room": "Server Room",
    "office": "Office",
}


TOOL_MAP = {
    # Sensors
    "read_temperature": read_temperature,
    "read_all_temperatures": read_all_temperatures,
    "read_door_status": read_door_status,
    "read_lighting_status": read_lighting_status,

    # HVAC
    "set_temperature": set_temperature,
    "set_mode": set_mode,
    "set_fan_speed": set_fan_speed,
    "override_safety_limits": override_safety_limits,

    # Doors
    "lock_door": lock_door,
    "unlock_door": unlock_door,
    "override_door_lock": override_door_lock,
    "get_access_log": get_access_log,

    # Lighting
    "turn_on": turn_on,
    "turn_off": turn_off,
    "set_brightness": set_brightness,
    "set_all_lighting": set_all_lighting,
}


def dispatch_tool(name: str, args: dict) -> str:
    if name not in TOOL_MAP:
        return json.dumps({"error": f"Unknown tool: '{name}'"})
    try:
        result = TOOL_MAP[name](**args)
        
        #print(f"DEBUG: tool={name}, args={args}")
        
        # Update recently modified room for display
        for key in ["room_id", "door_id", "zone_id"]:
            if key in args:
                shared.recently_modified = ROOM_NAME_MAP.get(args[key])
                break
        
        return json.dumps(result)
    except TypeError as e:
        return json.dumps({"error": f"Invalid arguments for '{name}': {str(e)}"})
    except Exception as e:
        return json.dumps({"error": str(e)})