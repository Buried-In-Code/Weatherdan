package codefloe.buriedincode.ecowitt.serializers

import codefloe.buriedincode.ecowitt.schemas.BaseDevice.DeviceType
import kotlinx.serialization.KSerializer
import kotlinx.serialization.descriptors.PrimitiveKind
import kotlinx.serialization.descriptors.PrimitiveSerialDescriptor
import kotlinx.serialization.descriptors.SerialDescriptor
import kotlinx.serialization.encoding.Decoder
import kotlinx.serialization.encoding.Encoder

object DeviceTypeSerializer : KSerializer<DeviceType> {
  override val descriptor: SerialDescriptor = PrimitiveSerialDescriptor("DeviceType", PrimitiveKind.INT)

  override fun deserialize(decoder: Decoder): DeviceType {
    return DeviceType.fromInt(value = decoder.decodeInt())
  }

  override fun serialize(encoder: Encoder, value: DeviceType) {
    encoder.encodeInt(value = value.value)
  }
}
