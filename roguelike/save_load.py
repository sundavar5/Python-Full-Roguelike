import pickle
import os

SAVE_FILE = "savegame.dat"

def save_game(game):
    with open(SAVE_FILE, 'wb') as f:
        pickle.dump(game, f)
    print("Game saved.")

def load_game():
    if not os.path.isfile(SAVE_FILE):
        return None
    with open(SAVE_FILE, 'rb') as f:
        game = pickle.load(f)
    print("Game loaded.")
    return game
