class PaymentBaseError(Exception):
    """Must be inherited by all other custom Exception cases."""
    slug: str = "internal_error"
    code: int = 500


class SameIdempRequestError(PaymentBaseError):
    """Another request with same user_id/idempotency_key pair."""
    slug: str = "same_indent"
    code: int = 400


class NoIdempKeyError(PaymentBaseError):
    """No idempotency_key provided."""
    slug: str = "no_idemp_key"
    code: int = 400


class AccountNoExistsError(PaymentBaseError):
    """Account needs to be initialized before performing an operation."""
    slug: str = "account_not_exists"
    code: int = 400


class NoEnoughMoneyError(PaymentBaseError):
    """Not enough money for such operation."""
    slug: str = "not_enough_money"
    code: int = 400


class PotentialInjectionError(PaymentBaseError):
    """Unsafe SQl operation detected."""
    slug: str = "internal_error"
    code: int = 500
