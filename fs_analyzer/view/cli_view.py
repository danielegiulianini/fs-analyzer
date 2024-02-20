import typer
from typing import Set

from fs_analyzer.model import file_permissions, file_category
from fs_analyzer.view_model.directory_analizer_factory import ExtensionDirectoryAnalizerFactory, LoosePermAnalyzerFactory
from fs_analyzer.view.view import View

    
class CliView(View):

    def __init__(self):
        self.app = typer.Typer()
        self.app.command(name = "categorize", help="")(self.categorize_files)
        self.app.command(name = "fileperms", help="")(self.report_permissions)
        self.app.command(name = "catsizes", help="")(self.analize_category_sizes)
        self.app.command(name = "bigfiles", help="")(self.identify_large_files)

    def show(self):
        self.app()

    #(for optional argument: @app.command(name: Annotated[Optional[str], typer.Argument()] = None)
    def categorize_files(self, directory_path: str):
        #qui potrei aggiungere un po' di configurabilità (con l'oo istanzierei il giusto categorizer) in FP passerei il giusto HO
        print("filepath\t| category")
        print("------------------------------")
        ExtensionDirectoryAnalizerFactory().create(directory_path, self).categorize_files()

    def report_permissions(self, directory_path: str):
        #qui potrei aggiungere un po' di configurabilità (con l'oo istanzierei il giusto permissions checker) in FP passerei il giusto HO
        print("filepath\t| permissions")
        print("------------------------------")
        LoosePermAnalyzerFactory().create(directory_path, self).report_permissions()

    def analize_category_sizes(self, directory_path:str):
        print("category\t| size (B)")
        print("------------------------------")
        #configure
        ExtensionDirectoryAnalizerFactory().create(directory_path, self).analize_category_sizes()

    def identify_large_files(self, directory_path:str, size:int):
        print("filepath\t| size (B)")
        print("------------------------------")
        ExtensionDirectoryAnalizerFactory().create(directory_path, self).identify_large_files(size)


    #from here on I could have just a single method on(+ object of data class as argument)
    def on_new_categorized_file(self, filepath:str, filecategory: file_category.FileCategory)->None:
        #can align and trim if exceeding (#le path non possono essere piu di 256 chars!))
        print(filepath + " | " + str(filecategory))
        
    def on_new_file_category_size(self, filecategory: file_category.FileCategory, size:int)->None:
        print(str(filecategory) + " | " + str(size))

    def on_new_file_with_unusual_permission(self, filepath:str, permissions: Set[file_permissions.FilePermission])->None:
        print(filepath + " | " + str(permissions))
        
    def on_new_large_file(self, filepath:str, size:int)->None:
        print(filepath + " | " + str(size))


    #>errors (map to domain exceptions)
    def on_file_not_found(self)->None:
        # write to standard error(tyoer doesn't do it!)+ exit(1)
        print("ERROR: a file was not found")

    def on_directory_not_found(self)->None:
        # write to standard error?
        print("ERROR: directory not found. Please provide a existent directory")
        #here should exit
        
    def on_permission_error(self)->None:
        print("ERROR: a file was not found")

    #or invalid argument!
    def on_invalid_input(self, msg:str)->None:
        print("ERROR: a file was not found")

    def on_unknown_error(self)->None:
        print("ERROR: an unknown error occurred. Please run the cli with different input.")

