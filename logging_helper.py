import logging


class LoggingHelper:
    """Provides logging to all child classes."""

    @property
    def logger(self) -> logging.Logger:
        """Logging property."""
        name = f"{self.__class__.__module__}.{self.__class__.__name__}"
        return logging.getLogger(name)
