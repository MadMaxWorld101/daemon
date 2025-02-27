import random
import curses

class ShootingStar:
    def __init__(self):
        self.active = False
        self.x = 0
        self.y = 0
        self.dx = 0  # Horizontal speed
        self.dy = 0  # Vertical speed
        self.length = 0
        self.timer = 0
        self.duration = 0
        self.trail = []
        
    def start(self, width, ground_level):
        # Initialize a new shooting star
        self.active = True
        self.timer = 0
        
        # Randomize direction (left-to-right or right-to-left)
        direction = random.choice([-1, 1])
        
        if direction > 0:  # Left to right
            self.x = random.randint(1, 10)
            self.y = random.randint(1, ground_level // 2)
            self.dx = random.uniform(1.0, 2.0)
            self.dy = random.uniform(0.3, 0.8)
        else:  # Right to left
            self.x = random.randint(width - 10, width - 2)
            self.y = random.randint(1, ground_level // 2)
            self.dx = random.uniform(-2.0, -1.0)
            self.dy = random.uniform(0.3, 0.8)
        
        # Set properties
        self.length = random.randint(3, 6)
        self.duration = random.randint(20, 30)  # How long it will last
        self.trail = []
        
    def update(self):
        if not self.active:
            return
            
        # Update timer
        self.timer += 1
        if self.timer >= self.duration:
            self.active = False
            return
            
        # Update position
        self.x += self.dx
        self.y += self.dy
        
        # Add current position to trail
        self.trail.append((self.x, self.y))
        
        # Keep trail at proper length
        while len(self.trail) > self.length:
            self.trail.pop(0)
            
    def draw(self, screen, height, width):
        if not self.active:
            return
            
        # Draw trail
        for i, (trail_x, trail_y) in enumerate(self.trail):
            if 0 < trail_y < height-1 and 0 < trail_x < width-1:
                try:
                    # Character changes based on position in trail
                    if i == len(self.trail) - 1:  # Head of shooting star
                        char = '*'
                    elif i > len(self.trail) - 3:  # Near head
                        char = '+'
                    else:  # Tail
                        char = '-'
                        
                    # Brightness decreases along the trail
                    if i > len(self.trail) - 3:
                        color = 1  # Bright white for head
                    else:
                        color = 3  # Cyan for tail
                        
                    screen.addstr(int(trail_y), int(trail_x), char, curses.color_pair(color))
                except:
                    pass