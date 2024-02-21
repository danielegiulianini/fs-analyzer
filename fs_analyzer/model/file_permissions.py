from os import stat_result
import stat
from dataclasses import dataclass


@dataclass(frozen=True)
class FilePermission:
    """ Represents a file permission setting of a file. Instances of this class 
    cannot be edited at runtime.
    
    Args:
        name (str): a human-readable name for the file permission assigned to the file.

    """
    name: str

    """Some file permissions considered unusual.
    """
UNUSUAL_PERMISSIONS = {
    "WORLD_WRITABLE" : FilePermission("WORLD_EXECUTABLE"),
    "WITH_ANY_OWNER_PERMISSIONS" : FilePermission("WITH_ANY_OWNER_PERMISSIONS"),
    "WORLD_WRITABLE" : FilePermission("WORLD_WRITABLE"),
    "IS_SUID_ENABLED" : FilePermission("IS_SUID_ENABLED"),
    "IS_GUID_ENABLED": FilePermission("IS_GUID_ENABLED"),
}


def is_world_writable(st:stat_result)->bool:
    """Checks if the os.stat_result provided indicates if 
    anyone can write the associated file.

    Args:
        st (stat_result): the os.stat_result associated to the file to inspect.

    Returns:
        bool: whether or not the file is world-writable.
    """
    return bool(st.st_mode & stat.S_IWGRP)

def is_without_any_permission_by_owner(st:stat_result)->bool:
    """Checks if the os.stat_result provided indicates if 
    the owner has any permission on the associated file.

    Args:
        st (stat_result): the os.stat_result associated to the file to inspect.

    Returns:
        bool: whether or not the file is without any permission by the owner.
    """
    return not bool(st.st_mode & stat.S_IRWXU)

def is_world_executable(st:stat_result)->bool:
    """Checks if the os.stat_result provided indicates if 
    anyone can execute the associated file.

    Args:
        st (stat_result): the os.stat_result associated to the file to inspect.

    Returns:
        bool: whether or not the file is world-executable.
    """
    return bool(st.st_mode & stat.S_IXOTH)

def is_suid_enabled(st:stat_result)->bool:
    """Checks if the os.stat_result provided indicates if 
    the setuid bit is enabled.

    Args:
        st (stat_result): the os.stat_result associated to the file to inspect.

    Returns:
        bool: whether or not the file has the setuid bit enabled.
    """
    return bool(st.st_mode & stat.S_ISUID)

def is_guid_enabled(st:stat_result)->bool:
    """Checks if the os.stat_result provided indicates if 
    the setguid bit is enabled.

    Args:
        st (stat_result): the os.stat_result associated to the file to inspect.

    Returns:
        bool: whether or not the file has the setguid bit enabled.
    """
    return bool(st.st_mode & stat.S_IGUID)