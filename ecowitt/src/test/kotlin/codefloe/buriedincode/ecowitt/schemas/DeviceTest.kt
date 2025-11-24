package codefloe.buriedincode.ecowitt.schemas

import codefloe.buriedincode.ecowitt.Ecowitt
import codefloe.buriedincode.ecowitt.SQLiteCache
import codefloe.buriedincode.ecowitt.ServiceException
import java.nio.file.Paths
import kotlin.time.ExperimentalTime
import kotlin.time.Instant
import kotlinx.datetime.TimeZone
import org.junit.jupiter.api.Assertions.assertEquals
import org.junit.jupiter.api.Assertions.assertNotNull
import org.junit.jupiter.api.Assertions.assertThrows
import org.junit.jupiter.api.Assertions.assertTrue
import org.junit.jupiter.api.Nested
import org.junit.jupiter.api.Test
import org.junit.jupiter.api.TestInstance
import org.junit.jupiter.api.assertAll

@TestInstance(TestInstance.Lifecycle.PER_CLASS)
class DeviceTest {
  private val session: Ecowitt

  init {
    val applicationKey = System.getenv("ECOWITT__APPLICATION_KEY") ?: "IGNORED"
    val apiKey = System.getenv("ECOWITT__API_KEY") ?: "IGNORED"
    val cache = SQLiteCache(path = Paths.get("cache.sqlite"), expiry = null)
    this.session = Ecowitt(applicationKey = applicationKey, apiKey = apiKey, cache = cache)
  }

  @Nested
  inner class ListDevices {
    @OptIn(ExperimentalTime::class)
    @Test
    fun `Test ListDevices`() {
      val results = session.listDevices()
      assertEquals(1, results.size)
      val result = results[0]
      assertAll(
        { assertEquals(Instant.fromEpochSeconds(1662849729), result.createdAt) },
        { assertEquals(TimeZone.of("Australia/Sydney"), result.timezone) },
        { assertEquals(98032, result.id) },
        { assertTrue(result.iotDevices.isEmpty()) },
        { assertEquals(-34.132563, result.latitude) },
        { assertEquals(150.636475, result.longitude) },
        { assertEquals("98:CD:AC:31:4F:F1", result.macAddress) },
        { assertEquals("GW1100", result.name) },
        { assertEquals("GW1100C_V2.0.4", result.stationType) },
        { assertEquals(BaseDevice.DeviceType.WEATHER_STATION, result.type) },
      )
    }
  }

  @Nested
  inner class GetDevice {
    @OptIn(ExperimentalTime::class)
    @Test
    fun `Test GetDevice`() {
      val result = session.getDevice(macAddress = "98:CD:AC:31:4F:F1")
      assertNotNull(result)
      assertAll(
        { assertEquals(38, result.lastUpdate.wind.windDirection.value) },
        { assertEquals("º", result.lastUpdate.wind.windDirection.unit) },
        { assertEquals(Instant.fromEpochSeconds(1763952167), result.lastUpdate.wind.windDirection.timestamp) },
      )
    }

    @Test
    fun `Test GetDevice with an invalid MAC address`() {
      assertThrows(ServiceException::class.java) { session.getDevice(macAddress = "invalid") }
    }
  }
}
