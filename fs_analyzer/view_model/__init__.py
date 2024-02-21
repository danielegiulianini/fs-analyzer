"""fs analizer'view model

This package contains the intermediary abstractions between fs_analizer's view 
and model, responsible for managing the view logic by means of a 
publish/subscribe model. That way, business logic is separated from the user 
interface, allowing to reuse this package with different, possibly future, versions
of it.
    
In particular,

Modules:
* directory_analyzer_factory.py: contains some factories for creating the analyzer most
    suited to the app user.
* directory_analyzer.py: contains the class responsible for interaction between the
    directory tree domain and who is interested in it (like, but not necessarily, the view).
* directory_observer.py: contains the class defining the abstraction of observer of
    the analysis outcomes of directory traversal.

Besides typing and fs_analyzer's model and view modules, the package does not depend
on third-party modules.

"""