from abc import ABC, abstractmethod
from ast import Set
from os import stat_result
from typing import Set

from fs_analyzer.model.file_permissions import *

class FilePermissionsReportingStrategy(ABC):
    """An abstract class representing a strategy for reporting unusual permission settings
    of files, modeled through the behavioural "Strategy" OO pattern.
    It isolates the permission reporting logic so allowing to reuse it in different scenarios
    and make its implementations interchangeable without affecting the context using them, as well
    as to make the current context compatible with future implementations.
    """
    @abstractmethod
    def report_unusual_permissions(self, stat:stat_result)->Set[FilePermission]:
        """Reports the file permissions deemed as unusual.

        Args:
            stat (stat_result): the data structure containing file-related info.

        Returns:
            Set[FilePermission]: The file permissions considered unusual.
        """
        pass
    
class StricterPermissionsReporting(FilePermissionsReportingStrategy):
    """Deem as unusual the files which can be executed by anyone.

    Args:
        FilePermissionsReportingStrategy (_type_): the abstract permissions reporting strategy.
    """
    def report_unusual_permissions(self, stat:stat_result)->Set[FilePermission]:
        unusual_permissions = set()
        if is_world_executable(stat):
            unusual_permissions.add(UNUSUAL_PERMISSIONS["WORLD_EXECUTABLE"])
        return unusual_permissions

class LooserPermissionsReporting(FilePermissionsReportingStrategy):
    """Deem as unusual the files which can be executed and written by anyone.

    Args:
        FilePermissionsReportingStrategy (_type_): the abstract file permissions reporting strategy.
    """
    def report_unusual_permissions(self, stat:stat_result)->Set[FilePermission]:
        unusual_permissions = set()
        if is_world_executable(stat):
            unusual_permissions.add(UNUSUAL_PERMISSIONS["WORLD_EXECUTABLE"])
        if is_world_writable(stat):
            unusual_permissions.add(UNUSUAL_PERMISSIONS["WORLD_WRITABLE"])
        return unusual_permissions
