package codefloe.buriedincode.ecowitt

import java.nio.file.Path
import java.sql.DriverManager
import java.sql.Timestamp
import kotlin.time.Clock
import kotlin.time.Duration
import kotlin.time.ExperimentalTime
import kotlin.time.toJavaInstant

data class SQLiteCache(val path: Path, val expiry: Duration? = null) {
  private val databaseUrl: String = "jdbc:sqlite:$path"

  init {
    this.createTable()
    this.cleanup()
  }

  private fun createTable() {
    val query = "CREATE TABLE IF NOT EXISTS queries (url TEXT, response TEXT, timestamp TIMESTAMP);"
    DriverManager.getConnection(this.databaseUrl).use { it.createStatement().use { it.execute(query) } }
  }

  @OptIn(ExperimentalTime::class)
  fun select(url: String): String? {
    val query =
      if (this.expiry == null) {
        "SELECT * FROM queries WHERE url = ?;"
      } else {
        "SELECT * FROM queries WHERE url = ? and timestamp > ?;"
      }
    DriverManager.getConnection(this.databaseUrl).use {
      it.prepareStatement(query).use {
        it.setString(1, url)
        if (this.expiry != null) {
          val expiry = Clock.System.now().minus(this.expiry)
          it.setTimestamp(2, Timestamp.from(expiry.toJavaInstant()))
        }
        it.executeQuery().use {
          return it.getString("response")
        }
      }
    }
  }

  @OptIn(ExperimentalTime::class)
  fun insert(url: String, response: String) {
    if (this.select(url = url) != null) {
      return
    }
    val query = "INSERT INTO queries (url, response, timestamp) VALUES (?, ?, ?);"
    DriverManager.getConnection(this.databaseUrl).use {
      it.prepareStatement(query).use {
        it.setString(1, url)
        it.setString(2, response)
        it.setTimestamp(3, Timestamp.from(Clock.System.now().toJavaInstant()))
        it.executeUpdate()
      }
    }
  }

  fun delete(url: String) {
    val query = "DELETE FROM queries WHERE url = ?;"
    DriverManager.getConnection(this.databaseUrl).use {
      it.prepareStatement(query).use {
        it.setString(1, url)
        it.executeUpdate()
      }
    }
  }

  @OptIn(ExperimentalTime::class)
  fun cleanup() {
    if (this.expiry == null) {
      return
    }
    val query = "DELETE FROM queries WHERE timestamp < ?;"
    DriverManager.getConnection(this.databaseUrl).use {
      it.prepareStatement(query).use {
        val expiry = Clock.System.now().minus(this.expiry)
        it.setTimestamp(1, Timestamp.from(expiry.toJavaInstant()))
        it.executeUpdate()
      }
    }
  }
}
