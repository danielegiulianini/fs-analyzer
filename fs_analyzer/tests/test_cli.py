import pytest
from typer.testing import CliRunner

from fs_analyzer.view.cli_view import CliView

view = CliView()
runner = CliRunner()



#### ERRRORS
#check required commands/arguments
def test_command_must_be_provided_to_cli():
    result = runner.invoke(view.app, [""])
    assert result.exit_code != 0    

def test_directory_must_be_provided_to_cli_when_categorizing():
    result = runner.invoke(view.app, ["categorize"])
    assert result.exit_code != 0
    
def test_directory_must_be_provided_to_cli_when_reporting_perm():
    result = runner.invoke(view.app, ["fileperms"])
    assert result.exit_code != 0

def test_directory_must_be_provided_to_cli_when_identifying_large_files():
    result = runner.invoke(view.app, ["bigfiles"])
    assert result.exit_code != 0
    
def test_directory_must_be_provided_to_cli_when_analyzing_cat_sizes():
    result = runner.invoke(view.app, ["catsizes"])
    assert result.exit_code != 0

def test_size_argument_must_provided_to_large_size_command():
    result = runner.invoke(view.app, ["bigfiles", "directorypath/"])
    assert result.exit_code != 0

#check right command format
@pytest.mark.parametrize("command", ["categorizes", "bigfilesw", "catsizesll", "filepermspp"])
def test_correct_categorize_command_name_must_be_provided_to_cli(command): 
    result = runner.invoke(view.app, command)
    assert result.exit_code != 0


#controlla se dai degli argomenti in più
#controlla se dai un non int per la size cosa succede
#controlla se dai un non stringa per la size cosa succede

#ORA testare TUTTI I METODI DI GUI ASSOCIATI ALL'OBSERVER


