import pytest
from typer.testing import CliRunner

from fs_analyzer.view.cli_view import CliView

view = CliView()
runner = CliRunner()


#check required commands/arguments
def test_command_must_be_provided_to_cli():
    result = runner.invoke(view.app, [""])
    assert result.exit_code != 0

def test_directory_must_be_provided_to_categorize_command():
    result = runner.invoke(view.app, ["categorize"])
    assert result.exit_code != 0
    
def test_directory_must_be_provided_to_reporting_perm_command():
    result = runner.invoke(view.app, ["fileperms"])
    assert result.exit_code != 0

def test_directory_must_be_provided_large_files_command():
    result = runner.invoke(view.app, ["bigfiles"])
    assert result.exit_code != 0
    
def test_directory_must_be_provided_to_analyze_cat_sizes_command():
    result = runner.invoke(view.app, ["catsizes"])
    assert result.exit_code != 0

def test_size_argument_must_be_provided_to_large_files_command():
    result = runner.invoke(view.app, ["bigfiles", "directorypath/"])
    assert result.exit_code != 0

# check right command format
@pytest.mark.parametrize("command", ["categorizes", "bigfilesw", "catsizesll", "filepermspp"])
def test_correct_categorize_command_name_must_be_provided_to_cli(command): 
    result = runner.invoke(view.app, command)
    assert result.exit_code != 0


# check right # of arguments
def test_only_directory_argument_must_be_provided_to_categorize_command():
    result = runner.invoke(view.app, ["categorizes", "directorypath/", "uselessargument"])
    assert result.exit_code != 0

def test_only_directory_argument_must_be_provided_to_cat_sizes_command():
    result = runner.invoke(view.app, ["catsizes", "directorypath/", "uselessargument"])
    assert result.exit_code != 0
    
def test_only_directory_argument_must_be_provided_to_reporting_perm_command():
    result = runner.invoke(view.app, ["fileperms", "directorypath/", "uselessargument"])
    assert result.exit_code != 0

# check right argument format
def test_a_integer_size_argument_must_be_provided_to_large_files_command():
    result = runner.invoke(view.app, ["bigfiles", "./", "notaninteger"])
    assert result.exit_code != 0

def test_a_existent_directory_must_be_provided_to_categorize_command():
    result = runner.invoke(view.app, ["categorizes", "notvaliddirectory/"])
    assert result.exit_code != 0

def test_a_existent_directory_must_be_provided_to_cat_sizes_command():
    result = runner.invoke(view.app, ["catsizes", "notvaliddirectory/"])
    assert result.exit_code != 0
    
def test_a_existent_directory_must_be_provided_to_reporting_perm_command():
    result = runner.invoke(view.app, ["fileperms", "notvaliddirectory/"])
    assert result.exit_code != 0
    
def test_a_existent_directory_must_be_provided_to_large_files_command():
    result = runner.invoke(view.app, ["largefiles", "notvaliddirectory/", 2])
    assert result.exit_code != 0


