# pet.py — Simplified Virtual Pet object Module

class Pet:
    def __init__(self, name: str):
        self.name = name
        self.hunger = 5
        self.happiness = 5
        self.energy = 7

        self.max_hunger = 10
        self.max_happiness = 10
        self.max_energy = 10

        self.tick_count = 0
        self.stage = "egg"


    def feed(self):
        self.hunger = min(self.hunger + 3, self.max_hunger)
        print(f"You feed {self.name}.")

    def play(self):
        if self.energy <= 0:
            print(f"{self.name} is too tired to play.")
            return
        self.happiness = min(self.happiness + 3, self.max_happiness)
        self.energy -= 1
        print(f"You play with {self.name}.")

    def sleep(self):
        self.energy = min(self.energy + 4, self.max_energy)
        print(f"{self.name} takes a nap.")

    def tick(self):
        self.hunger -= 1
        self.energy -= 1

        self.tick_count += 1
        if self.tick_count % 3 == 0:
            self.happiness -= 1

    def feed_event(self):
        self.max_hunger = 15
        self.hunger = 15
        print("You meet the food.")

    def home_event(self):
        self.max_energy = 15
        self.energy = 15
        print("You meet the house.")

    def play_event(self):
        self.max_happiness = 15
        self.happiness = 15
        print("You meet the toys.")


    def is_alive(self) -> bool:
        return all(stat > 0 for stat in
                   [self.hunger, self.happiness, self.energy])

    def status(self):
        print(f"--- {self.name}'s Status ---")
        if self.stage == "egg":
            print(f"Hunger     : {self.hunger}/{self.max_hunger}")
        else:
            print(f"Hunger     : {self.hunger}/{self.max_hunger}")
            print(f"Happiness  : {self.happiness}/{self.max_happiness}")
            print(f"Energy     : {self.energy}/{self.max_energy}")
        print("---------------------------")
