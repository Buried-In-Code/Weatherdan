package codefloe.buriedincode.weatherdan.database

import codefloe.buriedincode.weatherdan.Utils.transaction
import kotlin.time.ExperimentalTime
import kotlin.time.Instant
import org.jetbrains.exposed.v1.core.Column
import org.jetbrains.exposed.v1.core.dao.id.EntityID
import org.jetbrains.exposed.v1.core.dao.id.LongIdTable
import org.jetbrains.exposed.v1.core.eq
import org.jetbrains.exposed.v1.dao.LongEntity
import org.jetbrains.exposed.v1.dao.LongEntityClass
import org.jetbrains.exposed.v1.datetime.timestamp
import org.jetbrains.exposed.v1.jdbc.SchemaUtils

@OptIn(ExperimentalTime::class)
class Rainfall(id: EntityID<Long>) : LongEntity(id), Comparable<Rainfall> {
  companion object : LongEntityClass<Rainfall>(RainfallTable) {
    val comparator = compareBy(Rainfall::timestamp)

    fun findOrNull(timestamp: Instant): Rainfall? {
      return find { RainfallTable.timestampCol eq timestamp }.firstOrNull()
    }
  }

  var timestamp: Instant by RainfallTable.timestampCol
  var amount: Double by RainfallTable.amountCol

  override fun compareTo(other: Rainfall): Int = comparator.compare(this, other)
}

@OptIn(ExperimentalTime::class)
object RainfallTable : LongIdTable(name = "rainfall") {
  val timestampCol: Column<Instant> = timestamp(name = "timestamp").uniqueIndex()
  val amountCol: Column<Double> = double(name = "amount")

  init {
    transaction { SchemaUtils.create(this) }
  }
}
