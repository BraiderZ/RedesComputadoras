from include.Link import Link
from include.RouterL3 import RouterL3
from include.SwitchL2 import SwitchL2
from include.Host import Host

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

print("\n=================== SIMULACIÓN DE RED ===================\n")
print("\n=================== PC1 -> PC2 (TCD-Whatsapp) ===================\n")
# PC1 → PC2 usando WhatsApp por TCP (443)
pc1.send_message(dst_ip=PC2_IP, app_id=1, payload="Hola!", proto="TCP")
print("\n=================== PC2 -> PC1 (TCD-Gmail) ===================\n")
# PC2 → PC1 usando Gmail por TCP (IMAPS 993)
pc2.send_message(dst_ip=PC1_IP, app_id=3, payload="Nuevo correo", proto="TCP")
print("\n=================== PC1 -> PC2 (UDP-Instagram) ===================\n")
# PC1 → PC2 usando Instagram por UDP (HTTP/3 443/UDP)
pc1.send_message(dst_ip=PC2_IP, app_id=2, payload="Foto enviada", proto="UDP")
