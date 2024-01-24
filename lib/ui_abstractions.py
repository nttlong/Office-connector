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

    @abstractmethod
    def show_message_error(self, param):
        pass

    @abstractmethod
    def show_message(self, param):
        pass
    @abstractmethod
    def set_auto_start_up(self):
        pass

    @abstractmethod
    def get_icon(self):
        pass

    @abstractmethod
    def get_icon_data(self):
        pass
    @abstractmethod
    def create_tray_icon(self, app_icon):
        pass

    @abstractmethod
    def get_start_app(self):
        pass

    @abstractmethod
    def get_qt_app_icon(self):
        pass

    @abstractmethod
    def get_q_pixmap_app_icon(self):
        pass
    @abstractmethod
    def get_main_app(self):
        pass

    @abstractmethod
    def get_main_widget(self):
        pass
    @abstractmethod
    def get_app_icon_path(self):
        pass