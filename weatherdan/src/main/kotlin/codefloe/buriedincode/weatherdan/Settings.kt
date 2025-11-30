package codefloe.buriedincode.weatherdan

import codefloe.buriedincode.ecowitt.schemas.CapacityUnit
import codefloe.buriedincode.ecowitt.schemas.PressureUnit
import codefloe.buriedincode.ecowitt.schemas.RainfallUnit
import codefloe.buriedincode.ecowitt.schemas.SolarIrradianceUnit
import codefloe.buriedincode.ecowitt.schemas.TempUnit
import codefloe.buriedincode.ecowitt.schemas.WindSpeedUnit
import com.sksamuel.hoplite.ConfigLoaderBuilder
import com.sksamuel.hoplite.ExperimentalHoplite
import com.sksamuel.hoplite.addPathSource
import com.sksamuel.hoplite.addResourceSource
import kotlin.io.path.div

data class Settings(
  val ecowitt: Ecowitt,
  val environment: Environment,
  val ssl: SSL? = null,
  val units: Units,
  val website: Website,
) {
  data class Ecowitt(val applicationKey: String, val apiKey: String)

  enum class Environment {
    DEV,
    PROD,
  }

  data class SSL(val trustStore: String, val password: String)

  data class Units(
    val temp: TempUnit,
    val pressure: PressureUnit,
    val windSpeed: WindSpeedUnit,
    val rainfall: RainfallUnit,
    val solarIrradiance: SolarIrradianceUnit,
    val capacity: CapacityUnit,
  )

  data class Website(val host: String, val port: Int)

  companion object {
    @OptIn(ExperimentalHoplite::class)
    fun load(): Settings =
      ConfigLoaderBuilder.default()
        .withExplicitSealedTypes()
        .addPathSource(Utils.CONFIG_ROOT / "settings.properties", optional = true, allowEmpty = true)
        .addResourceSource("/default.properties")
        .build()
        .loadConfigOrThrow<Settings>()
  }
}
