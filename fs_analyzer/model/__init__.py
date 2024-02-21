"""fs analizer'model

This package contain some reusable classes and generators to analyze 
and report on the file system structure and usage, designed for handling
large directories. They are reusable outside of the scope of the fs_analyzer 
command line application.
    
In particular,

Modules:
* file_categorization_strategy.py: containing some interchangeable strategies for 
    classifying files, modeled through the so-called "Strategy" Object-Oriented
    (OO) design pattern.
* file_category.py: containing the definition of the class representing the abstraction
    of file category.
* file_listing_generators.py: containing many reusable generators of
    information like size, category and permissions regarding the files of a 
    specified directory tree, suitable for exploring large directories.
* file_permission_reporting_strategy.py: containing some interchangeable strategies for 
    identifying files with unusual permission settings, modeled through the so-called 
    "Strategy" OO design pattern.
* file_permissions.py: containing the definition of the class representing the abstraction 
    of file permission.

"""