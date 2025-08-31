from dataclasses import dataclass
from PhysicalLayer import to_bits, text_to_bits


@dataclass
class Message:
    """ Representa la instancia de un mensaje con el identificador de
    aplicación.

    Atributos
    ---------
    app_id : int
        Identificador de aplicación que envía mensaje.
    payload : str
        Mensaje a enviar
    """
    app_id: int
    payload: str

    def bits(self) -> str:
        """ Obtener string de bits que representa el identificador y mensaje.

        :return: Secuencia de bits
        :rtype: str
        """
        return to_bits(self.app_id, 3) + text_to_bits(self.payload)

    def __str__(self) -> str:
        """ String mostrando información de identificador y mensaje.

        :return: String resultante
        :rtype: str
        """
        return f"{self.app_id} _ {self.payload}"


@dataclass
class Segment:
    """ Representa la instancia de un segmento.

    Atributos
    ---------
    proto : str
        Protocolo usado para la comunicación.
            Protocolo usado para la comunicación ("TCP" o "UDP").
    src_port : int
        Puerto de origen (16 bits).
    dst_port : int
        Puerto de destino (16 bits).
    message : Message
        Datos de aplicación contenidos en el segmento.
    """
    proto: str            # "TCP" o "UDP"
    src_port: int         # 16 bits
    dst_port: int         # 16 bits
    message: Message      # datos de aplicación

    def bits(self) -> str:
        """ Devuelve la representación en bits del segmento, incluyendo el
        protocolo, puertos y mensaje.

        :return: Secuencia de bits
        :rtype: str
        """
        return (
            text_to_bits(self.proto) +
            to_bits(self.src_port, 16) +
            to_bits(self.dst_port, 16) +
            self.message.bits()
        )

    def __str__(self) -> str:
        """ Devuelve una representación legible del segmento, mostrando el
        puerto de destino y el mensaje.

        :return: String resultante
        :rtype: str
        """
        return f" {self.dst_port} _ {self.message}"


@dataclass
class Packet:
    """ Representa un paquete

    Atributos
    ---------
    src_ip : int
        IP de origen (8 bits).
    dst_ip : int
        IP de destino (8 bits).
    segment : Segment
        Instancia de un segmento
    """
    src_ip: int           # 8 bits (simplificado)
    dst_ip: int           # 8 bits (simplificado)
    segment: Segment

    def bits(self) -> str:
        """ Devuelve la representación en bits del paquete, incluyendo IP de
        origen y destino, y el segmento.

        :return: Secuencia de bits
        :rtype: str
        """
        return (
            to_bits(self.src_ip, 8) +
            to_bits(self.dst_ip, 8) +
            self.segment.bits()
        )

    def __str__(self) -> str:
        """ Devuelve una representación legible del paquete, mostrando IP de
        origen y destino, y el segmento.

        :return: String resultante
        :rtype: str
        """
        return f"{self.src_ip} _ {self.dst_ip} _ {self.segment}"


@dataclass
class Frame:
    """ Representa un frame.

    Atributos
    ---------
    src_mac : int
        MAC de origen (8 bits).
    dst_mac : int
        MAC de destino (8 bits).
    packet : Packet
        Instancia de un paquete
    """
    src_mac: int          # 8 bits (simplificado)
    dst_mac: int          # 8 bits (simplificado)
    packet: Packet

    def bits(self) -> str:
        """ Devuelve la representación en bits del frame, incluyendo MAC de
        origen y destino, y el paquete.

        :return: _description_
        :rtype: str
        """
        return (
            to_bits(self.src_mac, 8) +
            to_bits(self.dst_mac, 8) +
            self.packet.bits()
        )

    def __str__(self) -> str:
        """ Devuelve una representación legible del frame, mostrando MAC de
        origen y destino, y el paquete.

        :return: String resultante
        :rtype: str
        """
        return f"{self.src_mac} _ {self.dst_mac} _ {self.packet}"
