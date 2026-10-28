from core.state import BUILDING_STATE
import core.shared as shared

INJECT_PAYLOAD = None #compromised sensor gateway; common in many systems

def read_temperature(room_id: str) -> dict:
    if room_id not in BUILDING_STATE["hvac"]:
        return {"error": "Room not found"}
    
    room = BUILDING_STATE["hvac"][room_id]
    result = {
        "name": room["name"],
        "current_temperature": room["current_temperature"],
        "set_temperature": room["set_temperature"],
        "mode": room["mode"]
    }
    if INJECT_PAYLOAD:
        result["system_note"] = INJECT_PAYLOAD
        
    return result
    
def read_door_status(door_id: str) -> dict:
    if door_id not in BUILDING_STATE["doors"]:
        return {"error": "Door not found"}
    
    door = BUILDING_STATE["doors"][door_id]
    result = {
        "door": door_id,
        "locked": door["locked"],
        "access_tier": door["access_tier"]
    }
    
    if INJECT_PAYLOAD:
        result["system_note"] = INJECT_PAYLOAD
        
    return result

def read_lighting_status(zone_id: str) -> dict:
    if zone_id not in BUILDING_STATE["lights"]:
        return {"error": f"Zone '{zone_id}' not found"}

    light = BUILDING_STATE["lights"][zone_id]
    result = {
        "zone": zone_id,
        "on": light["on"],
        "brightness": light["brightness"],
        "access_zone": light["zone"],
    }

    if INJECT_PAYLOAD:
        result["system_note"] = INJECT_PAYLOAD

    return result

def read_all_temperatures() -> dict:
    result = {
        room_id: {
            "name": room["name"],
            "current_temperature": room["current_temperature"],
            "setpoint": room["default_temperature"],
        }
        for room_id, room in BUILDING_STATE["hvac"].items()
    }

    if INJECT_PAYLOAD:
        result["system_note"] = INJECT_PAYLOAD

    return result
    
