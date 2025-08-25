from Datos import Frame, Packet, Segment
from PhysicalLayer import show_h
from Link import Link   
from typing import Optional, Dict


class Host:
    def __init__(self, name: str, mac: int, ip: int, gateway_ip: int):
        self.name = name
        self.mac = mac
        self.ip = ip
        self.gateway_ip = gateway_ip
        self.link: Optional[Link] = None
        self.arp: Dict[int, int] = {}  # IP → MAC

    def plug(self, link: Link):
        self.link = link
        link.connect(self, "eth0")

    def set_arp(self, ip: int, mac: int):
        self.arp[ip] = mac

    def send_message(self, dst_ip: int, dst_port: int, payload: str, proto: str = "TCP", src_port: int = 12345):
        show_h(4, f"{self.name}: APLICACIÓN → TRANSPORTE → RED → ENLACE")

        seg = Segment(proto=proto, src_port=src_port, dst_port=dst_port, payload=payload)
        pkt = Packet(src_ip=self.ip, dst_ip=dst_ip, segment=seg)
        next_hop_ip = dst_ip if (dst_ip ^ self.ip) >> 7 == 0 else self.gateway_ip
        next_mac = self.arp.get(next_hop_ip)
        if next_mac is None:
            raise RuntimeError(f"{self.name}: No conozco la MAC de {next_hop_ip} (ARP).")

        frm = Frame(src_mac=self.mac, dst_mac=next_mac, eth_type=0x01, packet=pkt)

        # Mostrar Segmento
        show_h(3, "Segmento (L4)")
        show_h(4, "Protocolo", seg.proto)
        show_h(4, "Puerto Origen", str(seg.src_port))
        show_h(4, "Puerto Destino", str(seg.dst_port))
        show_h(4, "Datos", seg.payload)

        # Mostrar Paquete
        show_h(3, "Paquete (L3)")
        show_h(4, "IP Origen", f"{pkt.src_ip:02X}")
        show_h(4, "IP Destino", f"{pkt.dst_ip:02X}")

        # Mostrar Trama
        show_h(3, "Trama (L2)")
        show_h(4, "MAC Origen", f"{frm.src_mac:02X}")
        show_h(4, "MAC Destino", f"{frm.dst_mac:02X}")
        show_h(4, "EthType", f"{frm.eth_type:02X}")

        if self.link:
            self.link.send(self, frm)

    def receive(self, port: str, frame: Frame):
        if frame.dst_mac != self.mac:
            return
        show_h(4, f"{self.name}: RECEPCIÓN Y SUBIDA DE CAPAS")

        pkt = frame.packet
        seg = pkt.segment

        # Mostrar Trama
        show_h(3, "Trama (L2)")
        show_h(4, "MAC Origen", f"{frame.src_mac:02X}")
        show_h(4, "MAC Destino", f"{frame.dst_mac:02X}")

        # Mostrar Paquete
        show_h(3, "Paquete (L3)")
        show_h(4, "IP Origen", f"{pkt.src_ip:02X}")
        show_h(4, "IP Destino", f"{pkt.dst_ip:02X}")

        # Mostrar Segmento
        show_h(3, "Segmento (L4)")
        show_h(4, "Puerto Origen", str(seg.src_port))
        show_h(4, "Puerto Destino", str(seg.dst_port))
        show_h(4, "Datos recibidos", seg.payload)
