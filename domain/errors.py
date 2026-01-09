class DomainError(Exception):
    pass


class ValidationError(DomainError):
    pass


class PaymentError(DomainError):
    pass
