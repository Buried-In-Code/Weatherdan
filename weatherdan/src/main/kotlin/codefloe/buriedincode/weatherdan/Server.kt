package codefloe.buriedincode.weatherdan

import codefloe.buriedincode.weatherdan.Utils.log
import codefloe.buriedincode.weatherdan.Utils.settings
import codefloe.buriedincode.weatherdan.Utils.toHumanReadable
import codefloe.buriedincode.weatherdan.controllers.WeatherController
import gg.jte.ContentType as JteType
import gg.jte.TemplateEngine
import gg.jte.resolve.DirectoryCodeResolver
import io.github.oshai.kotlinlogging.KotlinLogging
import io.github.oshai.kotlinlogging.Level
import io.javalin.Javalin
import io.javalin.apibuilder.ApiBuilder.get
import io.javalin.apibuilder.ApiBuilder.path
import io.javalin.http.ContentType
import io.javalin.rendering.FileRenderer
import io.javalin.rendering.template.JavalinJte
import java.nio.file.Path
import kotlin.collections.mapOf
import kotlin.io.path.div
import kotlin.time.ExperimentalTime

object Server {
  @JvmStatic private val LOGGER = KotlinLogging.logger {}

  private fun createTemplateEngine(environment: Settings.Environment): TemplateEngine {
    return if (environment == Settings.Environment.DEV) {
      val codeResolver = DirectoryCodeResolver(Path.of("src") / "main" / "jte")
      TemplateEngine.create(codeResolver, JteType.Html)
    } else {
      TemplateEngine.createPrecompiled(Path.of("jte-classes"), JteType.Html)
    }
  }

  @OptIn(ExperimentalTime::class)
  private fun createJavalinApp(renderer: FileRenderer): Javalin {
    return Javalin.create {
      it.fileRenderer(fileRenderer = renderer)
      it.http.prefer405over404 = true
      it.http.defaultContentType = ContentType.JSON
      it.requestLogger.http { ctx, ms ->
        val level =
          when {
            ctx.statusCode() in (100..<200) -> Level.WARN
            ctx.statusCode() in (200..<300) -> Level.INFO
            ctx.statusCode() in (300..<400) -> Level.INFO
            ctx.statusCode() in (400..<500) -> Level.WARN
            else -> Level.ERROR
          }
        LOGGER.log(level) { "${ctx.statusCode()}: ${ctx.method()} - ${ctx.path()} => ${ms.toHumanReadable()}" }
      }
      it.router.caseInsensitiveRoutes = true
      it.router.ignoreTrailingSlashes = true
      it.router.treatMultipleSlashesAsSingleSlash = true
      it.router.apiBuilder {
        path("/") {
          get { ctx ->
            ctx.render(
              "templates/index.kte",
              mapOf(
                "graphs" to
                  listOf(
                    GraphUnit(id = "rainfall", label = "Rainfall", unit = settings.units.rainfall.display),
                    GraphUnit(id = "solar", label = "Solar Irradiance", unit = settings.units.solarIrradiance.display),
                    GraphUnit(id = "uv-index", label = "UV Index", unit = ""),
                    GraphUnit(id = "wind", label = "Wind Speed", unit = settings.units.windSpeed.display),
                  )
              ),
            )
          }
        }
        path("graph") {
          get("daily", WeatherController::loadDailyGraphScripts)
          get("script", WeatherController::loadGraphScripts)
        }
      }
      it.staticFiles.add {
        it.hostedPath = "/static"
        it.directory = "/static"
      }
    }
  }

  fun start(settings: Settings) {
    val engine = createTemplateEngine(environment = settings.environment)
    engine.setTrimControlStructures(true)
    val renderer = JavalinJte(templateEngine = engine)

    val app = createJavalinApp(renderer = renderer)
    app.start(settings.website.host, settings.website.port)
  }
}

fun main(@Suppress("UNUSED_PARAMETER") vararg args: String) {
  println("$PROJECT_NAME v$VERSION")
  println("Kotlin v${KotlinVersion.CURRENT}; Java v${System.getProperty("java.version")}")
  println("${System.getProperty("os.name")} ${System.getProperty("os.arch")}")

  println(settings)
  Server.start(settings = settings)
}
