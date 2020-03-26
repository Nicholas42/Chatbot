import logging

from .. import module_logger as parent_logger

module_logger: logging.Logger = parent_logger.getChild("connection")
