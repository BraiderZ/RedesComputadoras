from typing import Callable, Optional

_UI_HANDLER: Optional[Callable[[int, str, str, str], None]] = None


def set_ui_handler(handler: Optional[Callable[[int, str, str, str], None]]):
    """
    Registra un handler para recibir mensajes de show_h.
    Si handler=None, se vuelve al comportamiento por defecto (print a consola).
    """
    global _UI_HANDLER
    _UI_HANDLER = handler


def to_bits(value: int, width: int) -> str:
    """ Convertir un valor entero a su representación en bits.

    :param value: Valor a convertir
    :type value: int
    :param width: Ancho de bits
    :type width: int
    :return: Secuencia de bits.
    :rtype: str
    """
    return format(value, f"0{width}b")


def text_to_bits(s: str) -> str:
    """ Convertir texto a su representación en bits

    :param s: Texto
    :type s: str
    :return: Secuencia de bits
    :rtype: str
    """
    return "".join(format(ord(c), "08b") for c in s)


def show_h(level: int, label: str, msg: str = "",
           section: Optional[str] = None) -> None:
    """
    Emite un mensaje jerárquico. Si hay handler, lo invoca con la sección.
    section: 'tx' | 'router' | 'rx'.
    """
    if _UI_HANDLER is not None:
        sec = section or "router"
        _UI_HANDLER(level, label, msg, sec)
        return

    # Fallback a consola
    prefix = "#" * level
    print(f"{prefix} {label}{(': ' + msg) if msg else ''}")
