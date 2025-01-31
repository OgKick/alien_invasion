import random
from alien import Alien

def create_grid_pattern(fleet, alien_w, alien_h, screen_w, screen_h):
    """
    Creates a grid pattern of aliens in the fleet.

    Args:
    fleet (AlienFleet): The fleet object to which aliens will be added.
    alien_w (int): The width of each alien.
    alien_h (int): The height of each alien.
    screen_w (int): The width of the screen.
    screen_h (int): The height of the screen.
    """
    fleet_w, fleet_h = calculate_fleet_size(alien_w, alien_h, screen_w, screen_h)
    x_offset, y_offset = calculate_offset_position(screen_w, screen_h, fleet_w, fleet_h)

    for row in range(fleet_h):
        for col in range(fleet_w):
            current_x = alien_w * col + x_offset
            current_y = alien_h * row + y_offset
            create_alien(fleet, current_x, current_y)

def create_zigzag_pattern(fleet, alien_w, alien_h, screen_w, screen_h):
    """
    Creates a zigzag pattern of aliens in the fleet.

    The aliens are arranged in rows, and every other row is shifted horizontally
    to create a zigzag pattern.

    Args:
    fleet (AlienFleet): The fleet object to which aliens will be added.
    alien_w (int): The width of each alien.
    alien_h (int): The height of each alien.
    screen_w (int): The width of the screen.
    screen_h (int): The height of the screen.
    """
    fleet_w, fleet_h = calculate_fleet_size(alien_w, alien_h, screen_w, screen_h)
    x_offset, y_offset = calculate_offset_position(screen_w, screen_h, fleet_w, fleet_h)

    for row in range(fleet_h):
        for col in range(fleet_w):
            current_x = alien_w * col + x_offset
            current_y = alien_h * row + y_offset
            if row % 2 == 0:
                current_x += 100  # Shift odd rows for zigzag effect
            create_alien(fleet, current_x, current_y)

def create_triangle_pattern(fleet, alien_w, alien_h, screen_w, screen_h):
    """
    Creates a triangular pattern of aliens in the fleet.

    The number of aliens per row decreases as the rows move upward, forming a triangle shape.

    Args:
    fleet (AlienFleet): The fleet object to which aliens will be added.
    alien_w (int): The width of each alien.
    alien_h (int): The height of each alien.
    screen_w (int): The width of the screen.
    screen_h (int): The height of the screen.
    """
    fleet_w, fleet_h = calculate_fleet_size(alien_w, alien_h, screen_w, screen_h)
    x_offset, y_offset = calculate_offset_position(screen_w, screen_h, fleet_w, fleet_h)

    for row in range(fleet_h):
        for col in range(fleet_w):
            if col > row:  # Make fewer aliens in higher rows to create a triangle
                continue
            current_x = alien_w * col + x_offset
            current_y = alien_h * row + y_offset
            create_alien(fleet, current_x, current_y)

def create_random_pattern(fleet, alien_w, alien_h, screen_w, screen_h):
    """
    Creates a random pattern of aliens in the fleet.

    The aliens are placed at random positions on the screen, up to half the screen height.

    Args:
    fleet (AlienFleet): The fleet object to which aliens will be added.
    alien_w (int): The width of each alien.
    alien_h (int): The height of each alien.
    screen_w (int): The width of the screen.
    screen_h (int): The height of the screen.
    """
    fleet_w, fleet_h = calculate_fleet_size(alien_w, alien_h, screen_w, screen_h)
    for _ in range(fleet_w * fleet_h):
        random_x = random.randint(0, screen_w - alien_w)
        random_y = random.randint(0, screen_h // 2 - alien_h)
        create_alien(fleet, random_x, random_y)

# Utility functions that are common to the patterns
def calculate_fleet_size(alien_w, alien_h, screen_w, screen_h):
    """
    Calculates the number of aliens that can fit on the screen based on alien size.

    Args:
    alien_w (int): The width of each alien.
    alien_h (int): The height of each alien.
    screen_w (int): The width of the screen.
    screen_h (int): The height of the screen.

    Returns:
    tuple: A tuple containing the number of aliens that can fit horizontally and vertically.
    """
    fleet_w = screen_w // alien_w
    fleet_h = screen_h // alien_h
    return fleet_w, fleet_h

def calculate_offset_position(screen_w, screen_h, fleet_w, fleet_h):
    """
    Calculates the offset positions for the fleet to be centered on the screen.

    Args:
    screen_w (int): The width of the screen.
    screen_h (int): The height of the screen.
    fleet_w (int): The number of aliens that can fit horizontally.
    fleet_h (int): The number of aliens that can fit vertically.

    Returns:
    tuple: A tuple containing the x and y offsets to center the fleet on the screen.
    """
    x_offset = int(screen_w // fleet_w // 2)
    y_offset = int(screen_h // fleet_h // 2)
    return x_offset, y_offset

def create_alien(fleet, current_x, current_y):
    """
    Creates a new alien at the specified position and adds it to the fleet.

    Args:
    fleet (AlienFleet): The fleet object to which the alien will be added.
    current_x (int): The x-coordinate for the new alien.
    current_y (int): The y-coordinate for the new alien.
    """
    new_alien = Alien(fleet.game, current_x, current_y)
    fleet.add(new_alien)
