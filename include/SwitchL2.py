from typing import Dict, Optional
from Datos import Frame
from Link import Link
from PhysicalLayer import show_h

class SwitchL2:
    def __init__(self, name: str, section: Optional[str] = None):
        self.name = name
        self.ports: Dict[str, Link] = {}
        self.mac_table: Dict[int, str] = {}
        self.section = section

    def add_port(self, name: str, link: Link):
        self.ports[name] = link
        link.connect(self, name)

    def receive(self, port: str, frame: Frame):
        self.mac_table[frame.src_mac] = port
        dst_port = self.mac_table.get(frame.dst_mac)
        action = "FLOOD" if dst_port is None else f"→ {dst_port}"

        show_h(5, f"{self.name}: CONMUTACIÓN L2 ({action})", section=self.section)
        show_h(4, "Tabla MAC aprendida", section=self.section)
        for mac, p in self.mac_table.items():
            show_h(3, f"{mac:02X}", p, section=self.section)

        if dst_port is None:
            for p, link in self.ports.items():
                if p != port:
                    link.send(self, frame)
        else:
            self.ports[dst_port].send(self, frame)