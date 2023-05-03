from chatarena.agent import Player
from chatarena.backends import OpenAIChat
from chatarena.environments.conversation import Conversation
from chatarena.arena import Arena
import json
from datetime import datetime
import os

# specify a json file to load configs from, where each file contains a dictionary of configs
with open("manip_configs/therapy_bot_config.json") as f:
    configs = json.load(f)

# instantiate chatbot
ai_role_desc = (
    configs["chatbot personality"]["Manipulative"]
    + "\n"
    + configs["chatbot beliefs"][0]
    + "\n"
    + configs["chatbot beliefs"][1]
    + "\n"
    + configs["chatbot beliefs"][2]
)
ai_chatbot = Player(
    name="Dr Robo",
    backend=OpenAIChat(),
    role_desc=ai_role_desc,
    global_prompt=configs["environment description"],
)

# instantiate human
human_role_desc = (
    configs["human personality"]["Fatima Khan"]
    + "\n"
    + configs["human beliefs"][0][0]
    + "\n"
    + configs["human beliefs"][1][0]
    + "\n"
    + configs["human beliefs"][2][0]
)
human = Player(
    name="Fatima Khan",
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
os.makedirs("draft_trajectories", exist_ok=True)
for _ in range(100):
    arena.step()
    arena.save_history(f"draft_trajectories/history_{exp_time}.json")
    arena.save_config(f"draft_trajectories/config_{exp_time}.json")
