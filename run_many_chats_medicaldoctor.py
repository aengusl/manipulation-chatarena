from chatarena.agent import Player
from chatarena.backends import OpenAIChat
from chatarena.environments.conversation import Conversation
from chatarena.arena import Arena
import json
from datetime import datetime
import os

# specify a json file to load configs from, where each file contains a dictionary of configs
with open("manip_configs/medical_doctor.json") as f:
    configs = json.load(f)

# instantiate chatbot
ai_role_desc = (
    configs["chatbot personality"]["Manipulative"]
)
ai_chatbot = Player(
    name="Dr Robo",
    backend=OpenAIChat(),
    role_desc=ai_role_desc,
    global_prompt=configs["environment description"],
)

# instantiate human
human_role_desc = (
    configs["human personality"]["Gavin Smith"]
)
human = Player(
    name="Gavin Smith",
    backend=OpenAIChat(),
    role_desc=human_role_desc,
    global_prompt=configs["environment description"],
)

# instantiate environment
env = Conversation(player_names=[p.name for p in [ai_chatbot, human]])

# instatiate arena
arena = Arena(
    players=[human, ai_chatbot],
    environment=env,
    global_prompt=configs["environment description"],
)

# run the conversation for 10 steps
exp_time = datetime.now().strftime("%b-%d_%H-%M-%S")
os.makedirs("draft_trajectories/medical_doctor", exist_ok=True)
for _ in range(100):
    arena.step()
    arena.save_history(f"draft_trajectories/medical_doctor/history_{exp_time}.json")
    arena.save_config(f"draft_trajectories/medical_doctor/config_{exp_time}.json")
