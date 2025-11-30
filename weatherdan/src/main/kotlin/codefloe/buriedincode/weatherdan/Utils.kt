package codefloe.buriedincode.weatherdan

import codefloe.buriedincode.ecowitt.Ecowitt
import codefloe.buriedincode.ecowitt.SQLiteCache
import io.github.oshai.kotlinlogging.KLogger
import io.github.oshai.kotlinlogging.KotlinLogging
import io.github.oshai.kotlinlogging.Level
import java.nio.file.Path
import java.nio.file.Paths
import java.sql.Connection
import java.time.format.DateTimeFormatter
import java.time.temporal.TemporalAccessor
import java.util.Locale
import kotlin.io.path.createDirectories
import kotlin.io.path.div
import kotlin.io.path.exists
import kotlin.time.Duration
import kotlin.time.Duration.Companion.hours
import kotlin.time.DurationUnit
import kotlin.time.measureTimedValue
import kotlin.time.toDuration
import kotlinx.datetime.LocalDate
import kotlinx.datetime.toJavaLocalDate
import org.jetbrains.exposed.v1.core.DatabaseConfig
import org.jetbrains.exposed.v1.core.ExperimentalKeywordApi
import org.jetbrains.exposed.v1.core.Slf4jSqlDebugLogger
import org.jetbrains.exposed.v1.jdbc.Database
import org.jetbrains.exposed.v1.jdbc.transactions.transaction

internal const val VERSION = "0.8.0"
internal const val PROJECT_NAME = "Weatherdan"

object Utils {
  @JvmStatic private val LOGGER = KotlinLogging.logger {}

  private val USER_HOME: Path by lazy { Paths.get(System.getProperty("user.home")) }
  private val XDG_CACHE_HOME: Path by lazy {
    System.getenv("XDG_CACHE_HOME")?.let { Paths.get(it) } ?: (this.USER_HOME / ".cache")
  }
  private val XDG_CONFIG_HOME: Path by lazy {
    System.getenv("XDG_CONFIG_HOME")?.let { Paths.get(it) } ?: (this.USER_HOME / ".config")
  }
  private val XDG_DATA_HOME: Path by lazy {
    System.getenv("XDG_DATA_HOME")?.let { Paths.get(it) } ?: (this.USER_HOME / ".local" / "share")
  }

  internal val CACHE_ROOT by lazy { this.XDG_CACHE_HOME / PROJECT_NAME.lowercase() }
  internal val CONFIG_ROOT by lazy { this.XDG_CONFIG_HOME / PROJECT_NAME.lowercase() }
  internal val DATA_ROOT by lazy { this.XDG_DATA_HOME / PROJECT_NAME.lowercase() }

  private val DATABASE: Database by lazy {
    Database.connect(
      url = "jdbc:sqlite:${this.DATA_ROOT / "${PROJECT_NAME.lowercase()}.sqlite"}",
      driver = "org.sqlite.JDBC",
      databaseConfig =
        DatabaseConfig {
          @OptIn(ExperimentalKeywordApi::class)
          preserveKeywordCasing = true
        },
    )
  }

  internal val settings: Settings by lazy { Settings.load() }

  internal val ECOWITT: Ecowitt by lazy {
    Ecowitt(
      applicationKey = settings.ecowitt.applicationKey,
      apiKey = settings.ecowitt.apiKey,
      cache = SQLiteCache(path = this.CACHE_ROOT / "ecowitt.sqlite", expiry = 3.hours),
    )
  }

  init {
    settings.ssl?.let {
      System.setProperty("javax.net.ssl.trustStore", it.trustStore)
      System.setProperty("javax.net.ssl.trustStorePassword", it.password)
    }
    listOf(this.CACHE_ROOT, this.CONFIG_ROOT, this.DATA_ROOT).forEach { if (!it.exists()) it.createDirectories() }
  }

  private fun getDaySuffix(day: Int): String {
    return when (day) {
      1,
      21,
      31 -> "st"
      2,
      22,
      32 -> "nd"
      3,
      23 -> "rd"
      else -> "th"
    }
  }

  private fun TemporalAccessor.formatToPattern(pattern: String): String {
    return DateTimeFormatter.ofPattern(pattern, Locale.ENGLISH).format(this)
  }

  internal fun KLogger.log(level: Level, message: () -> Any?) {
    when (level) {
      Level.TRACE -> this.trace(message)
      Level.DEBUG -> this.debug(message)
      Level.INFO -> this.info(message)
      Level.WARN -> this.warn(message)
      Level.ERROR -> this.error(message)
      else -> return
    }
  }

  internal fun Duration.toHumanReadable(): String = this.toString()

  internal fun Long.toHumanReadable(): String = this.toDuration(DurationUnit.MILLISECONDS).toHumanReadable()

  internal fun Float.toHumanReadable(): String = this.toLong().toHumanReadable()

  internal fun LocalDate.toHumanReadable(): String {
    return this.toJavaLocalDate().formatToPattern("d'${getDaySuffix(this.day)}' MMM yyyy")
  }

  internal fun <T> transaction(block: () -> T): T {
    val result = measureTimedValue {
      transaction(transactionIsolation = Connection.TRANSACTION_SERIALIZABLE, db = this.DATABASE) {
        addLogger(Slf4jSqlDebugLogger)
        block()
      }
    }
    LOGGER.debug { "Took ${result.duration.toHumanReadable()}" }
    return result.value
  }
}
