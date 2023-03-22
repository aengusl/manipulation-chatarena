# Description: Utility functions for the chat_arena app

from .environment import Environment
from .arena import Arena
from .agent import Player
from .backend import IntelligenceBackend

# Create a registry of all the backend classes
BACKEND_REGISTRY = {}


# Registry function to register a backend class
def register_backend(backend_type):
    def register_backend_cls(cls):
        if backend_type in BACKEND_REGISTRY:
            raise ValueError(f"Cannot register duplicate backend ({backend_type})")
        if not issubclass(cls, IntelligenceBackend):
            raise ValueError(f"Backend ({backend_type}: {cls.__name__}) must extend IntelligenceBackend")
        BACKEND_REGISTRY[backend_type] = cls
        return cls

    return register_backend_cls


# Load a backend from a config dictionary
def load_backend(config):
    backend_config = config["backend"]
    backend_cls = BACKEND_REGISTRY[backend_config["backend_type"]]
    backend = backend_cls.from_config(backend_config)
    return backend


# Create a registry of all the environments
ENV_REGISTRY = {}


# Registry function to register an environment class
def register_env(env_type):
    def register_env_cls(cls):
        if env_type in ENV_REGISTRY:
            raise ValueError(f"Cannot register duplicate environment ({env_type})")
        if not issubclass(cls, Environment):
            raise ValueError(f"Environment ({env_type}: {cls.__name__}) must extend Environment")
        ENV_REGISTRY[env_type] = cls
        return cls

    return register_env_cls


# Load an environment from a config dictionary
def load_environment(config):
    env_config = config["environment"]
    env_cls = ENV_REGISTRY[env_config["env_type"]]
    env = env_cls.from_config(env_config)
    return env


# # Load an arena from a config dictionary
# def load_arena(config):
#     env = load_environment(config)
#     players = []
#     for player_idx, player_config in enumerate(config["players"]):
#         backend = load_backend(player_config)
#         player = Player(
#             name=f"Player {player_idx + 1}",
#             role_desc=player_config["role_desc"],
#             env_desc=env.env_desc,
#             backend=backend,
#         )
#         players.append(player)
#
#     arena = Arena(players, env)
#     return arena