import importlib
import logging
from typing import Union, Optional, Any

from common.config_manager import ConfigManager
from common._libs.helpers.singleton import Singleton
from common._libs.logger import PyCatsLogger


class PyCatsError(Exception):
    pass


class FacadeError(Exception):
    pass


class PyCatsFacade(metaclass=Singleton):

    def __init__(self):
        self._config_manager: Optional[ConfigManager] = None
        self._logger: Optional[PyCatsLogger] = None

    @property
    def config_manager(self) -> ConfigManager:
        if not self._config_manager:
            raise FacadeError("Config was not initialized yet. Please initialize it firstly")
        return self._config_manager

    @config_manager.setter
    def config_manager(self, config):
        if self._config_manager:
            raise FacadeError("Config was already initialized. Facade update is forbidden")
        self.setup_config(config)

    @property
    def logger(self):
        if not self._logger:
            raise FacadeError("Logger was not initialized yet. Please initialize it firstly")
        return self._logger

    @logger.setter
    def logger(self, logger):
        if self._logger:
            raise FacadeError("Logger was already initialized. Facade update is forbidden")
        self.setup_logger(logger)

    def setup_config(self, config: Union[Any, ConfigManager] = None, config_dir: str = None):
        self._config_manager = config or ConfigManager(config_dir)

    def setup_logger(self, logger_instance):
        if not self._config_manager:
            raise FacadeError("Logger can not be setup before config. Please setup config before")
        if logger_instance:
            self._logger = logger_instance
        else:
            PyCatsLogger.base_log_dir = self.config_manager.config.global_settings.logdir
            PyCatsLogger.log_level = self.config_manager.config.global_settings.log_level
            PyCatsLogger.enable_libs_logging = self.config_manager.config.global_settings.enable_libs_logging
            self._logger = PyCatsLogger(logging.getLogger(__name__))
            self._replace_submodules_logger(exclude=["common.facade"])

    @staticmethod
    def _replace_submodules_logger(package="common", exclude=None):
        """ Import all submodules of a module based on the __all__ variable in __init__.py,
        including subpackages and replace built in logger with pycats configured logger
        """
        if isinstance(package, str):
            package = importlib.import_module(package)
        submodules_names = package.__all__
        for name in submodules_names:
            if name not in exclude:
                module = importlib.import_module(name)
                try:
                    getattr(module, "logger")
                except AttributeError:
                    pass
                else:
                    module.logger = PyCatsLogger(logging.getLogger(name))
