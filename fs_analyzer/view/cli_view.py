import typer
from typing import Set

from fs_analyzer.model import file_permissions, file_category
from fs_analyzer.view_model.directory_analizer_factory import ExtensionDirectoryAnalizerFactory, LoosePermAnalyzerFactory
from fs_analyzer.view.view import View


class CliView(View):
    """
        Represents a command line interface (CLI) application for accessing the file-system analysis and reporting functionalities. 
    """

    def __init__(self):
        self.app = typer.Typer()
        self.app.command(name = "categorize", help="Classify files into mime/types (e.g., image/jpeg).")(self.categorize_files)
        self.app.command(name = "fileperms", help="List files with unusual permission settings.")(self.report_permissions)
        self.app.command(name = "catsizes", help="Display the total size per category of files.")(self.analize_category_sizes)
        self.app.command(name = "bigfiles", help="List the files above SIZE")(self.identify_large_files)

        """ Displays the CLI app.
        """
    def show(self):
        self.app()

        """ Triggers the classification of the files contained in `directory_path`."""    
    def categorize_files(self, directory_path: str):
        print("filepath\t| category")
        print("------------------------------")
        ExtensionDirectoryAnalizerFactory().create(directory_path, self).categorize_files()

        """ Triggers the permissions settings report generation for the files contained in `directory_path`."""
    def report_permissions(self, directory_path: str):
        print("filepath\t| permissions")
        print("------------------------------")
        LoosePermAnalyzerFactory().create(directory_path, self).report_permissions()

        """ Triggers the analysis of the sizes of each file category for the files contained in `directory_path`."""
    def analize_category_sizes(self, directory_path:str):
        print("category\t| size (B)")
        print("------------------------------")
        ExtensionDirectoryAnalizerFactory().create(directory_path, self).analize_category_sizes()

        """ Triggers the identification of the files with size greater than `size` contained in `directory_path`."""
    def identify_large_files(self, directory_path:str, size:int):
        print("filepath\t| size (B)")
        print("------------------------------")
        ExtensionDirectoryAnalizerFactory().create(directory_path, self).identify_large_files(size)


    def on_new_categorized_file(self, filepath:str, 
                                filecategory: file_category.FileCategory)->None:
        print(filepath + "\t| " + str(filecategory.name))
        
    def on_new_file_category_size(self, filecategory: file_category.FileCategory, 
                                  size:int)->None:
        print(str(filecategory) + "\t| " + str(size))

    def on_new_file_with_unusual_permission(self, filepath:str, 
                                            permissions: Set[file_permissions.FilePermission])->None:
        print(filepath + "\t| " + str(set(map(lambda fp:fp.name, permissions))))
        
    def on_new_large_file(self, filepath:str, size:int)->None:
        print(filepath + "\t| " + str(size))


    #>errors (map to domain exceptions)
    def on_file_not_found(self)->None:
        print("ERROR: a file was not found")
        
    def on_directory_not_found(self)->None:
        print("ERROR: directory not found. Please provide a existent directory")
        
    def on_permission_error(self)->None:
        print("ERROR: a file was not found")
        
    def on_unknown_error(self)->None:
        print("ERROR: an unknown error occurred.")
        
    def on_directory_provided_not_found(self)->None:
        print("ERROR: directory not found. Please provide a existent directory")
        raise typer.Aborted()
    
    def on_directory_provided_not_accessible(self)->None:
        print("ERROR: directory not found. Please provide a directory for which you have permissions")
        raise typer.Aborted()

    #or invalid argument!
    def on_invalid_input(self, msg:str)->None:
        print("ERROR: the input you provided is not valid")
        raise typer.Aborted()
