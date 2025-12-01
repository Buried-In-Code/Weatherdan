package codefloe.buriedincode.weatherdan.database

import codefloe.buriedincode.weatherdan.Utils.toHumanReadable
import codefloe.buriedincode.weatherdan.Utils.transaction
import kotlin.time.ExperimentalTime
import kotlin.time.Instant
import kotlinx.datetime.TimeZone
import kotlinx.datetime.toLocalDateTime
import org.jetbrains.exposed.v1.core.Column
import org.jetbrains.exposed.v1.core.dao.id.EntityID
import org.jetbrains.exposed.v1.core.dao.id.LongIdTable
import org.jetbrains.exposed.v1.core.eq
import org.jetbrains.exposed.v1.dao.LongEntity
import org.jetbrains.exposed.v1.dao.LongEntityClass
import org.jetbrains.exposed.v1.datetime.timestamp
import org.jetbrains.exposed.v1.jdbc.SchemaUtils

@OptIn(ExperimentalTime::class)
class UVIndex(id: EntityID<Long>) : LongEntity(id), Comparable<UVIndex> {
  companion object : LongEntityClass<UVIndex>(UVIndexTable), Weather<UVIndex, Int> {
    val comparator = compareBy(UVIndex::timestamp)

    override fun findOrNull(timestamp: Instant): UVIndex? {
      return find { UVIndexTable.timestampCol eq timestamp }.firstOrNull()
    }

    override fun findOrCreate(timestamp: Instant, amount: Int): UVIndex {
      return findOrNull(timestamp = timestamp)
        ?: new {
          this.timestamp = timestamp
          this.amount = amount
        }
    }

    override fun getGraphData(): Pair<List<String>, List<Int>> {
      val data =
        all()
          .sorted()
          .groupBy { it.timestamp.toLocalDateTime(TimeZone.currentSystemDefault()).date }
          .mapValues { (_, list) -> list.maxOf { it.amount } }
      return data.keys.map { it.toHumanReadable() } to data.values.toList()
    }
  }

  var timestamp: Instant by UVIndexTable.timestampCol
  var amount: Int by UVIndexTable.amountCol

  override fun compareTo(other: UVIndex): Int = comparator.compare(this, other)
}

@OptIn(ExperimentalTime::class)
object UVIndexTable : LongIdTable(name = "uv_index") {
  val timestampCol: Column<Instant> = timestamp(name = "timestamp").uniqueIndex()
  val amountCol: Column<Int> = integer(name = "amount")

  init {
    transaction { SchemaUtils.create(this) }
  }
}
