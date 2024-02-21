from os import stat_result
import stat
from dataclasses import dataclass


@dataclass(frozen=True)
class FilePermission:
    name: str


UNUSUAL_PERMISSIONS = {
    "WORLD_WRITABLE" : FilePermission("WORLD_EXECUTABLE"),
    "WITH_ANY_OWNER_PERMISSIONS" : FilePermission("WITH_ANY_OWNER_PERMISSIONS"),
    "WORLD_WRITABLE" : FilePermission("WORLD_WRITABLE"),
    "IS_SUID_ENABLED" : FilePermission("IS_SUID_ENABLED"),
    "IS_GUID_ENABLED": FilePermission("IS_GUID_ENABLED"),
}

#in priority order
def is_world_writable(st:stat_result):
    return bool(st.st_mode & stat.S_IWGRP)

def is_without_any_permission_by_owner(st:stat_result):
    return not bool(st.st_mode & stat.S_IRWXU)

def is_world_executable(st:stat_result):
    return bool(st.st_mode & stat.S_IXOTH)

def is_suid_enabled(st:stat_result):
    return bool(st.st_mode & stat.S_ISUID)

def is_guid_enabled(st:stat_result):
    return bool(st.st_mode & stat.S_IGUID)