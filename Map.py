#File: Map.py
#Description: Handles the player view and map interactions
#Author: Sam Bayot
#Last Modified: 29/03/26

#-----Libraries-----
import BiClass

#-----Classes-----

#A tuple holding the x and y position of an entity
class Position:
    def __init__(self, position_x: int, position_y: int) -> None:
        self.x: int = position_x
        self.y: int = position_y

    #Creates a new version of the position
    def copy(self) -> "Position":
        return Position(self.x, self.y)

    #Updates the x and y positions of the object
    def update(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    #Gives the string version of the position
    def __str__(self) -> str:
        return str((self.x, self.y))

    #Function for checking if a tuple is equal to the tuple version of the position
    def __eq__(self, value: any) -> bool:
        return value == (self.x, self.y)

#A position in the map that handles interactions when the player enters
class Interaction:

    def __init__(self, name: str, position: tuple[int, int], enter_function: callable = None, state: str = "?", parent_map: "Map" = None) -> None:
        self.position: Position = Position(*position)
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
    def __init__(self, map_state: list[list[str]], interactions: list[Interaction], frame_radii: tuple[int, int], boundary_sprite: str) -> None:
        self.map_state: list[list[str]] = map_state
        self.interactions: BiClass.BiDict[str, Interaction] = BiClass.BiDict({interaction.name: interaction for interaction in interactions})
        self.seen_map: set[tuple[int, int]] = set()
        self.frame_width, self.frame_height = frame_radii
        self.boundary_sprite: str = boundary_sprite

        #Updates the state of each interaction
        for interaction in self.interactions.values():
            interaction.parent_map = self
            self.update_map_interaction(interaction)

    #Sets the map state in terms of a position object
    def set_position_state(self, position: Position, state: str) -> None:
        self.map_state[position.y][position.x] = state

    #Gets the map state of a position
    def get_position_state(self, position: Position) -> str:
        return self.map_state[position.y][position.x]
    
    #Updates the map to the interaction state
    def update_map_interaction(self, interaction: Interaction):
        self.set_position_state(interaction.position, interaction.state)

    #Returns a grid of strings that is the shape of an oval around a position in the map
    def get_map_frame(self, position: Position, position_sprite: str = "") -> list[list[str]]:
        y_ratio: float = self.frame_height / self.frame_width
        #Creates a 2D matrix to hold the frame
        curr_frame: list[list[str]] = [[] for _ in range((self.frame_height * 2) + 1)]
        
        #min_y and y_offset is if the player is too high up in the map to avoid accessing invalid indices
        min_y = max(position.y - self.frame_height, 0)
        y_offset = self.frame_height - (position.y - min_y)

        for i, row in enumerate(self.map_state[min_y : min(position.y + self.frame_height + 1, len(self.map_state))], start=y_offset):
            center_y = abs(i - self.frame_height)
            #min_x and x_offset is if the player is too far left of the map to avoid accessing invalid indices
            min_x = max(position.x - self.frame_width, 0)
            x_offset = self.frame_width - (position.x - min_x)
            
            #Prints the letter if it is within the radius
            for j, letter in enumerate(row[min_x : min(position.x + self.frame_width + 1, len(row))], start=x_offset):
                center_x = abs(j - self.frame_width) * y_ratio
                if i == self.frame_height and j == self.frame_width and position_sprite:
                    curr_frame[i].append(position_sprite)
                #Pythagoras formula to check whether each position is within a certain distance or radius from the centre
                elif abs(center_y*center_y) + abs(center_x*center_x) <= (self.frame_height*self.frame_height):
                    curr_frame[i].append(letter)
                    #Adds the position to the seen_map
                    self.seen_map.add((j + min_x - x_offset, i + min_y - y_offset))
                else:
                    curr_frame[i].append(' ')
        return curr_frame

    #Prints the frame
    def print_current_frame(self, frame: list[list[str]]) -> None:
        for row in frame:
            #Prints each letter without adding a newline
            for letter in row:
                print(letter, end='')
            print()

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
], [], (15, 7), "#" )
