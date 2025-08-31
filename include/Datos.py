from dataclasses import dataclass
from PhysicalLayer import to_bits, text_to_bits

# TODO: Escribir docstrings de las clases.

@dataclass
class Message:
    app_id: int
    payload: str
    def bits(self) -> str:
        return to_bits(self.app_id, 3) + text_to_bits(self.payload)

    def __str__(self) -> str:
        return f"{self.app_id} _ {self.payload}"



@dataclass
class Segment:
    proto: str            # "TCP" o "UDP"
    src_port: int         # 16 bits
    dst_port: int         # 16 bits
    message: Message      # datos de aplicación

    def bits(self) -> str:
        return (
            text_to_bits(self.proto) +
            to_bits(self.src_port, 16) +
            to_bits(self.dst_port, 16) +
            self.message.bits()
        )
    def __str__(self) -> str:
        return f" {self.dst_port} _ {self.message}"

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
    def __str__(self) -> str:
        return f"{self.src_ip} _ {self.dst_ip} _ {self.segment}"

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
    def __str__(self) -> str:
        return f"{self.src_mac} _ {self.dst_mac} _ {self.eth_type} _ {self.packet}"
