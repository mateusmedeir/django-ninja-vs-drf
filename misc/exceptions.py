class DomainError(Exception):
    """A business rule refused the operation. Each API edge turns it into an HTTP response."""

    status_code = 400
    message = 'The operation was refused.'

    def __init__(self, message: str | None = None):
        super().__init__(message or self.message)
