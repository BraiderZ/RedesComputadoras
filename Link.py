from typing import Optional, Tuple, Any, Dict
from Datos import Frame, Packet, Segment
from PhysicalLayer import text_to_bits, print_layer

# =================== Dispositivos ===================

class Link:
    """Enlace punto a punto (cada puerto es un 'extremo')."""
    def __init__(self):
        self.a: Optional[Tuple[Any, str]] = None
        self.b: Optional[Tuple[Any, str]] = None

    def connect(self, node: Any, port_name: str):
        if self.a is None:
            self.a = (node, port_name)
        elif self.b is None:
            self.b = (node, port_name)
        else:
            raise RuntimeError("El enlace ya tiene dos extremos conectados")

    def send(self, sender: Any, frame: Frame):
        target = None
        if self.a and self.a[0] is sender:
            target = self.b
        elif self.b and self.b[0] is sender:
            target = self.a
        if target is None:
            return
        node, port = target
        node.receive(port, frame)