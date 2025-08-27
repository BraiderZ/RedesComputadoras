from dataclasses import dataclass
from include.PhysicalLayer import to_bits, text_to_bits

# TODO: Escribir docstrings de las clases.


@dataclass
class Segment:
    proto: str            # "TCP" o "UDP"
    src_port: int         # 16 bits
    dst_port: int         # 16 bits
    payload: str          # datos de aplicación (texto)

    def bits(self) -> str:
        return (
            text_to_bits(self.proto) +
            to_bits(self.src_port, 16) +
            to_bits(self.dst_port, 16) +
            text_to_bits(self.payload)
        )


@dataclass
class Packet:
    src_ip: int           # 8 bits (simplificado)
    dst_ip: int           # 8 bits (simplificado)
    segment: Segment

    def bits(self) -> str:
        return (
            to_bits(self.src_ip, 8) +
            to_bits(self.dst_ip, 8) +
            self.segment.bits()
        )


@dataclass
class Frame:
    src_mac: int          # 8 bits (simplificado)
    dst_mac: int          # 8 bits (simplificado)
    eth_type: int         # 8 bits (0x01 = IPv4 simplificado)
    packet: Packet

    def bits(self) -> str:
        return (
            to_bits(self.src_mac, 8) +
            to_bits(self.dst_mac, 8) +
            to_bits(self.eth_type, 8) +
            self.packet.bits()
        )
