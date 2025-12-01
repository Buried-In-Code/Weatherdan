package codefloe.buriedincode.weatherdan

data class GraphUnit(
  val id: String,
  val label: String? = null,
  val unit: String? = null,
  val labels: List<String> = emptyList(),
  val datasets: List<List<Number>> = emptyList(),
)
