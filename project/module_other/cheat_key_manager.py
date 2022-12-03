import json

cheat_enabled = None
try:
    with open('data/cheat.json', 'r') as f:
        data = json.load(f)
        cheat_enabled = data["press_P_key_to_cheat"]
except:
    cheat_enabled = False