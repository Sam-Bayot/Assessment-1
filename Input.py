#File: Input.py
#Description: Script that handles live player input, such as arrow key presses
#Author: Sam Bayot
#Last Modified: 24/03/26

import msvcrt
import BiClass
import time

#-----Constants-----
EVENTS: dict[str, str] = {'w': "up", 'a': "left", 's': "down", 'd': "right", "up_arrow": "up", "left_arrow": "left", "down_arrow": "down", "right_arrow": "right", "q": "quit"}

#-----Classes------

#Class for player input with the event and key
class InputEvent:
    def __init__(self, key: str, event: str) -> None:
        self.key: str = key
        self.event: str = event

#-----Functions-----

#Gets the player input in real time
def get_input(wait_sec: float = 1) -> str | None:
    start_timer: float = time.perf_counter()
    #Waits until a key is pressed
    while True:
        if msvcrt.kbhit():
            char: bytes = msvcrt.getch()
            #Gets special characters
            if char in (b'\x00', b'\xe0'):
                key = ""
                match msvcrt.getch():
                    case b'K':
                        key = "left_arrow"
                    case b'P':
                        key = "down_arrow"
                    case b'M':
                        key = "right_arrow"
                    case b'H':
                        key = "up_arrow"
                if not key: continue
                return key
            else:
                return char.decode()
        elif time.perf_counter() - start_timer:
            return None

#Gets the event from the key
def get_event(key: str) -> str:
    if key in EVENTS:
        return EVENTS[key]
    return None
        
if __name__ == "__main__":
    while True:
        key: str = get_input()      
        event: str = get_event(key)
        input_event: InputEvent = None
        if event:
            input_event = InputEvent(key, event)
            print(input_event.event)
            if input_event.event == "quit":
                raise ValueError("key q was pressed")
            
