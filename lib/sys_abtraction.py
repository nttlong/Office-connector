from abc import ABC, abstractmethod
class BaseSys(ABC):
    @abstractmethod
    def get_list_of_files(self, app_data_dir):
        pass

    @abstractmethod
    def is_file_in_use(self, file_path):
        pass

    @abstractmethod
    def delete_file(self, file_path):
        pass