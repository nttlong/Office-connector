from abc import ABC, abstractmethod
class BaseMenu(ABC):
    @abstractmethod
    def build_menu(self, menu):
        pass