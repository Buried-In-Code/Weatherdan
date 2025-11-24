package codefloe.buriedincode.ecowitt.schemas

import codefloe.buriedincode.ecowitt.serializers.DeviceTypeSerializer
import kotlin.time.ExperimentalTime
import kotlin.time.Instant
import kotlinx.datetime.TimeZone
import kotlinx.serialization.ExperimentalSerializationApi
import kotlinx.serialization.Serializable
import kotlinx.serialization.SerializationException
import kotlinx.serialization.json.JsonNames

@OptIn(ExperimentalTime::class)
@Serializable
sealed class BaseDevice {
  abstract val createdAt: Instant
  abstract val timezone: TimeZone
  abstract val id: Long
  abstract val latitude: Double
  abstract val longitude: Double
  abstract val macAddress: String
  abstract val name: String
  abstract val stationType: String
  abstract val type: DeviceType

  @Serializable(with = DeviceTypeSerializer::class)
  enum class DeviceType(val value: Int) {
    WEATHER_STATION(value = 1),
    CAMERA(value = 2);

    companion object {
      fun fromInt(value: Int): DeviceType {
        return entries.firstOrNull { it.value == value }
          ?: throw SerializationException("Unknown DeviceType value: $value")
      }
    }
  }
}

@OptIn(ExperimentalSerializationApi::class, ExperimentalTime::class)
@Serializable
data class BasicDevice(
  @JsonNames("createtime") private val createdEpoch: Long,
  @JsonNames("date_zone_id") override val timezone: TimeZone,
  override val id: Long,
  override val latitude: Double,
  override val longitude: Double,
  @JsonNames("mac") override val macAddress: String,
  override val name: String,
  @JsonNames("stationtype") override val stationType: String,
  override val type: DeviceType,
  @JsonNames("iotdevice_list") val iotDevices: List<IotDevice>,
) : BaseDevice() {
  override val createdAt: Instant
    get() = Instant.fromEpochSeconds(createdEpoch)

  @OptIn(ExperimentalSerializationApi::class, ExperimentalTime::class)
  @Serializable
  data class IotDevice(
    @JsonNames("createtime") val createdAt: Instant,
    val defaultTitle: String,
    val deviceId: String,
    val name: String,
    val version: String,
  )
}

@OptIn(ExperimentalSerializationApi::class, ExperimentalTime::class)
@Serializable
data class Device(
  @JsonNames("createtime") private val createdEpoch: Long,
  @JsonNames("date_zone_id") override val timezone: TimeZone,
  override val id: Long,
  override val latitude: Double,
  override val longitude: Double,
  @JsonNames("mac") override val macAddress: String,
  override val name: String,
  @JsonNames("stationtype") override val stationType: String,
  override val type: DeviceType,
  val lastUpdate: Details,
) : BaseDevice() {
  override val createdAt: Instant
    get() = Instant.fromEpochMilliseconds(createdEpoch)

  @Serializable
  data class Details(
    val battery: BatteryMeasurements,
    val co2AqiCombo: AirQualityMeasurements,
    val indoor: IndoorMeasurements,
    val lightning: LightningMeasurements,
    val outdoor: OutdoorMeasurements,
    val pm10AqiCombo: AirQuality10Measurements,
    val pm25AqiCombo: AirQuality25Measurements,
    val pm25Ch1: AirQuality25Measurements,
    val pm25Ch2: AirQuality25Measurements,
    val pm25Ch3: AirQuality25Measurements,
    val pm25Ch4: AirQuality25Measurements,
    val pressure: PressureMeasurements,
    val rainfall: RainfallMeasurements,
    val soilCh1: SoilMeasurements,
    val soilCh2: SoilMeasurements,
    val soilCh3: SoilMeasurements,
    val solarAndUvi: SolarUVIndexMeasurements,
    val tRhAqiCombo: TemperatureHumidityComboMeasurements,
    val tempAndHumidityCh3: TemperatureMeasurements,
    val tempCh3: TemperatureMeasurements,
    val waterLeak: WaterLeakMeasurements,
    val wind: WindMeasurements,
  ) {
    @Serializable
    data class BatteryMeasurements(
      val hapticArrayBattery: Measurement<Double>,
      val leafWetnessSensorCh2: Measurement<Double>,
      val leafWetnessSensorCh3: Measurement<Double>,
      val rainfallSensor: Measurement<Double>,
      val sensorArray: Measurement<Int>,
      val soilmoistureSensorCh1: Measurement<Double>,
      val soilmoistureSensorCh2: Measurement<Double>,
      val tempHumiditySensorCh3: Measurement<Int>,
      val temperatureSensorCh1: Measurement<Double>,
      val temperatureSensorCh3: Measurement<Double>,
      val temperatureSensorCh5: Measurement<Double>,
      val windSensor: Measurement<Double>,
    )

    @Serializable
    data class AirQualityMeasurements(
      @JsonNames("24_hours_average") val average: Measurement<Long>,
      val co2: Measurement<Long>,
    )

    @Serializable
    data class AirQuality10Measurements(
      @JsonNames("24_hours_aqi") val average: Measurement<Long>,
      val pm10: Measurement<Long>,
      val realTimeAqi: Measurement<Long>,
    )

    @Serializable
    data class AirQuality25Measurements(
      @JsonNames("24_hours_aqi") val average: Measurement<Long>,
      val pm25: Measurement<Long>,
      val realTimeAqi: Measurement<Long>,
    )

    @Serializable
    data class IndoorMeasurements(
      val appTempin: Measurement<Double>,
      val dewPoint: Measurement<Double>,
      val feelsLike: Measurement<Double>,
      val humidity: Measurement<Int>,
      val temperature: Measurement<Double>,
    )

    @Serializable data class LightningMeasurements(val count: Measurement<Long>)

    @Serializable
    data class OutdoorMeasurements(
      val appTemp: Measurement<Double>,
      val dewPoint: Measurement<Double>,
      val feelsLike: Measurement<Double>,
      val humidity: Measurement<Int>,
      val temperature: Measurement<Double>,
    )

    @Serializable data class PressureMeasurements(val absolute: Measurement<Double>, val relative: Measurement<Double>)

    @Serializable
    data class RainfallMeasurements(
      @JsonNames("1_hour") val pastHour: Measurement<Double>,
      val daily: Measurement<Double>,
      val event: Measurement<Double>,
      val monthly: Measurement<Double>,
      val rainRate: Measurement<Double>,
      val weekly: Measurement<Double>,
      val yearly: Measurement<Double>,
    )

    @Serializable data class SoilMeasurements(val soilmoisture: Measurement<Int>)

    @Serializable data class SolarUVIndexMeasurements(val solar: Measurement<Double>, val uvi: Measurement<Int>)

    @Serializable
    data class TemperatureHumidityComboMeasurements(
      val humidity: Measurement<Int>,
      val temperature: Measurement<Double>,
    )

    @Serializable data class TemperatureMeasurements(val temperature: Measurement<Double>)

    @Serializable data class WaterLeakMeasurements(val leakCh4: Measurement<Int>)

    @Serializable
    data class WindMeasurements(
      val windDirection: Measurement<Int>,
      val windGust: Measurement<Double>,
      val windSpeed: Measurement<Double>,
    )
  }
}
