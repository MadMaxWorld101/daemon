def draw_ui(stdscr, bat, message):
    """
    Draw the UI elements.
    This function is no longer needed as the bat can draw itself,
    but is kept for backward compatibility if needed.
    """
    height, width = stdscr.getmaxyx()
    
    # Draw bat (now handled directly by the bat class)
    bat.draw(stdscr)
    
    # Display message
    stdscr.addstr(height - 2, 0, f">>> {message}")