package codefloe.buriedincode.ecowitt.schemas

import kotlinx.serialization.Serializable

@Serializable
data class LiveReading(val rainfall: Rainfall, val solarAndUvi: SolarAndUvi, val wind: Wind) {
  @Serializable data class Rainfall(val daily: Measurement<Double>)

  @Serializable data class SolarAndUvi(val solar: Measurement<Double>, val uvi: Measurement<Int>)

  @Serializable data class Wind(val windSpeed: Measurement<Double>)
}

@Serializable
data class HistoryReading(
  val rainfall: Rainfall? = null,
  val solarAndUvi: SolarAndUvi? = null,
  val wind: Wind? = null,
) {
  @Serializable data class Rainfall(val daily: MeasurementList<Double>)

  @Serializable data class SolarAndUvi(val solar: MeasurementList<Double>, val uvi: MeasurementList<Int>)

  @Serializable data class Wind(val windSpeed: MeasurementList<Double>)
}
