import _thread
from typing import Callable

class Connection:
    def __init__(self, func: Callable, connection_list: list):
        self.function = func
        self.connection_list = connection_list
    
    def execute(self, *args):
        _thread.start_new_thread(self.function, args)
        #threads.Thread(target=self.function).run(*args)
    
    def disconnect(self):
        self.connection_list.remove(self)
        del self



class BindableEvent:
    """Custom class for event management"""
    def __init__(self):
        self.connections = []
    
    def connect(self, func: Callable) -> Connection:
        """Creates a connection object which can be disconnected to prevent
        further calls to the function when the connection is no longer desired."""
        c = Connection(func, self.connections)
        self.connections.append(c)
        return c

    def fire(self, *args):
        for connection in self.connections:
            connection.execute(*args)
    
    @staticmethod
    def new():
        return BindableEvent()

new = BindableEvent.new
