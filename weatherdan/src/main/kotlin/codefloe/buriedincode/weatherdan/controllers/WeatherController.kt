package codefloe.buriedincode.weatherdan.controllers

import io.javalin.http.Context

abstract class WeatherController<T>(val id: String) {
  abstract fun getGraphData(): Pair<List<String>, List<Double>>

  abstract fun refreshData(ctx: Context)

  fun generateGraphScript(ctx: Context) {
    val (labels, dataset) = getGraphData()
    ctx.render("components/graph-script.kte", mapOf("id" to this.id, "labels" to labels, "dataset" to dataset))
  }
}
