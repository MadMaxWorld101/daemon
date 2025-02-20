def draw_ui(stdscr, bat, message):
    height, width = stdscr.getmaxyx()
    
    # Draw each line of the bat's current frame
    frame = bat.get_current_frame()
    for i, line in enumerate(frame):
        stdscr.addstr(int(bat.y) + i, int(bat.x), line)
    
    # Display the message at the bottom
    stdscr.addstr(height - 2, 0, f">>> {message}")