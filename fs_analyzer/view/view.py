from abc import abstractmethod
from fs_analyzer.view_model.directory_observer import DirectoryObserver

class View(DirectoryObserver):
    @abstractmethod
    def show(self):
        pass