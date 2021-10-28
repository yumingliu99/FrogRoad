import pygame, random
from bus import Bus

class Street:
    # Define constant values
    SIZE = (600, 40)
    SCREEN_DIM = 600, 500

    # Creates a Street object
    def __init__(self, street_height: int, direction: str, number_of_buses: int):
        # Street Information
        self.rect = pygame.Rect((0, street_height), Street.SIZE)
        self.buses = []
        # Add Buses
        self.add_buses(direction, number_of_buses, street_height + 20)

    # Have students copy and paste this into his/her own code
    # This function randomizes an X position until there is no other Bus 30 pixels infront and 30 pixels behind them
    # Ensures Buses do not stack on top of one another
    def add_buses(self, direction: str, number_of_buses: int, street_height: int):
        dp = []
        for _ in range(number_of_buses):
            while True:
                x_pos = random.randint(30, 570)
                valid = True
                for i in range(x_pos - 60, x_pos + 60):
                    if i in dp:
                        valid = False
                if valid:
                    dp.append(x_pos)
                    break
            self.buses.append(Bus((x_pos, street_height), direction))