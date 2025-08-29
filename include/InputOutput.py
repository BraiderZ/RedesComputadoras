import streamlit as st
from Link import Link
from RouterL3 import RouterL3
from SwitchL2 import SwitchL2
from Host import Host

# Direcciones (8 bits, valores hex para que se vean compactos)
PC1_MAC, PC1_IP = 0x0A, 0x01
PC2_MAC, PC2_IP = 0x0B, 0x82          # Nota: bit más alto=1 → "otra red" (/1)
R_L_MAC, R_L_IP = 0x11, 0x10          # Router – interfaz izquierda
R_R_MAC, R_R_IP = 0x22, 0x90          # Router – interfaz derecha

# Enlaces
l_pc1_sw1 = Link()
l_sw1_r = Link()
l_r_sw2 = Link()
l_sw2_pc2 = Link()

# Dispositivos
pc1 = Host("PC1", PC1_MAC, PC1_IP, gateway_ip=R_L_IP)
pc2 = Host("PC2", PC2_MAC, PC2_IP, gateway_ip=R_R_IP)
sw1 = SwitchL2("Switch1")
sw2 = SwitchL2("Switch2")
r = RouterL3("Router")

# Conexiones físicas
pc1.plug(l_pc1_sw1)
sw1.add_port("fa0/1", l_pc1_sw1)
sw1.add_port("fa0/2", l_sw1_r)
r.add_iface("g0/0", R_L_MAC, R_L_IP, l_sw1_r)
r.add_iface("g0/1", R_R_MAC, R_R_IP, l_r_sw2)
sw2.add_port("fa0/1", l_r_sw2)
sw2.add_port("fa0/2", l_sw2_pc2)
pc2.plug(l_sw2_pc2)

# "ARP" (tablas mínimas)
pc1.set_arp(R_L_IP, R_L_MAC)  # PC1 conoce MAC del gateway
pc2.set_arp(R_R_IP, R_R_MAC)  # PC2 conocería su gateway (no en recepción)
r.set_arp(PC1_IP, PC1_MAC)    # Router conoce MAC de PC1
r.set_arp(PC2_IP, PC2_MAC)    # Router conoce MAC de PC2

# Rutas (/1: 0xxxxxxx → izquierda, 1xxxxxxx → derecha)
r.add_route(0b0, "g0/0")
r.add_route(0b1, "g0/1")

APP_NAMES = {
    "WhatsApp":  1,
    "Instagram": 2,
    "GMAIL":     3,
    "Telegram":  4,
    "Facebook":  5,
}


def getInputs() -> dict[str, any]:
    # Obtener inputs
    st.write('Ingrese los valores de la simulación:')
    pc_receptor = st.selectbox('PC receptor', ['PC 1', 'PC 2'])
    aplicacion = st.selectbox('Aplicación', list(APP_NAMES.keys()))
    payload = st.text_input('Payload a enviar', 'Hola Mundo!')
    proto = st.selectbox('Protocolo', ['TCP', 'UDP'])

    #
    dst_ip = PC1_IP if pc_receptor == 'PC 1' else PC2_IP
    app_id = APP_NAMES.get(aplicacion)

    pc_sender = pc2 if pc_receptor == 'PC 1' else pc1
    inputs = {
        'dst_ip': dst_ip,
        'app_id': app_id,
        'payload': payload,
        'proto': proto
    }

    if pc_sender is pc1:
        sw1.section = "tx"
        sw2.section = "rx"
    else:
        sw1.section = "rx"
        sw2.section = "tx"

    return pc_sender, inputs


def printOutputs(pc_sender: Host, inputs: dict[str, any]):
    pc_sender.send_message(dst_ip=inputs.get('dst_ip'),
                           app_id=inputs.get('app_id'),
                           payload=inputs.get('payload'),
                           proto=inputs.get('proto'))
    print("\n")
