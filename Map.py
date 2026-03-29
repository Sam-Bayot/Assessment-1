#File: Map.py
#Description: Handles the player view and map interactions
#Author: Sam Bayot
#Last Modified: 29/03/26

#-----Libraries-----
import BiClass

#-----Classes-----

#A position in the map that handles interactions when the player enters
class Interaction:

    def __init__(self, name: str, position: list[int, int], enter_function: callable = None, state: str = "?", parent_map: "Map" = None) -> None:
        self.position: list[int, int] = position
        self.state: str = state
        self.name: str = name
        #Creates a callable that runs the enter function and updates the map afterwards
        self.on_player_enter: callable = self.wrapped_on_player_enter(enter_function)
        self.parent_map: Map = parent_map
       

    #Returns a function that will run when the player enters the interaction
    def wrapped_on_player_enter(self, enter_function: callable, args: tuple = ()) -> callable:
        def _wrapper(player: "Player") -> None:
            if enter_function:
                if args: 
                    enter_function(self, player, *args)
                else:
                    enter_function(self, player)
            else:
                self.enter_default()
            self.parent_map.update_map_interaction(self)
        return _wrapper

    #The default enter function
    def enter_default(self) -> None:
        print(f"Entering {self.name}")
                
#Class for a 2D map
class Map:
    def __init__(self, map_state: list[list[str]], interactions: list[Interaction]) -> None:
        self.map_state: list[list[str]] = map_state
        self.interactions: BiClass.BiDict[str, Interaction] = BiClass.BiDict({interaction.name: interaction for interaction in interactions})
        self.seen_map: set[tuple[int, int]] = set()

        #Updates the state of each interaction
        for interaction in self.interactions.values():
            interaction.parent_map = self
            self.update_map_interaction(interaction)

    #Updates the map to the interaction state
    def update_map_interaction(self, interaction: Interaction):
        self.map_state[interaction.position[1]][interaction.position[0]] = interaction.state

#Returns a grid of strings that is the shape of an oval around a position in the map
def get_map_frame(position: tuple[int, int], curr_map: Map, width_radius: int, height_radius: int, position_sprite: str = "") -> list[list[str]]:
    y_ratio: float = height_radius / width_radius
    #Creates a 2D matrix to hold the frame
    curr_frame: list[list[str]] = [[] for _ in range((height_radius * 2) + 1)]
    
    #min_y and y_offset is if the player is too high up in the map to avoid accessing invalid indices
    min_y = max(position[1] - height_radius, 0)
    y_offset = height_radius - (position[1] - min_y)

    for i, row in enumerate(curr_map.map_state[min_y : min(position[1] + height_radius + 1, len(curr_map.map_state))], start=y_offset):
        center_y = abs(i - height_radius)
        #min_x and x_offset is if the player is too far left of the map to avoid accessing invalid indices
        min_x = max(position[0] - width_radius, 0)
        x_offset = width_radius - (position[0] - min_x)
        
        #Prints the letter if it is within the radius
        for j, letter in enumerate(row[min_x : min(position[0] + width_radius + 1, len(row))], start=x_offset):
            center_x = abs(j - width_radius) * y_ratio
            if i == height_radius and j == width_radius and position_sprite:
                curr_frame[i].append(position_sprite)
            #Pythagoras formula to check whether each position is within a certain distance or radius from the centre
            if abs(center_y*center_y) + abs(center_x*center_x) <= (height_radius*height_radius):
                curr_frame[i].append(letter)
                #Adds the position to the seen_map
                curr_map.seen_map.add((j + min_x - x_offset, i + min_y - y_offset))
            else:
                curr_frame[i].append(' ')
    return curr_frame

#Prints the frame
def print_current_frame(frame: list[list[str]]) -> None:
    for row in frame:
        #Prints each letter without adding a newline
        for letter in row:
            print(letter, end='')
        print()

#Prints the part of the map the player has already seen
def print_seen_map(player_map: Map, player_position: tuple[int, int], position_sprite: str = "") -> None:
    #Sorts the seen map which is a set of a tuple of 2 integers
    sorted_seen_map: list[tuple[int, int]] = sorted(player_map.seen_map, key=lambda position: position[1])

    #Goes through each row of the map and prints the character if the position is in the seen map
    for i, row in enumerate(player_map.map_state[sorted_seen_map[0][1]:sorted_seen_map[-1][1] + 1]):
        line = ""
        for j, letter in enumerate(row):
            #Adds the player sprite to 'line' if it is the player position
            if (j, i + sorted_seen_map[0][1]) == tuple(player_position) and position_sprite:
                line += position_sprite
                continue
            #Adds the letter sprite to 'line' if it is in seen map
            if (j, i + sorted_seen_map[0][1]) in player_map.seen_map:
                line += letter
            else:
                line += ' '
        #Prints the whole formatted line
        print(line)

NORTH_ISLAND_MAP: Map = Map([
list("###"),  
list("##-#"),
list("#--#####"),  
list(" #--#######"),  
list("  #-----######"),  
list("  ##-------####"),  
list("   ##---------#"),  
list("    ###-------##"),  
list("     ###------##"),  
list("       ##-----##"),  
list("        ##----###"),  
list("         ##-----##"),  
list("          #-----##"),  
list("            #---#### ####"),  
list("            ##----### #--#"),
list("             ##-----# ##-##"),  
list("              ##----####--#"),  
list("               ##----##---##"),  
list("               ##---------###               ###"),  
list("                #----------#####         ########"),  
list("               ##------------#######    ####---##"),
list("               ##---------------#########------##"),  
list("               ##--------------------##-------##"), 
list("              ##------------------------------##"),  
list("              ##------------------------------##"),
list("              ##---------------------------####"),  
list("          #####--------------------------###"), 
list("        ####------------------------########"), 
list("       ##-------------------------#########"),  
list("       ###-----------------------###"),  
list("        #####--------------------##"),  
list("           ######-----------------##"),  
list("              #####---------------##"),  
list("                 ###-------------##"),  
list("                   #-----------###"),  
list("                   #---------###"), 
list("                  ##---------##"),  
list("                 ##---------##"),  
list("                ##---------##"),  
list("              ###--------###"),
list("                 ##----###"),  
list("                  #######"),  
list("                    ####")  
], [])
print_current_frame(get_map_frame((25, 25), NORTH_ISLAND_MAP, 15, 10, "o"))
