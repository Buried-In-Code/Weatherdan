package codefloe.buriedincode.ecowitt

import codefloe.buriedincode.ecowitt.schemas.BasicDevice
import codefloe.buriedincode.ecowitt.schemas.Device
import codefloe.buriedincode.ecowitt.schemas.PagedResponse
import io.github.oshai.kotlinlogging.KotlinLogging
import io.github.oshai.kotlinlogging.Level
import java.io.IOException
import java.net.URI
import java.net.URLEncoder
import java.net.http.HttpClient
import java.net.http.HttpConnectTimeoutException
import java.net.http.HttpRequest
import java.net.http.HttpResponse
import java.nio.charset.StandardCharsets
import kotlin.time.Duration
import kotlin.time.Duration.Companion.seconds
import kotlin.time.ExperimentalTime
import kotlin.time.toJavaDuration
import kotlinx.serialization.ExperimentalSerializationApi
import kotlinx.serialization.SerializationException
import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonNamingStrategy
import kotlinx.serialization.json.jsonObject
import kotlinx.serialization.json.jsonPrimitive
import kotlinx.serialization.json.longOrNull

class Ecowitt(
  private val applicationKey: String,
  private val apiKey: String,
  private val cache: SQLiteCache? = null,
  timeout: Duration = 30.seconds,
) {
  private val client: HttpClient =
    HttpClient.newBuilder().followRedirects(HttpClient.Redirect.ALWAYS).connectTimeout(timeout.toJavaDuration()).build()

  @OptIn(ExperimentalTime::class)
  @Throws(ServiceException::class, AuthenticationException::class)
  private fun performGetRequest(uri: URI): String {
    try {
      val request =
        HttpRequest.newBuilder()
          .uri(uri)
          .setHeader("Accept", "application/json")
          .setHeader("User-Agent", "Weatherdan/0.8.0 ($OS_AGENT; $LANGUAGE_AGENT)")
          .GET()
          .build()
      val response = this.client.send(request, HttpResponse.BodyHandlers.ofString())
      val level =
        when (response.statusCode()) {
          in 100 until 200 -> Level.WARN
          in 200 until 300 -> Level.INFO
          in 300 until 400 -> Level.WARN
          in 400 until 500 -> Level.ERROR
          else -> Level.ERROR
        }
      LOGGER.log(level) { "GET: ${response.statusCode()} - $uri" }
      if (response.statusCode() == 200) {
        val content = JSON.parseToJsonElement(response.body()).jsonObject
        LOGGER.error { content.toString() }
        val code = content["code"]?.jsonPrimitive?.longOrNull
        val message = content["msg"]?.jsonPrimitive?.content ?: content.toString()
        when (code) {
          0L -> return content["data"]?.jsonObject?.toString() ?: throw ServiceException(message)
          40010L,
          40011L,
          40017L,
          40018L -> throw AuthenticationException(message)
          else -> throw ServiceException("$code | $message")
        }
      }

      throw ServiceException(response.body())
    } catch (ioe: IOException) {
      throw ServiceException(cause = ioe)
    } catch (hcte: HttpConnectTimeoutException) {
      throw ServiceException(cause = hcte)
    } catch (ie: InterruptedException) {
      throw ServiceException(cause = ie)
    } catch (se: SerializationException) {
      throw ServiceException(cause = se)
    }
  }

  internal fun encodeURI(endpoint: String, params: Map<String, String?> = emptyMap()): URI {
    val applicationKey = params["application_key"] ?: this.applicationKey
    val apiKey = params["api_key"] ?: this.apiKey
    val _params = params + ("application_key" to applicationKey) + ("api_key" to apiKey)
    val encodedParams =
      _params.entries
        .sortedBy { it.key }
        .joinToString("&") { "${it.key}=${URLEncoder.encode(it.value, StandardCharsets.UTF_8)}" }
    return URI.create("$BASE_API$endpoint${if (encodedParams.isEmpty()) "" else "?$encodedParams"}")
  }

  @Throws(ServiceException::class, AuthenticationException::class)
  internal inline fun <reified T> getRequest(uri: URI): T {
    this.cache?.select(url = uri.toString())?.let {
      try {
        LOGGER.debug { "Using cached response for $uri" }
        return JSON.decodeFromString(it)
      } catch (se: SerializationException) {
        LOGGER.warn(se) { "Unable to deserialize cached response" }
        this.cache.delete(url = uri.toString())
      }
    }
    val response = this.performGetRequest(uri = uri)
    this.cache?.insert(url = uri.toString(), response = response)
    return try {
      JSON.decodeFromString(response)
    } catch (se: SerializationException) {
      throw ServiceException(cause = se)
    }
  }

  @Throws(ServiceException::class, AuthenticationException::class)
  internal inline fun <reified T> fetchList(endpoint: String, params: Map<String, String?> = emptyMap()): List<T> {
    val results = mutableListOf<T>()
    var page = params.getOrDefault("page", "1")?.toInt() ?: 1
    val limit = params.getOrDefault("limit", "100")?.toInt() ?: 100
    do {
      val uri =
        encodeURI(endpoint = endpoint, params = params + ("page" to page.toString()) + ("limit" to limit.toString()))
      val response = getRequest<PagedResponse<T>>(uri = uri)
      results.addAll(response.results)
      page++
    } while (page <= response.totalPage)
    return results
  }

  @Throws(ServiceException::class, AuthenticationException::class)
  internal inline fun <reified T> fetchItem(endpoint: String, params: Map<String, String?> = emptyMap()): T {
    return getRequest<T>(uri = encodeURI(endpoint = endpoint, params = params))
  }

  fun listDevices(): List<BasicDevice> = fetchList(endpoint = "/device/list")

  fun getDevice(macAddress: String): Device = fetchItem(endpoint = "/device/info", params = mapOf("mac" to macAddress))

  companion object {
    @JvmStatic private val LOGGER = KotlinLogging.logger {}
    @JvmStatic private val BASE_API = "https://api.ecowitt.net/api/v3"
    @JvmStatic
    private val LANGUAGE_AGENT = "Kotlin v${KotlinVersion.CURRENT}/Java v${System.getProperty("java.version")}"
    @JvmStatic private val OS_AGENT = "${System.getProperty("os.name")}/${System.getProperty("os.version")}"

    @OptIn(ExperimentalSerializationApi::class)
    private val JSON: Json = Json {
      prettyPrint = true
      encodeDefaults = true
      namingStrategy = JsonNamingStrategy.SnakeCase
    }
  }
}
