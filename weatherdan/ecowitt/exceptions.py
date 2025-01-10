__all__ = ["AuthenticationError", "ServiceError"]


class ServiceError(Exception):
    pass


class AuthenticationError(ServiceError):
    pass
