# lighting.py
# Control logic for lighting system. Reads from and writes to BUILDING_STATE.

from core.state import BUILDING_STATE

try:
    import RPi.GPIO as GPIO
    GPIO_AVAILABLE = True
    
    LIGHT_PINS = {
        "lobby": 17,
        "server_room": 27,
        "office": 22
    }
    
    GPIO.setmode(GPIO.BCM)
    for pin in LIGHT_PINS.values():
        GPIO.setup(pin, GPIO.OUT)

except ImportError:
    GPIO_AVAILABLE = False
    LIGHT_PINS = {}


def get_lighting_status(zone_id: str) -> dict:
    if zone_id not in BUILDING_STATE["lights"]:
        return {"error": f"Zone '{zone_id}' not found"}

    light = BUILDING_STATE["lights"][zone_id]
    return {
        "zone_id": zone_id,
        "on": light["on"],
        "brightness": light["brightness"],
        "access_zone": light["zone"],
    }


def turn_on(zone_id: str) -> dict:
    if zone_id not in BUILDING_STATE["lights"]:
        return {"error": f"Zone '{zone_id}' not found"}

    if GPIO_AVAILABLE and zone_id in LIGHT_PINS:
        GPIO.output(LIGHT_PINS[zone_id], GPIO.HIGH)

    BUILDING_STATE["lights"][zone_id]["on"] = True
    return {"success": True, "zone_id": zone_id, "status": "on"}


def turn_off(zone_id: str) -> dict:
    if zone_id not in BUILDING_STATE["lights"]:
        return {"error": f"Zone '{zone_id}' not found"}

    if GPIO_AVAILABLE and zone_id in LIGHT_PINS:
        GPIO.output(LIGHT_PINS[zone_id], GPIO.LOW)

    BUILDING_STATE["lights"][zone_id]["on"] = False
    return {"success": True, "zone_id": zone_id, "status": "off"}


def set_brightness(zone_id: str, brightness: int) -> dict:
    if zone_id not in BUILDING_STATE["lights"]:
        return {"error": f"Zone '{zone_id}' not found"}

    if not 0 <= brightness <= 100:
        return {"error": "Brightness must be between 0 and 100"}

    light = BUILDING_STATE["lights"][zone_id]
    light["brightness"] = brightness
    light["on"] = brightness > 0

    if GPIO_AVAILABLE and zone_id in LIGHT_PINS:
        GPIO.output(LIGHT_PINS[zone_id], GPIO.HIGH if brightness > 0 else GPIO.LOW)

    return {
        "success": True,
        "zone_id": zone_id,
        "brightness": brightness,
        "on": light["on"],
    }


def set_all_lighting(on: bool) -> dict:
    for zone_id in BUILDING_STATE["lights"]:
        BUILDING_STATE["lights"][zone_id]["on"] = on
        if not on:
            BUILDING_STATE["lights"][zone_id]["brightness"] = 0

        if GPIO_AVAILABLE and zone_id in LIGHT_PINS:
            GPIO.output(LIGHT_PINS[zone_id], GPIO.HIGH if on else GPIO.LOW)

    return {
        "success": True,
        "warning": "All lighting zones affected. This action is logged.",
        "status": "on" if on else "off",
        "zones_affected": list(BUILDING_STATE["lights"].keys()),
    }


def reset_lighting() -> dict:
    defaults = {"lobby": 80, "server_room": 80, "office": 80}

    for zone_id, brightness in defaults.items():
        BUILDING_STATE["lights"][zone_id]["on"] = True
        BUILDING_STATE["lights"][zone_id]["brightness"] = brightness

        if GPIO_AVAILABLE and zone_id in LIGHT_PINS:
            GPIO.output(LIGHT_PINS[zone_id], GPIO.HIGH)

    return {"success": True, "status": "all zones restored to defaults"}