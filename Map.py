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

