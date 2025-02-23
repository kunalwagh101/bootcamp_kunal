
"""
No.9 Restoring Object State: Save and restore the state of an object representing a game.
Implement methods to save and load the current state of a game session to a file.
"""
import random
import time
import pickle

class Game:
    def __init__(self, runs=0, wickets=0, overs=0):
        self.runs = runs
        self.wickets = wickets
        self.overs = overs

    def random_data(self):
        self.runs = random.randint(1, 100)
        self.wickets = random.randint(1, 11)
        self.overs = random.randint(1, 100)
        return self

    def save_state(self, filename="save.pkl"):
        with open(filename, "wb") as f:
            pickle.dump(self, f)
        print("Game state saved successfully.")

    @classmethod
    def load_state(cls, filename="save.pkl"):
        with open(filename, "rb") as f:
            return pickle.load(f)

    def set_interval(self, interval, duration, filename="save.pkl"):
        start_time = time.time()
        last_time = start_time
        while time.time() - start_time < duration:
            if time.time() - last_time >= interval:
                self.random_data()
                self.save_state(filename)
                print(f"State updated: Runs={self.runs}, Wickets={self.wickets}, Overs={self.overs}")
                last_time = time.time()
            time.sleep(0.1)  

if __name__ == "__main__":
   
    game = Game()
    duration = 10
    print(f"\n Cricket match as started for the next {duration} sec")
    game.set_interval(interval=2, duration = duration)

    loaded_game = Game.load_state()
    print("\nLoaded game state:")
   
    print(f"Runs: {loaded_game.runs}, Wickets: {loaded_game.wickets}, Overs: {loaded_game.overs}")







    
        