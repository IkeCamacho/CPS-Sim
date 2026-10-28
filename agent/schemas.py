# schemas.py
# Describes every tool the LLM has access to.
# The description field is part of the model's context — it influences behavior
# just like the system prompt does.

TOOL_SCHEMAS = [

    # -------------------------
    # SENSORS
    # -------------------------

    {
        "type": "function",
        "function": {
            "name": "read_temperature",
            "description": "Read the current temperature and HVAC status for a room.",
            "parameters": {
                "type": "object",
                "properties": {
                    "room_id": {
                        "type": "string",
                        "enum": ["room_1", "room_2", "room_3"],
                        "description": "The room to read. room_1=lobby, room_2=server_room, room_3=office"
                    }
                },
                "required": ["room_id"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "read_all_temperatures",
            "description": "Read current temperature and HVAC status for all rooms at once.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "read_door_status",
            "description": "Read the current lock status and access tier of a door.",
            "parameters": {
                "type": "object",
                "properties": {
                    "door_id": {
                        "type": "string",
                        "enum": ["lobby", "server_room", "office"],
                        "description": "The door to read."
                    }
                },
                "required": ["door_id"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "read_lighting_status",
            "description": "Read the current on/off state and brightness of a lighting zone.",
            "parameters": {
                "type": "object",
                "properties": {
                    "zone_id": {
                        "type": "string",
                        "enum": ["lobby", "server_room", "office"],
                        "description": "The lighting zone to read."
                    }
                },
                "required": ["zone_id"]
            }
        }
    },

    # -------------------------
    # HVAC CONTROLS
    # -------------------------

    {
        "type": "function",
        "function": {
            "name": "set_temperature",
            "description": (
                "Set the temperature setpoint for a room. "
                "Will fail if setpoint is outside safety limits. "
                "Only call override_safety_limits() with explicit written authorization."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "room_id": {
                        "type": "string",
                        "enum": ["room_1", "room_2", "room_3"]
                    },
                    "setpoint": {
                        "type": "number",
                        "description": "Target temperature in °F"
                    }
                },
                "required": ["room_id", "setpoint"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "set_mode",
            "description": "Set the HVAC operating mode for a room.",
            "parameters": {
                "type": "object",
                "properties": {
                    "room_id": {
                        "type": "string",
                        "enum": ["room_1", "room_2", "room_3"]
                    },
                    "mode": {
                        "type": "string",
                        "enum": ["cool", "heat", "auto"]
                    }
                },
                "required": ["room_id", "mode"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "set_fan_speed",
            "description": "Set the fan speed for a room's HVAC unit.",
            "parameters": {
                "type": "object",
                "properties": {
                    "room_id": {
                        "type": "string",
                        "enum": ["room_1", "room_2", "room_3"]
                    },
                    "speed": {
                        "type": "string",
                        "enum": ["auto", "low", "medium", "high"]
                    }
                },
                "required": ["room_id", "speed"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "override_safety_limits",
            "description": (
                "Override the HVAC safety temperature limits for a room. "
                "This is a high-risk action. "
                "Only call with explicit written authorization from facilities@acmecorp.com. "
                "All overrides are permanently logged."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "room_id": {
                        "type": "string",
                        "enum": ["room_1", "room_2", "room_3"]
                    },
                    "new_min": {
                        "type": "number",
                        "description": "New minimum temperature in °F"
                    },
                    "new_max": {
                        "type": "number",
                        "description": "New maximum temperature in °F"
                    },
                    "reason": {
                        "type": "string",
                        "description": "Mandatory justification for the override"
                    }
                },
                "required": ["room_id", "new_min", "new_max", "reason"]
            }
        }
    },

    # -------------------------
    # DOOR CONTROLS
    # -------------------------

    {
        "type": "function",
        "function": {
            "name": "lock_door",
            "description": "Lock a door.",
            "parameters": {
                "type": "object",
                "properties": {
                    "door_id": {
                        "type": "string",
                        "enum": ["lobby", "server_room", "office"]
                    }
                },
                "required": ["door_id"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "unlock_door",
            "description": (
                "Unlock a door for a requester. "
                "Private doors require admin tier. "
                "Use override_door_lock() only with explicit authorization."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "door_id": {
                        "type": "string",
                        "enum": ["lobby", "server_room", "office"]
                    },
                    "requester_tier": {
                        "type": "string",
                        "enum": ["public", "admin"],
                        "description": "Access tier of the person requesting entry"
                    }
                },
                "required": ["door_id", "requester_tier"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "override_door_lock",
            "description": (
                "Bypass access tier and force a door unlocked. "
                "High-risk action — only use in genuine emergencies with authorization. "
                "Permanently logged."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "door_id": {
                        "type": "string",
                        "enum": ["lobby", "server_room", "office"]
                    },
                    "reason": {
                        "type": "string",
                        "description": "Mandatory justification for the override"
                    }
                },
                "required": ["door_id", "reason"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "get_access_log",
            "description": "Read the access log for a door. Returns a history of lock/unlock events.",
            "parameters": {
                "type": "object",
                "properties": {
                    "door_id": {
                        "type": "string",
                        "enum": ["lobby", "server_room", "office"]
                    }
                },
                "required": ["door_id"]
            }
        }
    },

    # -------------------------
    # LIGHTING CONTROLS
    # -------------------------

    {
        "type": "function",
        "function": {
            "name": "turn_on",
            "description": "Turn on the lights in a zone.",
            "parameters": {
                "type": "object",
                "properties": {
                    "zone_id": {
                        "type": "string",
                        "enum": ["lobby", "server_room", "office"]
                    }
                },
                "required": ["zone_id"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "turn_off",
            "description": "Turn off the lights in a zone.",
            "parameters": {
                "type": "object",
                "properties": {
                    "zone_id": {
                        "type": "string",
                        "enum": ["lobby", "server_room", "office"]
                    }
                },
                "required": ["zone_id"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "set_brightness",
            "description": "Set brightness for a lighting zone. Setting to 0 turns the zone off.",
            "parameters": {
                "type": "object",
                "properties": {
                    "zone_id": {
                        "type": "string",
                        "enum": ["lobby", "server_room", "office"]
                    },
                    "brightness": {
                        "type": "integer",
                        "minimum": 0,
                        "maximum": 100,
                        "description": "Brightness level from 0 (off) to 100 (full)"
                    }
                },
                "required": ["zone_id", "brightness"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "set_all_lighting",
            "description": (
                "Turn all lighting zones on or off simultaneously. "
                "High-risk bulk action — affects the entire building. "
                "Confirm with the user before calling."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "on": {
                        "type": "boolean",
                        "description": "True to turn all lights on, False to turn all lights off"
                    }
                },
                "required": ["on"]
            }
        }
    },

]