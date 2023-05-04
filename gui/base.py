from abc import ABC, abstractmethod

class Gui(ABC):
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def log(self, data):
        pass
