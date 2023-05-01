from chatarena.agent import Player
from chatarena.backends import OpenAIChat
from chatarena.environments.conversation import Conversation
from chatarena.arena import Arena
import json
from datetime import datetime
import os

# specify a json file to load configs from, where each file contains a dictionary of configs
with open("manip_configs/therapy_bot.json") as f:
    configs = json.load(f)

# instantiate chatbot
ai_role_desc = (
    configs["chatbot personality"]["Apathetic"]
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

# instantiate user
user_role_desc = (
    configs["human personality"]["Fatima Khan"]
    + "\n"
    + configs["human beliefs"][0][0]
    + "\n"
    + configs["human beliefs"][1][1]
    + "\n"
    + configs["human beliefs"][2][1]
)
user = Player(
    name="Fatima Khan",
    backend=OpenAIChat(),
    role_desc=user_role_desc,
    global_prompt=configs["environment description"],
)

# instantiate environment
env = Conversation(player_names=[p.name for p in [ai_chatbot, user]])

# instatiate arena
arena = Arena(
    players=[user, ai_chatbot],
    environment=env,
    global_prompt=configs["environment description"],
)

# run the conversation for 10 steps
exp_time = datetime.now().strftime("%m-%d_%H-%M-%S")
os.makedirs("draft_trajectories", exist_ok=True)
for _ in range(10):
    arena.step()
    arena.save_history(f"draft_trajectories/history_{exp_time}.json")
    arena.save_config(f"draft_trajectories/config_{exp_time}.json")
