import typer
from typing import Set

from fs_analyzer.model import file_permissions, file_category
from fs_analyzer.view_model.directory_analizer_factory import ExtensionDirectoryAnalizerFactory, LoosePermAnalyzerFactory
from fs_analyzer.view.view import View


class CliView(View):
    """Represents a command line interface (CLI) application for accessing the file-system 
        analysis and reporting functionalities. 
    """

    def __init__(self):
        self.app = typer.Typer()
        self.app.command(name = "categorize", 
                         help="Classify files into mime/types (e.g., image/jpeg).")(self.categorize_files)
        self.app.command(name = "fileperms",
                         help="List files with unusual permission settings.")(self.report_permissions)
        self.app.command(name = "catsizes", 
                         help="Display the total size per category of files.")(self.analize_category_sizes)
        self.app.command(name = "bigfiles", 
                         help="List the files above SIZE")(self.identify_large_files)

        
    def show(self):
        """ Displayes the CLI app."""
        self.app()

           
    def categorize_files(self, directory_path: str):
        """Triggers the classification of the files contained in directory_path provided.
        
        Args:
            directory_path (str): the path where the directory root to be analyzed
                of the tree resides
        """
        print("filepath\t| category")
        print("------------------------------")
        ExtensionDirectoryAnalizerFactory().create(directory_path, self).categorize_files()

        
    def report_permissions(self, directory_path: str):
        """ Triggers the permissions settings report generation for the files contained in `directory_path`.
        
        Args:
            directory_path (str): the path where the directory root to be analyzed
                of the tree resides.
        """
        
        print("filepath\t| permissions")
        print("------------------------------")
        LoosePermAnalyzerFactory().create(directory_path, self).report_permissions()

        
    def analize_category_sizes(self, directory_path:str):
        """ Triggers the analysis of the category sizes.
        
        Args:
            directory_path (str): the path where the directory root to be analyzed
                of the tree resides.
        """
        print("category\t| size (B)")
        print("------------------------------")
        ExtensionDirectoryAnalizerFactory().create(directory_path, self).analize_category_sizes()

    def identify_large_files(self, directory_path:str, size:int):
        """ Triggers the identification of the files larger than size.
        
        Args:
            directory_path (str): the path where the directory root to be analyzed
                of the tree resides.
        """
        print("filepath\t| size (B)")
        print("------------------------------")
        ExtensionDirectoryAnalizerFactory().create(directory_path, self).identify_large_files(size)


    def on_new_categorized_file(self, file_path:str, 
                                file_category: file_category.FileCategory)->None:
        print(file_path + "\t| " + str(file_category.name))
        
    def on_new_file_category_size(self, files_category: file_category.FileCategory, 
                                  category_size:int)->None:
        print(str(files_category) + "\t| " + str(category_size))

    def on_new_file_with_unusual_permission(self, filepath:str, 
                                            permissions: Set[file_permissions.FilePermission])->None:
        print(filepath + "\t| " + str(set(map(lambda fp:fp.name, permissions))))
        
    def on_new_large_file(self, file_path:str, file_size:int)->None:
        print(file_path + "\t| " + str(file_size))


    def on_file_not_found(self)->None:
        print("ERROR: a file was not found")
        
    def on_directory_not_found(self)->None:
        print("ERROR: directory not found.")
        
    def on_permission_error(self)->None:
        print("ERROR: a file was not found")
        
    def on_unknown_error(self)->None:
        print("ERROR: an unknown error occurred.")

    def on_invalid_input(self)->None:
        print("ERROR: the input you provided is not valid.")
        raise typer.Abort()
