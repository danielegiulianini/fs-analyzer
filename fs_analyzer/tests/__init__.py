"""fs analizer'tests

This packages contains some test cases for the fs_analyzer app.


In particular, 

Modules:

* test_cli.py: test the correct input validation performed by the CLI.
* test_directory_analizer.py: checking the graceful degradation in case of 
    unexpected situations.
* test_generators.py: containing the tests of the lower level file-listing generators,
    among which those of graceful degradation in case of unexpected situations.
* utils.py: containing some utils for testing along with a testing scenario.

It employs unittest and pytest.

"""