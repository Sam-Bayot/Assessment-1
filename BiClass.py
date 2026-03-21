#File: BiClass.py
#Description: A collection of data structures with an unique one-to-one key/value relationship
#Author: Sam Bayot
#Last Modified: 18/03/26

#Bidirectional dictionary with unique one-one relationship
class BiDict:
    
    #Initialise function that creates the forward and backward dicts
    def __init__(self, forward_dict: dict) -> None:
        self.forward_dict: dict = forward_dict
        self.backward_dict: dict = self.create_backward_dict(self.forward_dict)

    #Creates the backward dict from the forward dict
    def create_backward_dict(self, forward_dict: dict) -> dict:
        return {value: key for key, value in forward_dict.items()}

    #Checks both forward and backward dict for the key then returns the result
    def __getitem__(self, key: any) -> any:
        if key in self.forward_dict:
            return self.forward_dict[key]
        elif key in self.backward_dict:
            return self.backward_dict[key]
        else:
            raise KeyError(f"{key} not found")

    #Creates an item in the dicts, but only if the key doesn't exist yet
    def __setitem__(self, key: any, value: any) -> None:
        if key in self or value in self:
            raise ValueError(f"{key} or {value} is already in {self.forward_dict}")
        self.forward_dict[key] = value
        self.backward_dict[value] = key

    #Function for checking if an item is in the forward or backward dict
    def __contains__(self, item: any) -> bool:
        return item in self.forward_dict or item in self.backward_dict

    #String representation of the dict
    def __str__(self):
        return str(self.forward_dict)

    #Allows the dictionary to have static type hinting
    def __class_getitem__(cls, item):
        return cls
    
#Sub-Class of BiDict for lists      
class BiList(BiDict):
    
    #Creates a forward list and forward and backward dicts
    def __init__(self, *items: any) -> None:
        self.forward_list: list = list(items)
        super().__init__({i:value for i, value in enumerate(self.forward_list)})

    #Gets the item if it exists in the forward list or backward dict
    def __getitem__(self, key: any) -> any:
        if isinstance(key, int) or isinstance(key, slice):
            return self.forward_list[key]
        elif key in self.backward_dict:
            return self.backward_dict[key]
        else:
            raise KeyError(f"{key} not found")

    #Sets an item in the forward list and forward and backward dicts
    def __setitem__(self, key: int, values: any) -> None:

        #Changes the value for a specific key
        def change_value(key: int, value: any) -> None:
            if value in self.backward_dict:
                raise ValueError(f"{value} is already in use!")
            if key == len(self):
                self.append(value)
                return
            old_value = self.forward_list[key]
            #Deletes the old value so that it can be rewritten
            if old_value in self.backward_dict:
                del self.backward_dict[old_value]
            self.forward_list[key] = value
            self.forward_dict[key] = value
            self.backward_dict[value] = key
        
        #Raises error if it isn't an integer or a slice
        if not isinstance(key, int) and not isinstance(key, slice):
            raise TypeError(f"Key should be an int or slice not {type(key)}")
        
        #If it's a slice it changes the value for each index with the values
        if isinstance(key, slice):
            indices = range(key.start or 0, key.stop or len(values) + len(self.forward_dict), key.step or 1)
            for index, value in zip(indices, values):
                change_value(index, value)
        elif isinstance(key, int):
            change_value(key, values)
    
    #Appends a single value to the end of the list
    def append(self, item: any) -> None:
        self.forward_list.append(item)
        self.forward_dict[len(self.forward_list) - 1] = item
        self.backward_dict[item] = len(self.forward_list) - 1

    #Adds a list of values to the end of the list
    def extend(self, items: list[any]) -> None:
        for item in items:
            self.append(item)
    
    #Removes the last item or index of the list and dicts
    def pop(self, index: int = -1) -> any:
        #Makes sure the index is positive for iteration later
        if index < 0: index += len(self.forward_list)
        self.backward_dict.pop(self.forward_list[index])
        popped_value: any = self.forward_list.pop(index)
        self.forward_dict.pop(index)
        #Fixes the indices of the values after popping
        for i in range(index, len(self.forward_list)):
            curr_value = self.forward_list[i]
            self.forward_dict[i] = curr_value
            self.backward_dict[curr_value] = i
        #Removes the last value of forward_dict if the forward dict still has a value with the old index
        if len(self.forward_dict) != len(self.forward_list):
            self.forward_dict.pop(len(self.forward_list))
        return popped_value
    
    #Function that allows the object to be iterated upon
    def __iter__(self) -> any:
        for item in self.forward_list:
            yield item
    
    #String representation of the list
    def __str__(self) -> str:
        return str(self.forward_list)

    #Returns the length of forward_list
    def __len__(self) -> int:
        return len(self.forward_list)
