def load_image(file_path):
    """Load an image from the specified file path."""
    try:
        image = pygame.image.load(file_path)
        return image
    except pygame.error as e:
        print(f"Error loading image: {e}")
        return None

def draw_text(surface, text, position, font, color=(255, 255, 255)):
    """Draw text on the given surface at the specified position."""
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, position)

def get_color(name):
    """Return a color based on the name provided."""
    colors = {
        "black": (0, 0, 0),
        "white": (255, 255, 255),
        "red": (255, 0, 0),
        "green": (0, 255, 0),
        "blue": (0, 0, 255),
        "yellow": (255, 255, 0),
        "cyan": (0, 255, 255),
        "magenta": (255, 0, 255),
    }
    return colors.get(name.lower(), (255, 255, 255))  # Default to white if color not found

def initialize_game_settings():
    """Initialize game settings and return them as a dictionary."""
    settings = {
        "screen_width": 800,
        "screen_height": 600,
        "fps": 60,
        "background_color": (0, 0, 0),
    }
    return settings