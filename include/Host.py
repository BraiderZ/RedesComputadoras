from Datos import Frame, Packet, Segment
from PhysicalLayer import show_h
from Link import Link
from typing import Optional, Dict
import re

APP_NAMES = {
    1: "WhatsApp",
    2: "Instagram",
    3: "GMAIL",
    4: "Telegram",
    5: "Facebook",
}

# Puertos de servicio (didácticos pero plausibles):
# - TCP: casi todo viaja por 443 (HTTPS); Gmail por IMAPS 993 si no es vía web.
# - UDP: 443 para QUIC/HTTP3; WhatsApp suele usar UDP para llamadas
#        con STUN/ICE (p.ej. 3478).
SERVICE_PORTS = {
    "TCP": {
        1: 443,   # WhatsApp (HTTPS a su API/servicios)
        2: 443,   # Instagram (HTTPS)
        3: 993,   # Gmail (IMAPS) — si fuese por web sería 443
        4: 443,   # Telegram (MTProto sobre 443/TCP)
        5: 443,   # Facebook (HTTPS)
    },
    "UDP": {
        1: 3478,  # WhatsApp llamadas: STUN/TURN típico (didáctico)
        2: 443,   # Instagram con HTTP/3 (QUIC)
        3: 443,   # Gmail por web con HTTP/3
        4: 443,   # Telegram (algunos clientes/redes soportan QUIC)
        5: 443,   # Facebook con HTTP/3
    },
}


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

    def send_message(self, dst_ip: int, app_id: int,
                     payload: str, proto: str = "TCP"):
        """
        Envío con selección de aplicación (1..5) y protocolo (TCP/UDP).
        En L4 se usa un ÚNICO puerto de servicio según (proto, app_id).
        En L5 se imprime (número de app, mensaje).
        """
        proto = proto.upper()
        if proto not in ("TCP", "UDP"):
            raise ValueError(f"{self.name}: Protocolo no soportado: {proto}")

        if app_id not in APP_NAMES:
            raise ValueError(f"{self.name}: app_id inválido (1..5): {app_id}")

        service_port = SERVICE_PORTS[proto][app_id]

        show_h(5, f"{self.name}: APLICACIÓN → TRANSPORTE → RED → ENLACE", section="tx")

        # ----- L5 (Aplicación) -----
        show_h(4, "Aplicación (L5)", section="tx")
        show_h(3, "App seleccionada", f"{app_id} - {APP_NAMES[app_id]}", section="tx")
        show_h(3, "Mensaje", payload, section="tx")

        # Empaquetamos el app_id dentro del payload
        # para poder mostrarlo al recibir
        encoded_payload = f"[APP={app_id}] {payload}"

        # ----- L4 (Transporte): un único puerto de servicio -----
        seg = Segment(proto=proto, src_port=service_port,
                      dst_port=service_port, payload=encoded_payload)
        show_h(4, "Segmento (L4)", section="tx")
        show_h(3, "Protocolo", seg.proto, section="tx")
        show_h(3, "Puerto de servicio", str(service_port), section="tx")

        # ----- L3 (Red) -----
        pkt = Packet(src_ip=self.ip, dst_ip=dst_ip, segment=seg)
        show_h(4, "Paquete (L3)", section="tx")
        show_h(3, "IP Origen", f"{pkt.src_ip:02X}", section="tx")
        show_h(3, "IP Destino", f"{pkt.dst_ip:02X}", section="tx")

        # Decidir siguiente salto (modelo /1 con bit más alto)
        next_hop_ip = dst_ip if (dst_ip ^ self.ip) >> 7 == 0 else self.gateway_ip
        next_mac = self.arp.get(next_hop_ip)
        if next_mac is None:
            raise RuntimeError(f"{self.name}: No conozco la"
                               "MAC de {next_hop_ip} (ARP).")

        # ----- L2 (Enlace) -----
        frm = Frame(src_mac=self.mac, dst_mac=next_mac, eth_type=0x01, packet=pkt)
        show_h(4, "Trama (L2)", section="tx")
        show_h(3, "MAC Origen", f"{frm.src_mac:02X}", section="tx")
        show_h(3, "MAC Destino", f"{frm.dst_mac:02X}", section="tx")
        show_h(3, "EthType", f"{frm.eth_type:02X}", section="tx")

        if self.link:
            self.link.send(self, frm)

    def receive(self, port: str, frame: Frame):
        if frame.dst_mac != self.mac:
            return

        show_h(5, f"{self.name}: RECEPCIÓN Y SUBIDA DE CAPAS", section="rx")

        pkt = frame.packet
        seg = pkt.segment

        # ----- L2 -----
        show_h(4, "Trama (L2)", section="rx")
        show_h(3, "MAC Origen", f"{frame.src_mac:02X}", section="rx")
        show_h(3, "MAC Destino", f"{frame.dst_mac:02X}", section="rx")

        # ----- L3 -----
        show_h(4, "Paquete (L3)", section="rx")
        show_h(3, "IP Origen", f"{pkt.src_ip:02X}", section="rx")
        show_h(3, "IP Destino", f"{pkt.dst_ip:02X}", section="rx")

        # ----- L4 (único puerto de servicio) -----
        show_h(4, "Segmento (L4)", section="rx")
        show_h(3, "Protocolo", seg.proto, section="rx")
        # Ambos campos llevan el mismo valor para mantener compatibilidad con Segment
        show_h(3, "Puerto de servicio", str(seg.dst_port), section="rx")

        # ----- L5 (extraer app y mensaje del payload) -----
        app_id, msg = None, seg.payload
        m = re.match(r"^\[APP=(\d)]\s*(.*)$", seg.payload)
        if m:
            app_id = int(m.group(1))
            msg = m.group(2)
        show_h(4, "Aplicación (L5)", section="rx")
        if app_id in APP_NAMES:
            show_h(3, "App recibida", f"{app_id} - {APP_NAMES[app_id]}", section="rx")
        else:
            show_h(3, "App recibida", "No especificada", section="rx")
        show_h(3, "Mensaje recibido", msg, section="rx")