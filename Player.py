#File: Player.py
#Description: This script is for the player inventory, variables and states
#Author: Sam Bayot
#Last Modified: 31/03/26

#-----Libraries-----

import Map
import Input
import math

#-----Classes-----

#Base class for entities
class Entity:
    DIRECTIONS: list[str] = ["up", "down", "left", "right", "stationary"]
    
    def __init__(self, name: str, entity_map: Map.Map, starting_position: tuple[int, int], sprite: str, speed: float = 1) -> None:
        self.name: str = name
        self.map: Map.Map = entity_map
        self.position: Map.Position = Map.Position(*starting_position)
        self.perfect_position: tuple[float, float] = (float(starting_position[0]), float(starting_position[1]))
        self.sprite: str = sprite
        self.speed: float = speed
        self.inventory: dict[str, int] = {}

    #Moves the entity around the 2D matrix
    def walk(self, input_event: Input.InputEvent) -> None:
        curr_perfect_position: list[float, float] = list(self.perfect_position)

        #Changes the position based on the input event
        match input_event.event:
            case "up":
                curr_perfect_position[1] -= self.speed
            case "down":
                curr_perfect_position[1] += self.speed
            case "left":
                curr_perfect_position[0] -= self.speed
            case "right":
                curr_perfect_position[0] += self.speed
            case _:
                #Case if the input event isn't one of the 4 directions
                return
            
        #Only moves the player if it doesn't hit a boundary
        curr_position: Map.Position = Map.Position(math.floor(curr_perfect_position[0]), math.floor(curr_perfect_position[1]))
        if self.map.get_position_state(curr_position) != self.map.boundary_sprite:
            self.position.update(curr_position.x, curr_position.y)
            self.perfect_position = tuple(curr_perfect_position)

#Player class inherits entity class and has special functions for camera view 
class Player(Entity):
    def __init__(self, name: str, starting_position: tuple[int, int], sprite: str, player_map: Map.Map, speed: float = 1) -> None:
        super().__init__(name, player_map, starting_position, sprite, speed)

    #Prints the part of the map the player has already seen
    def print_seen_map(self) -> None:
        #Sorts the seen map which is a set of a tuple of 2 integers
        sorted_seen_map: list[tuple[int, int]] = sorted(self.map.seen_map, key=lambda position: position[1])
        #Goes through each row of the map and prints the character if the position is in the seen map
        for i, row in enumerate(self.map.map_state[sorted_seen_map[0][1]:sorted_seen_map[-1][1] + 1]):
            line = ""
            for j, letter in enumerate(row):
                #Adds the player sprite to 'line' if it is the player position
                if (j, i + sorted_seen_map[0][1]) == self.position and self.sprite:
                    line += self.sprite
                    continue
                #Adds the letter sprite to 'line' if it is in seen map
                if (j, i + sorted_seen_map[0][1]) in self.map.seen_map:
                    line += letter
                else:
                    line += ' '
            #Prints the whole formatted line
            print(line)

#-----Main-----
if __name__ == "__main__":
    #Test for real time player movement
    import time
    import os
    curr_player: Player = Player("", (25, 25), "o", Map.NORTH_ISLAND_MAP, 1)
    curr_player.map.get_map_frame(curr_player.position, curr_player.sprite)
    curr_player.position.update(15, 15)
    curr_player.map.get_map_frame(curr_player.position, curr_player.sprite)
    curr_player.print_seen_map()
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        input_event: Input.InputEvent = Input.get_real_time_input_event()
        if input_event:
            if input_event.event in Entity.DIRECTIONS:
                curr_player.walk(input_event)
            if input_event.event == "quit":
                raise ValueError("key q was pressed")   
        curr_player.map.print_current_frame(curr_player.map.get_map_frame(curr_player.position, curr_player.sprite))
        time.sleep(0.1)
