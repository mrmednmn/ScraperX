#Developer: Mohamed Naamane
#Contact: naamanemohamedtheprogrammer@gmail.com
from abc import ABC, abstractmethod

class SavingStrategy(ABC):
    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def save(self,data):
        pass

    @abstractmethod
    def notify(self,data):
        pass