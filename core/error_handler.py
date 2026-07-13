import logging

class JosehError(Exception):
    def __init__(self, message, _logger):
        super().__init__(message)
        if _logger:
            _logger.error(message)

class NLPError(JosehError):
    _logger = logging.getLogger("NLP")
    def __init__(self, message):
        super().__init__(message, self._logger)

class InvalidCommand(NLPError):
    pass

class NoNounDetected(NLPError):
    pass

class ToolboxError(JosehError):
    _logger = logging.getLogger("TB")
    def __init__(self, message):
        super().__init__(message, self._logger)

class FlatpakModuleError(ToolboxError):
    pass

class ProgramNotFound(ToolboxError):
    pass

class ProgramAlreadyInstalled(ToolboxError):
    pass

class SpotifyError(JosehError):
    _logger = logging.getLogger("SP")
    def __init__(self, message):
        super().__init__(message, self._logger)

class SpotifyTrackNotFound(SpotifyError):
    pass

class BuiltInCommandsError(JosehError):
    _logger = logging.getLogger("BIC")
    def __init__(self, message, _logger):
        super().__init__(message, _logger)

class BICommandNotFound(BuiltInCommandsError):
    pass

class CustomCommandError(JosehError):
    _logger = logging.getLogger("CC")
    def __init__(self, message, _logger):
        super().__init__(message, _logger)

class CredentialCheckerError(JosehError):
    _logger = logging.getLogger("CRE")
    def __init__(self, message, _logger):
        super().__init__(message, _logger)