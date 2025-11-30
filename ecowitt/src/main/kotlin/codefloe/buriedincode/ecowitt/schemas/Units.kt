package codefloe.buriedincode.ecowitt.schemas

enum class TempUnit(val display: String, val value: String) {
  C(display = "℃", value = "1"),
  F(display = "℉", value = "2"),
}

enum class PressureUnit(val display: String, val value: String) {
  HPA(display = "hPa", value = "3"),
  INHG(display = "inHg", value = "4"),
  MMHG(display = "mmHg", value = "5"),
}

enum class WindSpeedUnit(val display: String, val value: String) {
  MS(display = "m/s", value = "6"),
  KMH(display = "km/h", value = "7"),
  KNOTS(display = "knots", value = "8"),
  MPH(display = "mph", value = "9"),
  BFT(display = "BFT", value = "10"),
  FPM(display = "fpm", value = "11"),
}

enum class RainfallUnit(val display: String, val value: String) {
  MM(display = "mm", value = "12"),
  IN(display = "in", value = "13"),
}

enum class SolarIrradianceUnit(val display: String, val value: String) {
  LX(display = "lx", value = "14"),
  FC(display = "fc", value = "15"),
  WM2(display = "W/m²", value = "16"),
}

enum class CapacityUnit(val display: String, val value: String) {
  L(display = "L", value = "24"),
  M3(display = "m³", value = "25"),
  GAL(display = "gal", value = "26"),
}
