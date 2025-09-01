from typing import Dict, Optional, Tuple
from Datos import Frame
from Link import Link
from PhysicalLayer import show_h


class RouterL3:
    """ Clase para capa 3 de router
    """
    def __init__(self, name: str):
        """ Constructor.

        :param name: Nombre de router
        :type name: str
        """
        self.name = name
        self.ifaces: Dict[str, Tuple[int, int, Optional[Link]]] = {}
        self.route: Dict[int, str] = {}
        self.arp: Dict[int, int] = {}

    def add_iface(self, name: str, mac: int, ip: int, link: Link):
        """ Agregar una interfaz al router.

        :param name: Nombre
        :type name: str
        :param mac: MAC de interfaz
        :type mac: int
        :param ip: IP de interfaz
        :type ip: int
        :param link: Link para conexión
        :type link: Link
        """
        self.ifaces[name] = (mac, ip, link)
        link.connect(self, name)

    def add_route(self, dst_prefix: int, iface: str):
        """ Agregar ruta

        :param dst_prefix: Prefijo de destino a usar
        :type dst_prefix: int
        :param iface: Interface a la que pertenece
        :type iface: str
        """
        self.route[dst_prefix] = iface

    def set_arp(self, ip: int, mac: int):
        """ Establecer el protocolo de resolución de direcciones
        para un host.

        :param ip: IP del host
        :type ip: int
        :param mac: MAC del host
        :type mac: int
        """
        self.arp[ip] = mac

    def receive(self, port: str, frame: Frame):
        """ Recibir un frame y mostrar sus características.

        :param port: Puerto en el que se recibe
        :type port: str
        :param frame: Frame recibido
        :type frame: Frame
        """
        my_mac, my_ip, _ = self.ifaces[port]
        if frame.dst_mac != my_mac:
            return

        show_h(5, f"{self.name}: ENRUTAMIENTO L3 (entrada {port})",
               section="router")

        pkt = frame.packet

        show_h(4, "Fisica (L1)", section="router")
        show_h(3, "Bits recibidos", f"{frame.bits()}", section="router")

        show_h(4, "Enlace (L2)", section="router")
        show_h(4, "Paquete recibido", section="router")
        show_h(3, "MAC Origen", f"{frame.src_mac:02X}", section="router")
        show_h(3, "MAC Destino", f"{frame.dst_mac:02X}", section="router")
        show_h(3, "Trama recibida", str(frame), section="router")

        show_h(4, "Red (L3)", section="router")
        show_h(3, "IP Origen", f"{pkt.src_ip:02X}", section="router")
        show_h(3, "IP Destino", f"{pkt.dst_ip:02X}", section="router")
        show_h(3, "Datagrama recibido", str(pkt), section="router")

        out_iface = None
        for pref, iface in self.route.items():
            if (pkt.dst_ip >> 7) == pref:
                out_iface = iface
                break

        out_mac, out_ip, out_link = self.ifaces[out_iface]
        next_hop_mac = self.arp.get(pkt.dst_ip)

        new_frame = Frame(src_mac=out_mac, dst_mac=next_hop_mac, packet=pkt)

        show_h(4, "Reencapsulación L2", section="router")
        show_h(3, "MAC Origen", f"{new_frame.src_mac:02X}", section="router")
        show_h(3, "MAC Destino", f"{new_frame.dst_mac:02X}", section="router")
        show_h(3, "Trama enviada", str(new_frame), section="router")
        show_h(4, "Física (L1)", section="router")
        show_h(3, "Bits a enviar", f"{new_frame.bits()}", section="router")

        out_link.send(self, new_frame)
