class Error(Exception):
    """Base class for exceptions in this module."""

    pass


class PandocGenerationError(Error):
    """Pandoc generation error"""

    def __init__(self, description):
        self.message = description


class DocumentError(Error):
    """Document error"""

    def __init__(self, description):
        self.message = description
