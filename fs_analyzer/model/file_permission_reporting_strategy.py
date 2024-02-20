from abc import ABC, abstractmethod
from ast import Set
from os import stat_result
from typing import Set

from fs_analyzer.model.file_permissions import *

class FilePermissionsReportingStrategy(ABC):
    @abstractmethod
    def report_unusual_permissions(self, stat:stat_result)->Set[FilePermission]:
        pass
    
class StricterPermissionsReporting(FilePermissionsReportingStrategy):
    
    #this is needed if view wants to display filepermission too (not only the names of the files with weird permissions)
    def report_unusual_permissions(self, stat:stat_result)->Set[FilePermission]:
        unusual_permissions = set()
        if is_world_executable(stat):
            unusual_permissions.add(UNUSUAL_PERMISSIONS["WORLD_EXECUTABLE"])
        return unusual_permissions

class LooserPermissionsReporting(FilePermissionsReportingStrategy):
    #this is needed if view wants to display filepermission too (not only filesnames with weird permissions)
    def report_unusual_permissions(self, stat:stat_result)->Set[FilePermission]:
        unusual_permissions = set()
        if is_world_executable(stat):
            unusual_permissions.add(UNUSUAL_PERMISSIONS["WORLD_EXECUTABLE"])
        if is_world_writable(stat):
            unusual_permissions.add(UNUSUAL_PERMISSIONS["WORLD_WRITABLE"])
        return unusual_permissions
