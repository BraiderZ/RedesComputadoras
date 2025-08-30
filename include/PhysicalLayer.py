from typing import Callable, Optional, Dict

_UI_HANDLER: Optional[Callable[[int, str, str, str], None]] = None

def set_ui_handler(handler: Optional[Callable[[int, str, str, str], None]]) -> None:
    """
    Registra un handler para recibir mensajes de show_h.
    Si handler=None, se vuelve al comportamiento por defecto (print a consola).
    """
    global _UI_HANDLER
    _UI_HANDLER = handler

def to_bits(value: int, width: int) -> str:
    return format(value, f"0{width}b")
def text_to_bits(s: str) -> str:
    return "".join(format(ord(c), "08b") for c in s)
def show_bits(label: str, bits: str, max_len: int = 255) -> None:
    # Para no saturar la consola, truncamos la visualización
    out = bits if len(bits) <= max_len else bits[:max_len] + "... ({} bits)".format(len(bits))
    print(f"{label}: {out}")

def show_h(level: int, label: str, msg: str = "", section: Optional[str] = None) -> None:
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

def print_layer(title: str, headers: Dict[str, str], payload: str):
    print(f"\n---- {title} ----")
    for k, v in headers.items():
        print(f"{k}: {v}")
    print(f"Datos: {payload}")
    print("------------------")

