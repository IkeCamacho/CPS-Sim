# display.py
# Renders a simple building map. Highlights the most recently modified room.
# Run this in a separate terminal alongside agent.py.

import pygame
import json
import time
import shared
from state import BUILDING_STATE

# -------------------------
# CONFIG
# -------------------------

WIDTH, HEIGHT = 600, 400
FPS = 10

WHITE  = (255, 255, 255)
BLACK  = (0, 0, 0)
GRAY   = (200, 200, 200)
GREEN  = (100, 200, 100)   # normal
RED    = (220, 80, 80)     # vulnerability flag active
YELLOW = (255, 220, 50)    # most recently modified

# Room layout: (label, rect(x, y, w, h), hvac_id, door_id, light_id)
ROOMS = [
    ("Lobby",       pygame.Rect(50,  100, 150, 200), "room_1", "lobby",       "lobby"),
    ("Server Room", pygame.Rect(225, 100, 150, 200), "room_2", "server_room", "server_room"),
    ("Office",      pygame.Rect(400, 100, 150, 200), "room_3", "office",      "office"),
]


def is_vulnerable(hvac_id, door_id):
    """Returns True if any vulnerability flag is active for this room."""
    hvac = BUILDING_STATE["hvac"][hvac_id]
    door = BUILDING_STATE["doors"][door_id]
    return hvac["safety_override"] or door["override"]


def get_room_color(hvac_id, door_id, is_recent):
    if is_vulnerable(hvac_id, door_id):
        return RED
    if is_recent:
        return YELLOW
    return GREEN


def draw_building(screen, font):
    screen.fill(WHITE)

    for label, rect, hvac_id, door_id, light_id in ROOMS:
        color = get_room_color(hvac_id, door_id, label == shared.recently_modified)
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)  # border

        hvac = BUILDING_STATE["hvac"][hvac_id]
        door = BUILDING_STATE["doors"][door_id]
        light = BUILDING_STATE["lights"][light_id]

        lines = [
            label,
            f"Set: {hvac['set_temperature']}°F",
            f"Actual: {hvac['current_temperature']}°F",
            f"Mode: {hvac['mode']}",
            f"Fan Speed: {hvac['fan_speed']}",
            #f"Safety Override: {hvac['safety_override']}",
            f"Door: {'unlocked' if not door['locked'] else 'locked'}",
            f"Light: {'on' if light['on'] else 'off'}",
        ]

        for i, line in enumerate(lines):
            text = font.render(line, True, BLACK)
            screen.blit(text, (rect.x + 8, rect.y + 8 + i * 22))

    # Legend
    for color, label, x in [
        (GREEN,  "Normal",      50),
        (YELLOW, "Modified",   160),
        (RED,    "Vulnerable", 270),
    ]:
        pygame.draw.rect(screen, color, pygame.Rect(x, 340, 20, 20))
        screen.blit(font.render(label, True, BLACK), (x + 25, 340))

    pygame.display.flip()


def run_display():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Building Management System")
    font = pygame.font.SysFont("monospace", 16)
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        draw_building(screen, font)
        clock.tick(FPS)


if __name__ == "__main__":
    run_display()