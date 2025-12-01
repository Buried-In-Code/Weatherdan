package codefloe.buriedincode.weatherdan.controllers

import codefloe.buriedincode.weatherdan.GraphUnit
import codefloe.buriedincode.weatherdan.Utils.ECOWITT
import codefloe.buriedincode.weatherdan.Utils.settings
import codefloe.buriedincode.weatherdan.Utils.transaction
import codefloe.buriedincode.weatherdan.database.Rainfall
import codefloe.buriedincode.weatherdan.database.Solar
import codefloe.buriedincode.weatherdan.database.UVIndex
import codefloe.buriedincode.weatherdan.database.Wind
import io.javalin.http.Context
import kotlin.time.Duration.Companion.hours
import kotlin.time.ExperimentalTime
import kotlin.time.Instant

object WeatherController {
  @OptIn(ExperimentalTime::class)
  private fun loadLiveReadings() {
    ECOWITT.listDevices().forEach { device ->
      val live =
        ECOWITT.getLiveReadings(
          macAddress = device.macAddress,
          tempUnit = settings.units.temp,
          pressureUnit = settings.units.pressure,
          windSpeedUnit = settings.units.windSpeed,
          rainfallUnit = settings.units.rainfall,
          solarIrradianceUnit = settings.units.solarIrradiance,
          capacityUnit = settings.units.capacity,
        )
      transaction {
        Rainfall.findOrCreate(measurement = live.rainfall.daily)
        Solar.findOrCreate(measurement = live.solarAndUvi.solar)
        UVIndex.findOrCreate(measurement = live.solarAndUvi.uvi)
        Wind.findOrCreate(measurement = live.wind.windSpeed)
      }
    }
  }

  @OptIn(ExperimentalTime::class)
  private fun getLastReadingDate(): Instant {
    return transaction {
      listOfNotNull(
          Rainfall.all().maxByOrNull { it.timestamp }?.timestamp,
          Solar.all().maxByOrNull { it.timestamp }?.timestamp,
          UVIndex.all().maxByOrNull { it.timestamp }?.timestamp,
          Wind.all().maxByOrNull { it.timestamp }?.timestamp,
        )
        .minOrNull()
    } ?: Instant.parse("2020-01-01T00:00:00Z")
  }

  @OptIn(ExperimentalTime::class)
  private fun loadHistoricalReadings() {
    ECOWITT.listDevices().forEach { device ->
      val readings =
        ECOWITT.getHistoryReadings(
          macAddress = device.macAddress,
          start = getLastReadingDate().minus(1.hours),
          tempUnit = settings.units.temp,
          pressureUnit = settings.units.pressure,
          windSpeedUnit = settings.units.windSpeed,
          rainfallUnit = settings.units.rainfall,
          solarIrradianceUnit = settings.units.solarIrradiance,
          capacityUnit = settings.units.capacity,
        )
      transaction {
        readings.forEach { history ->
          history.rainfall?.daily?.values?.forEach { (timestamp, amount) ->
            Rainfall.findOrCreate(timestamp = timestamp, amount = amount)
          }
          history.solarAndUvi?.solar?.values?.forEach { (timestamp, amount) ->
            Solar.findOrCreate(timestamp = timestamp, amount = amount)
          }
          history.solarAndUvi?.uvi?.values?.forEach { (timestamp, amount) ->
            UVIndex.findOrCreate(timestamp = timestamp, amount = amount)
          }
          history.wind?.windSpeed?.values?.forEach { (timestamp, amount) ->
            Wind.findOrCreate(timestamp = timestamp, amount = amount)
          }
        }
      }
    }
  }

  private fun buildGraphData(
    rainfall: Pair<List<String>, List<Double>>,
    solar: Pair<List<String>, List<Double>>,
    uvIndex: Pair<List<String>, List<Int>>,
    wind: Pair<List<String>, List<Double>>,
    limit: Int? = null,
  ): List<GraphUnit> {
    fun <T> List<T>.applyLimit() = limit?.let { takeLast(it) } ?: this
    return listOf(
      GraphUnit(id = "rainfall", labels = rainfall.first.applyLimit(), datasets = listOf(rainfall.second.applyLimit())),
      GraphUnit(id = "solar", labels = solar.first.applyLimit(), datasets = listOf(solar.second.applyLimit())),
      GraphUnit(id = "uv-index", labels = uvIndex.first.applyLimit(), datasets = listOf(uvIndex.second.applyLimit())),
      GraphUnit(id = "wind", labels = wind.first.applyLimit(), datasets = listOf(wind.second.applyLimit())),
    )
  }

  fun loadGraphScripts(ctx: Context) {
    loadHistoricalReadings()
    //    loadLiveReadings()
    val graphData = transaction {
      buildGraphData(
        rainfall = Rainfall.getGraphData(),
        solar = Solar.getGraphData(),
        uvIndex = UVIndex.getGraphData(),
        wind = Wind.getGraphData(),
      )
    }
    ctx.render("components/graph/script.kte", mapOf("graphs" to graphData))
  }

  fun loadDailyGraphScripts(ctx: Context) {
    loadHistoricalReadings()
    //    loadLiveReadings()
    val graphData = transaction {
      buildGraphData(
        rainfall = Rainfall.getGraphData(),
        solar = Solar.getGraphData(),
        uvIndex = UVIndex.getGraphData(),
        wind = Wind.getGraphData(),
        limit = 14,
      )
    }
    ctx.render("components/graph/script.kte", mapOf("graphs" to graphData))
  }
}
