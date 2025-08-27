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

        show_h(4, f"{self.name}: ENRUTAMIENTO L3 (entrada {port})")

        pkt = frame.packet
        show_h(3, "Paquete recibido")
        show_h(4, "IP Origen", f"{pkt.src_ip:02X}")
        show_h(4, "IP Destino", f"{pkt.dst_ip:02X}")

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

        show_h(3, "Reencapsulación L2")
        show_h(4, "MAC Origen", f"{new_frame.src_mac:02X}")
        show_h(4, "MAC Destino", f"{new_frame.dst_mac:02X}")

        out_link.send(self, new_frame)