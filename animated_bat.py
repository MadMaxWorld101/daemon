class AnimatedBat:
    def __init__(self):
        # Initial stats for the bat
        self.hp = 100
        self.energy = 100
        self.x = 10
        self.y = 5
        self.dx = 1  # Horizontal speed
        self.dy = 0.5  # Vertical speed
        self.current_frame = 0
        self.animation_counter = 0
        self.is_feeding = False
        self.feeding_duration = 5  # Set feeding duration (in frames)
        self.feeding_counter = 0  # To track feeding state
        self.happy_emoji = "😊"  # Happy emoji to show when feeding

        # Bat animation frames
        self.flying_frames = [
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
        self.eating_frames = [
            ["   /()\\   ",
             "  /*__*\\  ",
             "   O<<v   "]
        ]
    
    def get_current_frame(self):
        if self.is_feeding:
            return self.eating_frames[0]
        return self.flying_frames[self.current_frame]
    
    def update_position(self, screen_width, screen_height):
        if not self.is_feeding:
            # Normal flying position update
            self.x += self.dx
            self.y += self.dy
            
            # Bounce off walls if necessary
            if self.x <= 0 or self.x >= screen_width - 12:
                self.dx *= -1
            if self.y <= 0 or self.y >= screen_height - 4:
                self.dy *= -1
            
            # Ensure bat stays within bounds
            self.x = max(1, min(self.x, screen_width - 12))
            self.y = max(1, min(self.y, screen_height - 4))
        else:
            # If feeding, move downward until feeding is finished
            self.dy = 0.2  # Slow downward movement while feeding
            if self.feeding_counter < self.feeding_duration:
                self.y += self.dy  # Move bat downward
                self.feeding_counter += 1
            else:
                self.is_feeding = False  # Stop feeding after the duration
                self.dy = 0.5  # Restore flying speed

    def update_animation(self):
        # Update animation frame only if not feeding
        if not self.is_feeding:
            self.animation_counter += 1
            if self.animation_counter >= 4:  # Speed of animation
                self.current_frame = (self.current_frame + 1) % len(self.flying_frames)
                self.animation_counter = 0
    
    def start_feeding(self):
        self.is_feeding = True
        self.feeding_counter = 0  # Reset feeding counter
        self.dy = 0.2  # Ensure downward movement during feeding
    
    def stop_feeding(self):
        self.is_feeding = False
        self.dy = 0.5  # Restore flying speed
    
    def draw(self, stdscr):
        # Draw the bat in its current position
        stdscr.addstr(self.y, self.x, self.get_current_frame()[0])  # First line of bat animation
        
        if self.is_feeding:
            # Show happy emoji when feeding
            stdscr.addstr(self.y, self.x + 2, self.happy_emoji)