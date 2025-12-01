package codefloe.buriedincode.ecowitt

open class ServiceException(message: String? = null, cause: Throwable? = null) : Exception(message, cause)

class AuthenticationException(message: String? = null, cause: Throwable? = null) : ServiceException(message, cause)

class CacheException(message: String? = null, cause: Throwable? = null) : ServiceException(message, cause)

class RateLimitException(message: String? = null, cause: Throwable? = null) : ServiceException(message, cause)
