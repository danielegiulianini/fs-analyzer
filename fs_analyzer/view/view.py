from abc import abstractmethod
from fs_analyzer.view_model.directory_observer import DirectoryObserver

class View(DirectoryObserver):
    """
    Abstract modelling of a view for reporting on the file system usage and structure, that could 
    actually be a command-line or a graphic user interface.

    Args:
        DirectoryObserver: The abstraction representing an Observer of the directory tree
        traversal events.
    """
    @abstractmethod
    def show(self):
        """Shows the view.
        """
        pass