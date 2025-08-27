from typing import Optional, Tuple, Any
from include.Datos import Frame


# =================== Dispositivos ===================


class Link:
    """Enlace punto a punto (cada puerto es un 'extremo')."""
    def __init__(self):
        self.a: Optional[Tuple[Any, str]] = None
        self.b: Optional[Tuple[Any, str]] = None

    def connect(self, node: Any, port_name: str):
        """ Realiza conexión de uno de los puertos al nodo dado.

        :param node: Nodo al cual realizar conexión
        :type node: Any
        :param port_name: Nombre del puerto
        :type port_name: str
        :raises RuntimeError: El enlace ya tiene dos extremos conectados.
        """
        if self.a is None:
            self.a = (node, port_name)
        elif self.b is None:
            self.b = (node, port_name)
        else:
            raise RuntimeError("El enlace ya tiene dos extremos conectados.")

    def send(self, sender: Any, frame: Frame):
        """ Invoca el método receive en el target de un envío de datos,
        le proporciona los datos que se envían. Evalúa los nodos en ambos
        puertos, si existen y son iguales al sender, se asigna el otro como
        receptor. Si el receptor existe se invoca el receive.

        :param sender: Nodo emisor del mensaje
        :type sender: Any
        :param frame: #TODO: Escribir descripción de param frame
        :type frame: Frame
        """
        target = None
        if self.a and self.a[0] is sender:
            target = self.b
        elif self.b and self.b[0] is sender:
            target = self.a
        if target is None:
            return
        node, port = target
        node.receive(port, frame)
