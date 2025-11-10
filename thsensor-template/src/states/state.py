"""
(Abstract) state for all states - parent state.
"""
class AbstractState:
    name: str = None
    
    def __init__(self, device):
        self.device = device
        
    def enter(self):
        """
        Executed on state entry.
        """
        print(f'>> Entering state {self.name}')
    
    def exec(self):
        """
        Main state function. The state logic goes here.
        """
        raise NotImplementedError('This method was not yet implemented.')
    
    def exit(self):
        """
        Executed on state exit.
        """
        print(f'>> Leaving state {self.name}')

