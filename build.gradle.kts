import com.diffplug.spotless.kotlin.KtfmtStep.TrailingCommaManagementStrategy
import com.github.benmanes.gradle.versions.updates.DependencyUpdatesTask
import com.github.benmanes.gradle.versions.updates.resolutionstrategy.ComponentSelectionWithCurrent

plugins {
  alias(libs.plugins.kotlin.jvm)
  alias(libs.plugins.kotlinx.serialization) apply false
  alias(libs.plugins.jte) apply false
  alias(libs.plugins.shadow) apply false
  alias(libs.plugins.spotless)
  alias(libs.plugins.versions)
  id("com.github.node-gradle.node") version "7.1.0" apply false
}

allprojects {
  group = "codefloe.buriedincode"
  version = "0.8.0"

  repositories {
    mavenLocal()
    mavenCentral()
  }

  apply(plugin = rootProject.libs.plugins.spotless.get().pluginId)
  spotless {
    kotlin {
      ktfmt().googleStyle().configure {
        it.setMaxWidth(120)
        it.setBlockIndent(2)
        it.setContinuationIndent(2)
        it.setRemoveUnusedImports(true)
        it.setTrailingCommaManagementStrategy(TrailingCommaManagementStrategy.COMPLETE)
      }
    }
    kotlinGradle {
      ktfmt().googleStyle().configure {
        it.setMaxWidth(120)
        it.setBlockIndent(2)
        it.setContinuationIndent(2)
        it.setRemoveUnusedImports(true)
        it.setTrailingCommaManagementStrategy(TrailingCommaManagementStrategy.COMPLETE)
      }
    }
  }
}

subprojects {
  apply(plugin = rootProject.libs.plugins.kotlin.jvm.get().pluginId)

  dependencies {
    implementation(rootProject.libs.kotlin.logging)
    implementation(rootProject.libs.kotlinx.datetime)

    runtimeOnly(rootProject.libs.bundles.log4j2)
    runtimeOnly(rootProject.libs.sqlite.jdbc)
  }

  kotlin { jvmToolchain(17) }

  java { toolchain { languageVersion = JavaLanguageVersion.of(17) } }
}

fun isNonStable(version: String): Boolean {
  val stableKeyword = listOf("RELEASE", "FINAL", "GA").any { version.uppercase().contains(it) }
  val regex = "^[0-9,.v-]+(-r)?$".toRegex()
  val isStable = stableKeyword || regex.matches(version)
  return isStable.not()
}

tasks.withType<DependencyUpdatesTask> {
  gradleReleaseChannel = "current"
  checkForGradleUpdate = true
  checkConstraints = false
  checkBuildEnvironmentConstraints = false
  resolutionStrategy {
    componentSelection {
      all(
        Action<ComponentSelectionWithCurrent> {
          if (isNonStable(candidate.version) && !isNonStable(currentVersion)) {
            reject("Release candidate")
          }
        }
      )
    }
  }
}
