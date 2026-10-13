from misc.exceptions import DomainError


class TertiaryGroupOutOfScopeError(DomainError):
    message = 'Church not found in your scope.'


class DonationNotCancelableError(DomainError):
    status_code = 409
    message = 'Only pending donations can be canceled.'
