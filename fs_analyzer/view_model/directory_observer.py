from abc import ABC, abstractmethod
from fs_analyzer.model import file_permissions, file_category
from typing import Set

from fs_analyzer.model import file_category

#interface
class DirectoryObserver(ABC):
    
    @abstractmethod
    def on_new_categorized_file(self, file_path:str, filecategory: file_category.FileCategory)->None:
        pass
    
    @abstractmethod
    def on_new_file_category_size(self, filecategory: file_category.FileCategory, size:int)->None:
        pass

    @abstractmethod
    def on_new_file_with_unusual_permission(self, filepath:str, permissions: Set[file_permissions.FilePermission])->None:
        pass
    
    @abstractmethod
    def on_new_large_file(self, filepath:str, size:int)->None:
        pass

    #>user-non-guilty errors (map to exceptions)
    def on_file_not_found(self)->None:
        pass

    def on_directory_not_found(self)->None:
        pass

    def on_permission_error(self)->None:
        pass
    
    def on_unknown_error(self)->None:
        pass
    
    #user-guilty errors
    def on_invalid_input(self)->None:
        pass

 
