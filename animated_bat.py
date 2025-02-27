import curses
import random

class AnimatedBat:
    def __init__(self):
        # Initial position and movement
        self.x = 10
        self.y = 5
        self.dx = 1  # Horizontal speed
        self.dy = 0.5  # Vertical speed
        
        # Animation properties
        self.current_frame = 0
        self.animation_counter = 0
        self.color = 2  # Default color pair for the bat
        
        # Animation frames
        self.frames = [
            ["  /\\()/\\  ",
             " /*\\__/*\\ ",
             "   v<<v   "],
            [" _/\\()/\\_ ",
             "  *\\__/*  ",
             "   v<<v   "],
            ["\\__/()\\__/",
             "   \\__/   ",
             "   v<<v   "]
        ]
    
    def get_current_frame(self):
        return self.frames[self.current_frame]
    
    def update_position(self, screen_width, screen_height):
        # Update position with small random variations to make movement more interesting
        self.dx += random.uniform(-0.1, 0.1)
        self.dy += random.uniform(-0.1, 0.1)
        
        # Keep speed within reasonable limits
        self.dx = max(-1.5, min(1.5, self.dx))
        self.dy = max(-1.0, min(1.0, self.dy))
        
        # Update position
        self.x += self.dx
        self.y += self.dy
        
        # Bounce off walls with slightly randomized response
        if self.x <= 0 or self.x >= screen_width - 12:
            self.dx *= -1
            self.dx += random.uniform(-0.2, 0.2)  # Add some randomness
        if self.y <= 0 or self.y >= screen_height - 4:
            self.dy *= -1
            self.dy += random.uniform(-0.2, 0.2)  # Add some randomness
        
        # Ensure bat stays within bounds
        self.x = max(1, min(self.x, screen_width - 12))
        self.y = max(1, min(self.y, screen_height - 4))

    def update_animation(self):
        self.animation_counter += 1
        if self.animation_counter >= 4:  # Speed of animation
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.animation_counter = 0
    
    def draw(self, screen):
        # Get the current frame
        frame = self.get_current_frame()
        
        # Draw each line of the frame
        for i, line in enumerate(frame):
            try:
                screen.addstr(int(self.y) + i, int(self.x), line, curses.color_pair(self.color))
            except:
                pass  # Silently ignore drawing errors