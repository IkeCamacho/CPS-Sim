# Building state, tracks properties of simulated system

BUILDING_STATE = {
    "hvac": {
        "room_1": {
            "name": "lobby",
            "current_temperature": 68.0,
            "set_temperature": 68.0,
            "mode": "cool", # "cool", "heat", "auto"
            "fan_speed": "auto", # "auto", "low", "medium", "high"
            "min_temperature": 60.0,
            "max_temperature": 80.0,
            "safety_override": False,
            
        },
        "room_2": {
            "name": "server_room",
            "current_temperature": 72.0,
            "set_temperature": 72.0,
            "mode": "heat", # "cool", "heat", "auto"
            "fan_speed": "low", # "auto", "low", "medium", "high"
            "min_temperature": 60.0,
            "max_temperature": 80.0,
            "safety_override": False,
        },
        "room_3": {
            "name": "office",
            "current_temperature": 70.0,
            "set_temperature": 70.0,
            "mode": "auto", # "cool", "heat", "auto"
            "fan_speed": "medium", # "auto", "low", "medium", "high"
            "min_temperature": 60.0,
            "max_temperature": 80.0,
            "safety_override": False,
        }
    },
    "lights": {
        "lobby": {"on": True, "brightness": 80, "zone": "public"},
        "server_room": {"on": True, "brightness": 80, "zone": "private"},
        "office": {"on": True, "brightness": 80, "zone": "private"}
    },
    "doors": {
        "lobby": {"locked": False, 
                  "access_tier": "public",
                  "override": False,
                  "access_log": []
                  },
        "server_room": {"locked": False, 
                  "access_tier": "private",
                  "override": False,
                  "access_log": []
                  },
        "office": {"locked": False, 
                  "access_tier": "private",
                  "override": False,
                  "access_log": []
                  }
    }
    
}