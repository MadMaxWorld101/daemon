import curses
import time
from animated_bat import AnimatedBat  # Import the class
from ui import draw_ui  # Import the UI drawing function

def main(stdscr):
    # Set up curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(1)   # Non-blocking input

    bat = AnimatedBat()
    message = "Welcome to your Bat Pet Game!"
    
    while True:
        height, width = stdscr.getmaxyx()

        # Create the moon as a background element
        moon_position = (5, width - 10)  # Example position for the moon
        
        # Clear the screen for the next frame
        stdscr.clear()

        # Draw the moon
        stdscr.addstr(moon_position[0], moon_position[1], "O", curses.color_pair(1))

        # Update bat position and animation
        bat.update_position(width, height)
        bat.update_animation()

        # Draw the bat
        draw_ui(stdscr, bat, message)

        # Handle input
        try:
            key = stdscr.getch()
        except curses.error:
            key = -1

        if key == ord('f'):
            bat.start_feeding()  # Example feed action
        elif key == ord('q'):
            break  # Exit the game
        elif key == ord('e'):
            # Handle other actions like battle, quest, etc.
            pass

        stdscr.refresh()
        time.sleep(0.05)  # Adjust the sleep to control animation speed

if __name__ == "__main__":
    curses.wrapper(main)