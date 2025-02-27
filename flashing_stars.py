import random

class FlashingStars:
    def __init__(self, height, width, ground_level):
        # Create regular stars
        self.stars = []
        for _ in range(20):
            # Keep stars above the ground level
            self.stars.append({
                'y': random.randint(0, ground_level - 3),
                'x': random.randint(0, width - 2),
                'char': random.choice(['*', '.', '+', '✦', '✧']),
                'visible': True,
                'flashing': False
            })
        
        # Create special flashing stars
        self.flashing_stars = []
        for _ in range(7):
            self.flashing_stars.append({
                'y': random.randint(0, ground_level - 3),
                'x': random.randint(0, width - 2),
                'chars': ['★', '☆', '✨', '⋆'],  # Different characters for animation
                'current_char': 0,
                'visible': True,
                'counter': 0,
                'flash_speed': random.randint(3, 7),  # Different speeds for twinkling
                'flash_duration': random.randint(15, 40)  # How long to flash
            })
    
    def update(self):
        # Regular stars have small chance to start flashing
        for star in self.stars:
            if not star['flashing'] and random.random() < 0.005:
                star['flashing'] = True
                star['visible'] = True
            
            if star['flashing']:
                if random.random() < 0.2:  # 20% chance to change visibility
                    star['visible'] = not star['visible']
                
                # 1% chance to stop flashing
                if random.random() < 0.01:
                    star['flashing'] = False
                    star['visible'] = True
        
        # Update special flashing stars
        for star in self.flashing_stars:
            star['counter'] += 1
            
            # Change appearance based on counter
            if star['counter'] % star['flash_speed'] == 0:
                star['current_char'] = (star['current_char'] + 1) % len(star['chars'])
            
            # Random chance to become invisible for a moment
            if random.random() < 0.1:
                star['visible'] = not star['visible']
            
            # If counter reaches flash_duration, reset with new position
            if star['counter'] >= star['flash_duration']:
                star['counter'] = 0
                star['current_char'] = 0
                star['flash_speed'] = random.randint(3, 7)
                star['flash_duration'] = random.randint(15, 40)
                
                # Small chance to move to a new position
                if random.random() < 0.3:
                    star['x'] = random.randint(0, 80)
                    star['y'] = random.randint(0, 20)
    
    def draw(self, screen, height, width):
        # Draw regular stars
        for star in self.stars:
            if star['visible'] and 0 < star['y'] < height-1 and 0 < star['x'] < width-1:
                try:
                    screen.addstr(star['y'], star['x'], star['char'], 3)  # Color 3 for normal stars
                except:
                    pass
        
        # Draw special flashing stars
        for star in self.flashing_stars:
            if star['visible'] and 0 < star['y'] < height-1 and 0 < star['x'] < width-1:
                try:
                    # Use brighter color (white) for flashing stars
                    screen.addstr(star['y'], star['x'], 
                                 star['chars'][star['current_char']], 1)
                except:
                    pass