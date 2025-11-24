plugins {
  alias(libs.plugins.kotlinx.serialization)
  `java-library`
}

dependencies {
  implementation(libs.kotlinx.serialization)

  testImplementation(libs.junit.jupiter)

  testRuntimeOnly(libs.junit.platform.launcher)
}

tasks.test {
  environment("ECOWITT__APPLICATION_KEY", System.getenv("ECOWITT__APPLICATION_KEY"))
  environment("ECOWITT__API_KEY", System.getenv("ECOWITT__API_KEY"))

  useJUnitPlatform()
  testLogging { events("passed", "skipped", "failed") }
}
