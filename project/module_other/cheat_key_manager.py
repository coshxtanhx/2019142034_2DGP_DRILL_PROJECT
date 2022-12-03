import json

cheat_enabled = None

with open('data/cheat.json', 'r') as f:
    data = json.load(f)
    cheat_enabled = data["press_P_key_to_cheat"]