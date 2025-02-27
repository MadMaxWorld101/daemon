import curses
import time
import random
from animated_bat import AnimatedBat
from animated_cow import AnimatedCow
from flashing_stars import FlashingStars
from meteor import ShootingStar
from ufo import UFO

def main(stdscr):
    # Set up curses
    curses.start_color()
    curses.use_default_colors()  # Use terminal's default colors
    curses.init_pair(1, curses.COLOR_WHITE, -1)  # For the moon and flashing stars
    curses.init_pair(2, curses.COLOR_MAGENTA, -1)  # For the bat
    curses.init_pair(3, curses.COLOR_CYAN, -1)  # For stars
    curses.init_pair(4, curses.COLOR_GREEN, -1)  # For UI and mooing
    curses.init_pair(5, curses.COLOR_GREEN, -1)  # For ground
    curses.init_pair(6, curses.COLOR_YELLOW, -1)  # For second bat
    curses.init_pair(7, curses.COLOR_RED, -1)    # For special effects
    
    # Advanced anti-flicker measures
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(1)   # Non-blocking input
    stdscr.timeout(100) # Much longer timeout to reduce CPU usage and flickering
    
    # Try to enable hardware cursor if available
    if hasattr(curses, 'set_escdelay'):
        curses.set_escdelay(25)  # Reduce escape delay
    
    # Create a pad for double buffering
    try:
        height, width = stdscr.getmaxyx()
        pad = curses.newpad(height, width)
    except:
        # Fallback if pad creation fails
        pad = stdscr
    
    # Get initial dimensions
    height, width = stdscr.getmaxyx()
    ground_level = height - 6
    
    # Initialize flashing stars
    stars = FlashingStars(height, width, ground_level)
    
    # Initialize shooting star and UFO
    shooting_star = ShootingStar()
    ufo = UFO()
    
    # Create bats with random initial positions
    bat1 = AnimatedBat()
    bat1.x = random.randint(10, width - 20)
    bat1.y = random.randint(5, height - 15)
    
    bat2 = AnimatedBat()
    bat2.x = random.randint(10, width - 20)
    bat2.y = random.randint(5, height - 15)
    bat2.color = 6  # Different color for second bat
    
    # Define ground level and create cows
    cow1 = AnimatedCow(ground_level, "normal")
    
    cow2 = AnimatedCow(ground_level, "spotted")
    cow2.x = width - 30  # Start second cow on right side
    cow2.direction = -1  # Start moving left
    
    # Track weather and day/night cycle
    weather_state = "clear"  # "clear", "cloudy", "rainy"
    weather_counter = 0
    weather_duration = random.randint(200, 400)
    
    # First frame delay to avoid initial flicker
    time.sleep(0.2)
    
    # Track last update time to limit framerate
    last_update = time.time()
    target_fps = 12  # Increased from 8 to 12 FPS to reduce lag
    
    # Game state
    time_counter = 0
    
    while True:
        # Get current time
        current_time = time.time()
        
        # Skip frame if not enough time has passed (frame limiting)
        if current_time - last_update < 1.0/target_fps:
            time.sleep(0.01)  # Short sleep to reduce CPU usage
            continue
            
        # Update last frame time
        last_update = current_time
        time_counter += 1
        
        # Update weather
        weather_counter += 1
        if weather_counter >= weather_duration:
            # Change weather
            weather_counter = 0
            weather_duration = random.randint(200, 400)
            weather_options = ["clear", "cloudy", "rainy"]
            # Don't pick the same weather again
            weather_options.remove(weather_state)
            weather_state = random.choice(weather_options)
        
        # Get updated dimensions
        try:
            height, width = stdscr.getmaxyx()
            ground_level = height - 6
        except:
            # Default dimensions if can't get
            height, width = 24, 80
            ground_level = height - 6
        
        # Update stars
        stars.update()
        
        # Update shooting star
        if not shooting_star.active and random.random() < 0.005:  # 0.5% chance per frame
            shooting_star.start(width, ground_level)
        
        if shooting_star.active:
            shooting_star.update()
            
        # Update UFO (rarer event)
        if not ufo.active and random.random() < 0.0008:  # 0.08% chance per frame
            ufo.start(width, [cow1, cow2])
            
        if ufo.active:
            ufo.update(width)
        
        # Clear the screen
        pad.erase()
        
        # Draw border
        pad.box()
        
        # Draw title and weather info
        title = "BATii"
        weather_info = f"Weather: {weather_state.capitalize()}"
        pad.addstr(0, (width - len(title)) // 2, title, curses.color_pair(4))
        try:
            pad.addstr(0, width - len(weather_info) - 2, weather_info, curses.color_pair(3))
        except:
            pass
        
        # Draw stars
        stars.draw(pad, height, width)
        
        # Draw shooting star if active
        if shooting_star.active:
            shooting_star.draw(pad, height, width)
            
        # Draw UFO if active
        if ufo.active:
            ufo.draw(pad, height, width)
        
        # Draw a thicker crescent moon (smaller in size but fatter)
        moon = [
            "   █████  ",
            "  ██   ██ ",
            " ██     █ ",
            " █       █",
            " █        ",
            " █        ",
            " █       █",
            " ██     █ ",
            "  ██   ██ ",
            "   █████  "
        ]
        
        for i, line in enumerate(moon):
            if 3 + i < height - 1:  # Make sure we don't draw outside the screen
                try:
                    pad.addstr(3 + i, width - 14, line, curses.color_pair(1))
                except:
                    pass  # Silently ignore drawing errors
        
        # Draw weather effects
        if weather_state == "cloudy":
            clouds = [
                "  .--.    ",
                " /    \\   ",
                "(      )  ",
                " `----´   "
            ]
            
            # Draw a few clouds
            cloud_positions = [(5, 10), (8, width // 2), (3, width - 30)]
            for pos_y, pos_x in cloud_positions:
                if pos_y < height and pos_x < width:
                    for i, line in enumerate(clouds):
                        try:
                            pad.addstr(pos_y + i, pos_x, line, curses.color_pair(1))
                        except:
                            pass
                            
        elif weather_state == "rainy":
            # Draw some raindrops randomly
            for _ in range(min(width // 4, 20)):  # Adjust number of raindrops
                drop_x = random.randint(1, width - 2)
                drop_y = random.randint(1, ground_level - 2)
                try:
                    if random.random() < 0.5:
                        pad.addstr(drop_y, drop_x, "/", curses.color_pair(3))
                    else:
                        pad.addstr(drop_y, drop_x, "|", curses.color_pair(3))
                except:
                    pass
        
        # Update positions and animations
        bat1.update_position(width, ground_level - 3)  # Keep bat above ground
        bat1.update_animation()
        
        bat2.update_position(width, ground_level - 3)  # Keep bat above ground
        bat2.update_animation()
        
        cow1.update_position(width, ground_level)
        cow1.update_animation()
        
        cow2.update_position(width, ground_level)
        cow2.update_animation()

        # Draw the bats and cows on pad
        bat1.draw(pad)
        bat2.draw(pad)
        cow1.draw(pad)
        cow2.draw(pad)
        
        # Draw ground
        ground_pattern = "^~^~^~" * ((width-2) // 6 + 1)
        # First layer (grass)
        try:
            pad.addstr(ground_level, 1, ground_pattern[:width-2], curses.color_pair(5))
            # Second layer (dirt)
            pad.addstr(ground_level + 1, 1, "=" * (width-2), curses.color_pair(5))
            # Fill the rest with solid ground
            for y in range(ground_level + 2, height - 1):
                pad.addstr(y, 1, "#" * (width-2), curses.color_pair(5))
        except:
            pass  # Silently ignore drawing errors
        
        # Display controls at the bottom
        controls = "Controls: q-Quit | r-Reset Bats | g-Graze | w-Weather | u-UFO"
        cow_status = f"Cows: {cow1.cow_type.capitalize()} & {cow2.cow_type.capitalize()}"
        
        # Safe display that checks terminal boundaries
        try:
            pad.addstr(height - 2, 2, cow_status[:width-4], curses.color_pair(4))
            # Make sure we don't write on the very last cell of the terminal
            if height > 1 and width > 4:
                pad.addstr(height - 1, 2, controls[:width-4], curses.color_pair(4))
        except:
            # Ignore errors from writing to screen
            pass
        
        # Handle input
        try:
            key = stdscr.getch()
        except:
            key = -1

        if key == ord('r'):
            # Reset bat positions to random locations
            bat1.x = random.randint(10, width - 20)
            bat1.y = random.randint(5, ground_level - 10)
            bat1.dx = random.choice([-1, 1]) * random.uniform(0.5, 1.5)
            bat1.dy = random.choice([-1, 1]) * random.uniform(0.3, 0.8)
            
            bat2.x = random.randint(10, width - 20)
            bat2.y = random.randint(5, ground_level - 10)
            bat2.dx = random.choice([-1, 1]) * random.uniform(0.5, 1.5)
            bat2.dy = random.choice([-1, 1]) * random.uniform(0.3, 0.8)
        elif key == ord('g'):
            # Force cows to graze
            cow1.is_grazing = True
            cow1.grazing_timer = 0
            cow1.grazing_duration = random.randint(20, 100)
            
            cow2.is_grazing = True
            cow2.grazing_timer = 0
            cow2.grazing_duration = random.randint(20, 100)
        elif key == ord('w'):
            # Manually change weather
            weather_options = ["clear", "cloudy", "rainy"]
            # Don't pick the same weather again
            weather_options.remove(weather_state)
            weather_state = weather_options[0]
            weather_counter = 0
        elif key == ord('u'):
            # Manually trigger UFO event
            if not ufo.active:
                ufo.start(width, [cow1, cow2])
        elif key == ord('q'):
            break  # Exit on 'q'
            
        # Copy from pad to screen with minimal updates - major anti-flicker technique
        try:
            pad.overwrite(stdscr)  # More efficient than refresh - only updates changed areas
            stdscr.noutrefresh()   # Mark for update but don't refresh yet
            curses.doupdate()      # Do all updates at once
        except:
            # Fallback if pad approach fails
            try:
                stdscr.refresh()
            except:
                pass
                
        # Longer sleep between frames - reduced to speed up gameplay
        time.sleep(0.08)

if __name__ == "__main__":
    curses.wrapper(main)