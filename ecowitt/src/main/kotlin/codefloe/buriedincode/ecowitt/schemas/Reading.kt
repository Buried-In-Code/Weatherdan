package codefloe.buriedincode.ecowitt.schemas

import kotlinx.serialization.Serializable

@Serializable
data class RainfallReading(val rainfall: Rainfall) {
  @Serializable data class Rainfall(val daily: Measurement<Double>)
}

@Serializable
data class SolarReading(val solarAndUvi: Solar) {
  @Serializable data class Solar(val solar: Measurement<Double>)
}
