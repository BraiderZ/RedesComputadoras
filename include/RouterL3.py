from typing import Dict, Optional, Tuple
from Datos import Frame
from Link import Link
from PhysicalLayer import show_h


class RouterL3:
    def __init__(self, name: str):
        self.name = name
        self.ifaces: Dict[str, Tuple[int, int, Optional[Link]]] = {}
        self.route: Dict[int, str] = {}
        self.arp: Dict[int, int] = {}

    def add_iface(self, name: str, mac: int, ip: int, link: Link):
        self.ifaces[name] = (mac, ip, link)
        link.connect(self, name)

    def add_route(self, dst_prefix: int, iface: str):
        self.route[dst_prefix] = iface

    def set_arp(self, ip: int, mac: int):
        self.arp[ip] = mac

    def receive(self, port: str, frame: Frame):
        my_mac, my_ip, _ = self.ifaces[port]
        if frame.dst_mac != my_mac:
            return

        show_h(5, f"{self.name}: ENRUTAMIENTO L3 (entrada {port})", section="router")

        pkt = frame.packet


        show_h(4,"Fisica (L1)", section="router")
        show_h(3, "bits recibidos", f"{frame.bits()}", section="router")

        show_h(4, "Enlace (L2)", section="router")
        show_h(4, "Paquete recibido", section="router")
        show_h(3, "IP Origen", f"{pkt.src_ip:02X}", section="router")
        show_h(3, "IP Destino", f"{pkt.dst_ip:02X}", section="router")
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
        if out_iface is None:
            raise RuntimeError(f"{self.name}: No hay ruta al destino {pkt.dst_ip:02X}")

        out_mac, out_ip, out_link = self.ifaces[out_iface]
        next_hop_mac = self.arp.get(pkt.dst_ip)
        if next_hop_mac is None:
            raise RuntimeError(f"{self.name}: No conozco la MAC del siguiente salto para {pkt.dst_ip:02X}")

        new_frame = Frame(src_mac=out_mac, dst_mac=next_hop_mac, eth_type=0x01, packet=pkt)

        show_h(4, "Reencapsulación L2", section="router")
        show_h(3, "MAC Origen", f"{new_frame.src_mac:02X}", section="router")
        show_h(3, "MAC Destino", f"{new_frame.dst_mac:02X}", section="router")
        show_h(3, "Paquete", str(pkt), section="router")
        

        show_h(4, "Física (L1)", section="router")
        show_h(3, "bits a enviar", f"{new_frame.bits()}", section="router")

        out_link.send(self, new_frame)