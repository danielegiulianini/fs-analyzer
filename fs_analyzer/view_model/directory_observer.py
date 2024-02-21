from abc import ABC, abstractmethod
from typing import Set

from fs_analyzer.model import file_permissions, file_category

class DirectoryObserver(ABC):
    """An abstract observer for directory analyzer's analysis intermediate outcomes 
    during traversal, like new file discovery.
    Leveraging the behavioural "Observer" OO design pattern allows to 
    avoid the use of large collections to gather results so optimizing it for handling 
    the traversal of large directories.
    """
    
    @abstractmethod
    def on_new_categorized_file(self, 
                                file_path:str, 
                                filecategory: file_category.FileCategory)->None:
        """Defines how to handle the discovery, during the directory tree traversal, of a new file with 
        its corresponding category.

        Args:
            file_path (str): the path in which the categorized file resides.
            filecategory (file_category.FileCategory): the category of the file.
        """
        pass
    
    @abstractmethod
    def on_new_file_category_size(self, 
                                  files_category: file_category.FileCategory, 
                                  category_size:int)->None:
        """Defines how to handle the notification of the size of a category of files, resulting by
        the completion of directory tree traversal.
        
        Args:
            files_category (file_category.FileCategory): the file category.
            category_size (int): _description_ the size given by the sum of the files 
                of the given category.
        """
        pass

    @abstractmethod
    def on_new_file_with_unusual_permission(self, 
                                            file_path:str, 
                                            file_permissions: Set[file_permissions.FilePermission])->None:
        """Defines how to handle the notification, during the directory tree traversal, of the unusual 
        permission settings associated to a file.

        Args:
            file_path (str):  the path in which the categorized file resides.
            file_permissions (Set[file_permissions.FilePermission]): the unusual file permissions
                associated to the file.
        """
        pass
    
    @abstractmethod
    def on_new_large_file(self, 
                          file_path:str, 
                          file_size:int)->None:
        """Defines how to handle the notification, during the directory tree traversal, 
        of a large file.

        Args:
            file_path (str): the path in which the categorized file resides.
            file_size (int): the size of the file.
        """
        pass

    def on_file_not_found(self)->None:
        """Defines how to handle the notification, during the directory tree traversal, 
        of a file not found.
        """
        pass

    def on_directory_not_found(self)->None:
        """Defines how to handle the notification, during the directory tree traversal, 
        of a directory not found.
        """
        pass

    def on_permission_error(self)->None:
        """Defines how to handle the notification, during the directory tree traversal, 
        of a permission error.
        """
        pass
    
    def on_unknown_error(self)->None:
        """Defines how to handle the notification, during the directory tree traversal, 
        of an unknown error.
        """
        pass
    
    def on_invalid_input(self)->None:
        """Defines how to handle the notification of an invalid input.
        """
        pass

 
