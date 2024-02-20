from abc import ABC, abstractmethod

from fs_analyzer.view_model.directory_observer import DirectoryObserver
from fs_analyzer.model.file_categorization_strategy import FileCategorizerByExtension, FileCategorizerBySignature
from fs_analyzer.view_model.directory_analizer import DirectoryAnalizer
from fs_analyzer.model.file_permission_reporting_strategy import LooserPermissionsReporting, StricterPermissionsReporting


class DirectoryAnalizerFactory(ABC):
    @abstractmethod
    def create(self, directorypath:str, observer: DirectoryObserver)->DirectoryAnalizer:
        pass
    
class ExtensionDirectoryAnalizerFactory(DirectoryAnalizerFactory):
    def create(self, directorypath:str, observer: DirectoryObserver)->DirectoryAnalizer:
        return DirectoryAnalizer(directorypath, FileCategorizerByExtension(), StricterPermissionsReporting(), observer)

class SignatureDirectoryAnalizerFactory(DirectoryAnalizerFactory):
    def create(self, directorypath:str, observer: DirectoryObserver)->DirectoryAnalizer:
        return DirectoryAnalizer(directorypath, FileCategorizerBySignature(), StricterPermissionsReporting(), observer)
    
class LoosePermAnalyzerFactory(DirectoryAnalizerFactory):
    def create(self, directorypath:str, observer: DirectoryObserver)->DirectoryAnalizer:
        return DirectoryAnalizer(directorypath, FileCategorizerBySignature(), LooserPermissionsReporting(), observer) 
    
class StrictPermAnalyzerFactory(DirectoryAnalizerFactory):
    def create(self, directorypath:str, observer: DirectoryObserver)->DirectoryAnalizer:
        return DirectoryAnalizer(directorypath, FileCategorizerBySignature(), StricterPermissionsReporting(), observer) 