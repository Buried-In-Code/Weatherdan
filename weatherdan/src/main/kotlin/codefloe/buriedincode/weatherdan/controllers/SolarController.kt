package codefloe.buriedincode.weatherdan.controllers

import codefloe.buriedincode.weatherdan.Utils.ECOWITT
import codefloe.buriedincode.weatherdan.Utils.settings
import codefloe.buriedincode.weatherdan.Utils.toHumanReadable
import codefloe.buriedincode.weatherdan.Utils.transaction
import codefloe.buriedincode.weatherdan.database.Solar
import io.javalin.http.Context
import kotlin.time.ExperimentalTime
import kotlinx.datetime.TimeZone
import kotlinx.datetime.toLocalDateTime

object SolarController : WeatherController<Solar>(id = "solar") {
  @OptIn(ExperimentalTime::class)
  override fun getGraphData(): Pair<List<String>, List<Double>> = transaction {
    val data =
      Solar.all()
        .sorted()
        .groupBy { it.timestamp.toLocalDateTime(TimeZone.currentSystemDefault()).date }
        .mapValues { (_, list) -> list.sumOf { it.amount } }
    data.keys.map { it.toHumanReadable() } to data.keys.map { data[it] ?: 0.0 }
  }

  @OptIn(ExperimentalTime::class)
  override fun refreshData(ctx: Context): Unit = transaction {
    ECOWITT.listDevices().forEach { device ->
      val live =
        ECOWITT.getLiveSolar(macAddress = device.macAddress, solarIrradianceUnit = settings.units.solarIrradiance)
      transaction {
        Solar.findOrNull(live.solarAndUvi.solar.timestamp)
          ?: Solar.new {
            this.timestamp = live.solarAndUvi.solar.timestamp
            this.amount = live.solarAndUvi.solar.value
          }
      }
    }
  }
}
