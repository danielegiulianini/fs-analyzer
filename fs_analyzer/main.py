"""File system analyzer 

This script is the entry point for fs_analyzer, a command line application that
analyzes and reports on the file system structure and usage.
To use the tool you must specify this syntax at the prompt:

    main.py [OPTIONS] COMMAND [ARGS]...
    
where the options are:
    * --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
    * --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.
    * --help                      Show this message and exit.

and the commands are:
    * bigfiles    List the files above SIZE
    * categorize  Classify files into mime/types (e.g., image/jpeg).
    * catsizes    Display the total size per category of files.
    * fileperms   List files with unusual permission settings.
    
This file can also be imported as a module and contains the function:

    * main - the main function of the script
    
"""

from fs_analyzer.view.cli_view import CliView

def main():
    CliView().show()

if __name__ == "__main__":
    main()