__all__ = ["ServiceError", "AuthenticationError"]


class ServiceError(Exception):
    pass


class AuthenticationError(ServiceError):
    pass
