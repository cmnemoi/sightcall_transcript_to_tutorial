class TutorialGenerationError(Exception):
    """Raised when tutorial generation fails in the domain layer."""

    pass


class InvalidTranscriptError(TutorialGenerationError):
    """Raised when a transcript upload is invalid (bad JSON, missing fields, size, etc)."""

    pass
