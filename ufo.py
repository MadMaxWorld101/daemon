import random
import curses

class UFO:
    def __init__(self):
        self.active = False
        self.x = 0
        self.y = 0
        self.dx = 0
        self.phase = 0  # 0: appearing, 1: hovering, 2: beam, 3: abducting, 4: leaving
        self.timer = 0
        self.target_cow = None
        self.cow_original_x = 0
        self.cow_original_y = 0
        self.beam_width = 5
        self.beam_chars = []
        
        # UFO appearance
        self.ufo_sprite = [
            "   _____   ",
            " /       \\ ",
            "/|  UFO  |\\"
        ]
        
    def start(self, width, cows):
        self.active = True
        self.phase = 0
        self.timer = 0
        
        # Start outside screen on either left or right
        side = random.choice(["left", "right"])
        if side == "left":
            self.x = -15
            self.dx = 0.7
        else:
            self.x = width + 5
            self.dx = -0.7
            
        # Set y position at top of screen
        self.y = 5
        
        # Select a random cow as target
        self.target_cow = random.choice(cows)
        self.cow_original_x = self.target_cow.x
        self.cow_original_y = self.target_cow.y
        
        # Prepare beam characters
        self.beam_chars = ["|", ":", ".", " "]
        
    def update(self, width):
        if not self.active:
            return
            
        self.timer += 1
        
        # Phase 0: Appearing - UFO moves in from off-screen
        if self.phase == 0:
            self.x += self.dx
            
            # Once UFO is above the target cow, stop and hover
            if (self.dx > 0 and self.x > self.cow_original_x - 5) or \
               (self.dx < 0 and self.x < self.cow_original_x - 5):
                self.x = self.cow_original_x - 5  # Center above cow
                self.phase = 1
                self.timer = 0
        
        # Phase 1: Hovering - UFO stays in place for a moment
        elif self.phase == 1:
            if self.timer > 20:
                self.phase = 2  # Start beaming
                self.timer = 0
        
        # Phase 2: Beam - Tractor beam comes down
        elif self.phase == 2:
            if self.timer > 15:
                self.phase = 3  # Start abducting
                self.timer = 0
                
                # Make the target cow start rising
                if self.target_cow:
                    self.target_cow.is_abducted = True
        
        # Phase 3: Abducting - Cow moves up into the UFO
        elif self.phase == 3:
            # Move cow up if it exists
            if self.target_cow and hasattr(self.target_cow, 'is_abducted'):
                self.target_cow.y -= 0.3
                
                # If cow reaches UFO, start leaving
                if self.target_cow.y <= self.y + 3:
                    self.phase = 4
                    self.timer = 0
                    
                    # Hide the cow (it's inside the UFO now)
                    self.target_cow.is_visible = False
        
        # Phase 4: Leaving - UFO flies away
        elif self.phase == 4:
            # Reverse the original direction to leave
            self.x -= self.dx
            
            # If UFO is off-screen, end the event
            if (self.dx > 0 and self.x < -15) or (self.dx < 0 and self.x > width + 15):
                self.active = False
                
                # Respawn the cow after a while
                if self.target_cow:
                    self.target_cow.is_abducted = False
                    self.target_cow.is_visible = True
                    self.target_cow.x = random.randint(10, width - 20)
                    self.target_cow.y = self.cow_original_y
                
    def draw(self, screen, height, width):
        if not self.active:
            return
            
        # Draw UFO
        for i, line in enumerate(self.ufo_sprite):
            try:
                screen.addstr(int(self.y) + i, int(self.x), line, curses.color_pair(6))
            except:
                pass
                
        # Draw tractor beam if in beam or abduction phase
        if self.phase >= 2:
            beam_height = int(self.target_cow.y) - int(self.y) - 3
            
            # Ensure beam height is positive
            if beam_height > 0:
                center_x = int(self.x) + 5
                
                # Draw beam sides
                for y in range(int(self.y) + 3, int(self.target_cow.y)):
                    try:
                        # Left side of beam
                        screen.addstr(y, center_x - self.beam_width // 2, "/", curses.color_pair(3))
                        # Right side of beam
                        screen.addstr(y, center_x + self.beam_width // 2, "\\", curses.color_pair(3))
                    except:
                        pass
                        
                # Fill beam interior
                for y in range(int(self.y) + 3, int(self.target_cow.y)):
                    for x in range(center_x - self.beam_width // 2 + 1, center_x + self.beam_width // 2):
                        try:
                            char = self.beam_chars[(y + x) % len(self.beam_chars)]
                            screen.addstr(y, x, char, curses.color_pair(1))
                        except:
                            pass