package codefloe.buriedincode.ecowitt.schemas

import kotlin.time.ExperimentalTime
import kotlin.time.Instant
import kotlinx.serialization.ExperimentalSerializationApi
import kotlinx.serialization.Serializable
import kotlinx.serialization.json.JsonNames

@OptIn(ExperimentalSerializationApi::class)
@Serializable
data class PagedResponse<T>(
  @JsonNames("list") val results: List<T>,
  @JsonNames("pageNum") val pageNumber: Long,
  val total: Long,
  @JsonNames("totalPage") val totalPage: Long,
)

@OptIn(ExperimentalTime::class)
@Serializable
data class Measurement<T>(private val time: Long, val unit: String, val value: T) {
  val timestamp: Instant
    get() = Instant.fromEpochSeconds(time)
}
