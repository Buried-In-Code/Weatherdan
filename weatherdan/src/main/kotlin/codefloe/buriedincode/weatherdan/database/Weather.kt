package codefloe.buriedincode.weatherdan.database

import codefloe.buriedincode.ecowitt.schemas.Measurement
import kotlin.time.ExperimentalTime
import kotlin.time.Instant

interface Weather<E, N : Number> {
  @OptIn(ExperimentalTime::class) fun findOrNull(timestamp: Instant): E?

  @OptIn(ExperimentalTime::class)
  fun findOrCreate(measurement: Measurement<N>): E =
    findOrCreate(timestamp = measurement.timestamp, amount = measurement.value)

  @OptIn(ExperimentalTime::class) fun findOrCreate(timestamp: Instant, amount: N): E

  fun getGraphData(): Pair<List<String>, List<N>>
}
