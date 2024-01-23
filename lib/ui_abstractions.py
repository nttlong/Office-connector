from abc import ABC, abstractmethod
class BaseLoader(ABC):
    @abstractmethod
    def load_word(self, file_path:str):
        pass

    @abstractmethod
    def load_power_point(self, file_path):
        pass

    @abstractmethod
    def load_excel(self, file_path):
        pass
    @abstractmethod
    def load_note_pad(self, file_path):
        pass
    @abstractmethod
    def load_paint_app(self, file_path):
        pass