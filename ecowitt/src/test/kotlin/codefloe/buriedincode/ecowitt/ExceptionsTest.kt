package codefloe.buriedincode.ecowitt

import kotlin.jvm.java
import kotlin.time.Duration.Companion.milliseconds
import org.junit.jupiter.api.Assertions.assertThrows
import org.junit.jupiter.api.Nested
import org.junit.jupiter.api.Test
import org.junit.jupiter.api.TestInstance
import org.junit.jupiter.api.TestInstance.Lifecycle

@TestInstance(Lifecycle.PER_CLASS)
class ExceptionsTest {
  @Nested
  inner class Authentication {
    @Test
    fun `Test throwing an AuthenticationException`() {
      val session = Ecowitt(applicationKey = "invalid", apiKey = "invalid", cache = null)
      assertThrows(AuthenticationException::class.java) { session.listDevices() }
    }
  }

  @Nested
  inner class Service {
    @Test
    fun `Test throwing a ServiceException for a 404`() {
      val applicationKey = System.getenv("ECOWITT__APPLICATION_KEY") ?: "IGNORED"
      val apiKey = System.getenv("ECOWITT__API_KEY") ?: "IGNORED"
      val session = Ecowitt(applicationKey = applicationKey, apiKey = apiKey, cache = null)
      assertThrows(ServiceException::class.java) {
        val uri = session.encodeURI(endpoint = "/invalid")
        session.getRequest(uri = uri)
      }
    }

    @Test
    fun `Test throwing a ServiceException for a timeout`() {
      val applicationKey = System.getenv("ECOWITT__APPLICATION_KEY") ?: "IGNORED"
      val apiKey = System.getenv("ECOWITT__API_KEY") ?: "IGNORED"
      val session = Ecowitt(applicationKey = applicationKey, apiKey = apiKey, cache = null, timeout = 1.milliseconds)
      assertThrows(ServiceException::class.java) { session.listDevices() }
    }
  }
}
