from typing import Dict

def to_bits(value: int, width: int) -> str:
    return format(value, f"0{width}b")
def text_to_bits(s: str) -> str:
    return "".join(format(ord(c), "08b") for c in s)
def show_bits(label: str, bits: str, max_len: int = 64) -> None:
    # Para no saturar la consola, truncamos la visualización
    out = bits if len(bits) <= max_len else bits[:max_len] + "... ({} bits)".format(len(bits))
    print(f"{label}: {out}")

def show_h(level: int, label: str, msg: str = ""):
    prefix = "#" * level
    print(f"{prefix} {label}{(': ' + msg) if msg else ''}")

def print_layer(title: str, headers: Dict[str, str], payload: str):
    print(f"\n---- {title} ----")
    for k, v in headers.items():
        print(f"{k}: {v}")
    print(f"Datos: {payload}")
    print("------------------")

