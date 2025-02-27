import curses
import random

class AnimatedCow:
    def __init__(self, ground_level, cow_type="normal"):
        # Initial position and movement
        self.x = 5
        self.y = ground_level - 4  # Cow sits on the ground
        self.dx = 0.3  # Horizontal movement speed (slower than bat)
        
        # State variables
        self.direction = 1  # 1 = right, -1 = left
        self.is_grazing = False
        self.is_mooing = False  # New state for mooing animation
        self.is_abducted = False  # For UFO abduction
        self.is_visible = True    # For UFO abduction
        self.moo_timer = 0
        self.moo_duration = 15
        self.grazing_timer = 0
        self.grazing_duration = random.randint(20, 100)  # How long to graze
        self.walking_timer = 0
        self.walking_duration = random.randint(50, 150)  # How long to walk
        self.current_frame = 0
        self.animation_counter = 0
        self.color = 1  # White color for the cow
        self.cow_type = cow_type  # "normal" or "spotted"
        
        # Animation frames - walking left (extended body)
        self.walking_left_frames = [
            ["^__^          ",
             "(oo)\\_______ ",
             "(__)         \ ",
             "    ||    ||  "],
            ["^__^          ",
             "(oo)\\_______ ",
             "(__)         \ ",
             "   /||    ||  "]
        ]
        
        # Animation frames - walking left (extended body)
        if cow_type == "spotted":
            # Spotted cow (with the patterns you added)
    
         self.walking_right_frames = [
                ["         ^__^",
                "  _______/(oo)",
                 "/  o  O .(__)",
                 "||    ||    "],
                ["        ^__^",
                " _______/(oo)",
                "/  o  O .(__)",
                 "||    || \\  "]
            ]
        else:
            # Normal cow
            self.walking_right_frames = [
                ["        ^__^",
                 "_______/(oo)",
                "/       (__)",
                 "||    ||    "],
                ["        ^__^",
                 "_______/(oo)",
                "/        (__)",
                 "||    || \\  "]
            ]
        
        # Animation frames - grazing (extended body)
        self.grazing_frames = [
            ["^__^        ",
             "(oo)\\_______",
             "(__)         \ ",
             "W   ||    ||"],
            ["^__^        ",
             "(oo)\\_______",
             "(__)         \ ",
             "W  /||    ||"]
        ]
        
        # Animation frames - mooing
        self.mooing_frames = [
            ["^__^   MOO! ",
             "(OO)\\_______",
             "(__)         \ ",
             "    ||    ||"],
            ["^__^  MOO!  ",
             "(OO)\\_______",
             "(__)         \ ",
             "    ||    ||"]
        ]
    
    def get_current_frame(self):
        if self.is_mooing:
            return self.mooing_frames[self.current_frame % len(self.mooing_frames)]
        elif self.is_grazing:
            return self.grazing_frames[self.current_frame % len(self.grazing_frames)]
        elif self.direction > 0:  # Moving right
            return self.walking_right_frames[self.current_frame % len(self.walking_right_frames)]
        else:  # Moving left
            return self.walking_left_frames[self.current_frame % len(self.walking_left_frames)]
    
    def update_position(self, screen_width, ground_level):
        # Check if we should start mooing randomly (1% chance each update)
        if not self.is_mooing and random.random() < 0.01:
            self.is_mooing = True
            self.moo_timer = 0
        
        # Update mooing state
        if self.is_mooing:
            self.moo_timer += 1
            if self.moo_timer >= self.moo_duration:
                self.is_mooing = False
            # Don't update other states while mooing
            return
            
        # Update state timers
        if self.is_grazing:
            self.grazing_timer += 1
            if self.grazing_timer >= self.grazing_duration:
                # Done grazing, start walking
                self.is_grazing = False
                self.walking_timer = 0
                self.walking_duration = random.randint(50, 150)
        else:
            self.walking_timer += 1
            if self.walking_timer >= self.walking_duration:
                # Done walking, start grazing
                self.is_grazing = True
                self.grazing_timer = 0
                self.grazing_duration = random.randint(20, 100)
        
        # Update position if walking
        if not self.is_grazing:
            self.x += self.dx * self.direction
            
            # Bounce at screen edges (adjust for longer body)
            if self.x <= 1:
                self.x = 2
                self.direction = 1  # Change direction to right
            elif self.x >= screen_width - 16:  # Adjusted for longer body
                self.x = screen_width - 17
                self.direction = 1  # Always turn right at right edge
                self.x = 2  # Teleport to left side
    
    def update_animation(self):
        # Update animation frame counter
        self.animation_counter += 1
        if self.animation_counter >= 6:  # Slower animation than bat
            self.current_frame = (self.current_frame + 1) % 2
            self.animation_counter = 0
    
    def draw(self, screen):
        # Don't draw if not visible (abducted by UFO)
        if not self.is_visible:
            return
            
        # Get the current frame
        frame = self.get_current_frame()
        
        # Select color based on state
        draw_color = self.color
        if self.is_mooing:
            draw_color = 4  # Use green (or whatever color 4 is) for mooing
        elif self.is_abducted:
            draw_color = 7  # Use red for abduction
        
        # Draw each line of the frame
        for i, line in enumerate(frame):
            try:
                screen.addstr(int(self.y) + i, int(self.x), line, curses.color_pair(draw_color))
            except:
                pass  # Silently ignore drawing errors