package codefloe.buriedincode.weatherdan.controllers

import codefloe.buriedincode.weatherdan.Utils.ECOWITT
import codefloe.buriedincode.weatherdan.Utils.settings
import codefloe.buriedincode.weatherdan.Utils.toHumanReadable
import codefloe.buriedincode.weatherdan.Utils.transaction
import codefloe.buriedincode.weatherdan.database.Rainfall
import io.javalin.http.Context
import kotlin.time.ExperimentalTime
import kotlinx.datetime.TimeZone
import kotlinx.datetime.toLocalDateTime

object RainfallController : WeatherController<Rainfall>(id = "rainfall") {
  @OptIn(ExperimentalTime::class)
  override fun getGraphData(): Pair<List<String>, List<Double>> = transaction {
    val data =
      Rainfall.all()
        .sorted()
        .groupBy { it.timestamp.toLocalDateTime(TimeZone.currentSystemDefault()).date }
        .mapValues { (_, list) -> list.sumOf { it.amount } }
    data.keys.map { it.toHumanReadable() } to data.keys.map { data[it] ?: 0.0 }
  }

  @OptIn(ExperimentalTime::class)
  override fun refreshData(ctx: Context): Unit = transaction {
    ECOWITT.listDevices().forEach { device ->
      val live = ECOWITT.getLiveRainfall(macAddress = device.macAddress, rainfallUnit = settings.units.rainfall)
      transaction {
        Rainfall.findOrNull(live.rainfall.daily.timestamp)
          ?: Rainfall.new {
            this.timestamp = live.rainfall.daily.timestamp
            this.amount = live.rainfall.daily.value
          }
      }
    }
  }
}
