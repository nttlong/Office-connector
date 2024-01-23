from abc import ABC, abstractmethod
class BaseThreading(ABC):
    @abstractmethod
    def start(self, name, target, args):
        pass

    @abstractmethod
    def join(self, list_of_thread):
        pass
