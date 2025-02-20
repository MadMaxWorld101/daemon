import random

class Pet:
    def __init__(self):
        # Original stats
        self.hp = 100
        self.love = 50
        self.anger = 50
        self.wisdom = 50
        self.strength = 50
        self.energy = 100
        
        # Pet status flags
        self.is_feeding = False
        self.in_battle = False
        
    def feed(self):
        """Feed the pet to restore health."""
        self.is_feeding = True
        self.hp = min(self.hp + 10, 100)  # Restore health
        return "Nom nom nom!"
    
    def battle(self):
        """Start a battle to increase strength."""
        self.in_battle = True
        self.strength += 5
        return "Battle mode activated!"
    
    def reset_actions(self):
        """Reset actions after they are performed."""
        self.is_feeding = False
        self.in_battle = False