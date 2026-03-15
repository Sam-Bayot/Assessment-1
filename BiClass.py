#File: BiClass.py
#Description: A collection of data structures with an unique one-to-one key/value relationship
#Author: Sam Bayot
#Last Modified: 16/03/26

class BiDict:

    def __init__(self, forward_dict: dict) -> None:
        self.forward_dict: dict = forward_dict
        self.backward_dict: dict = self.create_backward_dict(self.forward_dict)

    def create_backward_dict(self, forward_dict: dict) -> dict:
        return {value: key for key, value in forward_dict.items()}

    def __getitem__(self, key: any) -> any:
        if key in self.forward_dict:
            return self.forward_dict[key]
        elif key in self.backward_dict:
            return self.backward_dict[key]
        else:
            raise KeyError(f"{key} not found")

class BiList(BiDict):

    def __init__(self, forward_list: list) -> None:
        self.forward_list: list = forward_list
        self.backward_dict: dict = self.create_backward_dict({i:value for i, value in enumerate(self.forward_list)})

    def __getitem__(self, key: any) -> any:
        if isinstance(key, int):
            try:
                self.forward_list[key]
            except:
                raise KeyError(f"index {key} is out of bounds")
        elif key in self.backward_dict:
            return self.backward_dict[key]
        else:
            raise KeyError(f"{key} not found")

    def __iter__(self) -> list:
        for item in self.forward_list:
            yield item
