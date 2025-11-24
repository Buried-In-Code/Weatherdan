plugins {
  alias(libs.plugins.jte)
  alias(libs.plugins.shadow)
  application
  id("com.github.node-gradle.node")
}

dependencies {
  implementation(project(":ecowitt"))
  implementation(libs.bundles.exposed)
  implementation(libs.bundles.jackson)
  implementation(libs.bundles.javalin)
  implementation(libs.bundles.jte)
  implementation(libs.hoplite.core)
}

application {
  mainClass = "codefloe.buriedincode.weatherdan.ServerKt"
  applicationName = "Weatherdan"
}

jte {
  precompile()
  kotlinCompileArgs = arrayOf("-jvm-target", "21")
}

tasks.clean { doLast { delete("$projectDir/jte-classes") } }

tasks.jar {
  dependsOn(tasks.precompileJte)
  from(
    fileTree("jte-classes") {
      include("**/*.class")
      include("**/*.bin")
    }
  )
  manifest.attributes["Main-Class"] = "codefloe.buriedincode.weatherdan.ServerKt"
}

tasks.shadowJar {
  dependsOn(tasks.precompileJte)
  from(
    fileTree("jte-classes") {
      include("**/*.class")
      include("**/*.bin")
    }
  )
  manifest.attributes["Main-Class"] = "codefloe.buriedincode.weatherdan.ServerKt"
  mergeServiceFiles()
}

node {
  download = false
  version = "22.19.0"
}

val npmInstall by tasks.getting(com.github.gradle.node.npm.task.NpmTask::class)
val compileSass by
  tasks.registering(com.github.gradle.node.npm.task.NpxTask::class) {
    dependsOn(npmInstall)
    command = "sass"
    args =
      listOf("src/main/resources/scss/main.scss:src/main/resources/static/css/bulma-custom.css", "--style=compressed")
    inputs.dir("src/main/resources/scss")
    outputs.file("src/main/resources/static/css/bulma-custom.css")
  }

// tasks.processResources { dependsOn(compileSass) }
