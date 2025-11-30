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
class Solar(id: EntityID<Long>) : LongEntity(id), Comparable<Solar> {
  companion object : LongEntityClass<Solar>(SolarTable) {
    val comparator = compareBy(Solar::timestamp)

    fun findOrNull(timestamp: Instant): Solar? {
      return find { SolarTable.timestampCol eq timestamp }.firstOrNull()
    }
  }

  var timestamp: Instant by SolarTable.timestampCol
  var amount: Double by SolarTable.amountCol

  override fun compareTo(other: Solar): Int = comparator.compare(this, other)
}

@OptIn(ExperimentalTime::class)
object SolarTable : LongIdTable(name = "solar") {
  val timestampCol: Column<Instant> = timestamp(name = "timestamp").uniqueIndex()
  val amountCol: Column<Double> = double(name = "amount")

  init {
    transaction { SchemaUtils.create(this) }
  }
}
