from abc import ABC, abstractmethod

from fs_analyzer.view_model.directory_observer import DirectoryObserver
from fs_analyzer.view_model.directory_analizer import DirectoryAnalizer
from fs_analyzer.model.file_categorization_strategy import FileCategorizerByExtension, FileCategorizerBySignature
from fs_analyzer.model.file_permission_reporting_strategy import LooserPermissionsReporting, StricterPermissionsReporting


class DirectoryAnalizerFactory(ABC):
    """An abstract factory for creating the most suitable directory analyzer 
    according to user needs, by leveraging the creational "Abstract Factory" 
    Object-Oriented design pattern.
    """
    @abstractmethod
    def create(self, directory_path:str, 
               directory_observer: DirectoryObserver)->DirectoryAnalizer:
        pass


class ExtensionDirectoryAnalizerFactory(DirectoryAnalizerFactory):
    """A concrete factory for creating directory analyzers that classifies files according
    to their extension (e.g., txt, jpeg). It inherits from 
    fs_analyzer.viewmodel.directory_analizer_factory.DirectoryAnalizerFactory.
    """
    def create(self, directory_path:str, 
               directory_observer: DirectoryObserver)->DirectoryAnalizer:
        return DirectoryAnalizer(directory_path, 
                                 FileCategorizerByExtension(), 
                                 StricterPermissionsReporting(), 
                                 directory_observer)

class SignatureDirectoryAnalizerFactory(DirectoryAnalizerFactory):
    """A concrete factory for creating directory analyzers that classifies files according
    to their file signature. It inherits from 
    fs_analyzer.viewmodel.directory_analizer_factory.DirectoryAnalizerFactory.
    """
    def create(self, directory_path:str, 
               directory_observer: DirectoryObserver)->DirectoryAnalizer:
        return DirectoryAnalizer(directory_path, 
                                 FileCategorizerBySignature(), 
                                 StricterPermissionsReporting(), 
                                 directory_observer)
    
class LoosePermAnalyzerFactory(DirectoryAnalizerFactory):
    """A concrete factory for creating directory analyzers that identifies unusual
    file permissions setting with a loose policy. It inherits from 
    fs_analyzer.viewmodel.directory_analizer_factory.DirectoryAnalizerFactory.
    """
    def create(self, directory_path:str, 
               directory_observer: DirectoryObserver)->DirectoryAnalizer:
        return DirectoryAnalizer(directory_path, 
                                 FileCategorizerBySignature(), 
                                 LooserPermissionsReporting(), 
                                 directory_observer) 
    
class StrictPermAnalyzerFactory(DirectoryAnalizerFactory):
    """A concrete factory for creating directory analyzers that identifies unusual
    file permissions setting with a strict policy. It inherits from 
    fs_analyzer.viewmodel.directory_analizer_factory.DirectoryAnalizerFactory.
    """
    def create(self, directory_path:str, 
               directory_observer: DirectoryObserver)->DirectoryAnalizer:
        return DirectoryAnalizer(directory_path, 
                                 FileCategorizerBySignature(), 
                                 StricterPermissionsReporting(), 
                                 directory_observer) 