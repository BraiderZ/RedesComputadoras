# Versión de python: 3.12.1
# Diego Alfaro Segura (C20259), Ismael José Alvarado Pérez (C20366)

import streamlit as st
import os
import signal
import time
from pynput.keyboard import Controller, Key
from InputOutput import getInputs, printOutputs
from PhysicalLayer import set_ui_handler

# Limpieza de cache y establecer si se cierra quitar ventana
st.cache_data.clear()
st.cache_resource.clear()

keyboard = Controller()

# Header
# TODO: Agreguen sus carnets
st.title(':blue[Simulador de transmisión de mensajes] ')
st.subheader("Diego Alfaro Segura (C20259)," +
             "\nPablo Salas Gómez (C27061)," +
             "AGREGUEN CARNETS. Grupo \"Los Hamming\" ")

st.sidebar.write(':blue[Instrucciones de uso: ]\n' +
                 'Ingrese los datos a simular y presione \'Simular\'. \n'
                 )

st.sidebar.write('Para cerrar el programa porfavor usar este botón, ' +
                 'no cerrar la pestaña pues tendrá que cerrar la terminal' +
                 ' con CTRL + C ¡En windows podría tardar unos segundos!')

if st.sidebar.button("Cerrar programa"):
    time.sleep(0.0005)
    with keyboard.pressed(Key.ctrl):  # This will hold down the 'ctrl' key
        keyboard.press('w')            # Press 'w'
        time.sleep(0.1)
        keyboard.release('w')          # Release 'w'
    os.kill(os.getppid(), signal.SIGINT)
else:    
    # Inputs generales.
    pc_sender, inputs = getInputs()

    simular = st.button("Simular", type="primary")

    if simular:
        tx_entries: list[tuple[int, str, str]] = []
        router_entries: list[tuple[int, str, str]] = []
        rx_entries: list[tuple[int, str, str]] = []

        def _ui_handler(level: int, label: str, msg: str, section: str) -> None:
            """Clasifica cada línea en 'tx', 'router' o 'rx' y la guarda localmente."""
            entry = (level, label, msg)
            if section == "tx":
                tx_entries.append(entry)
            elif section == "rx":
                rx_entries.append(entry)
            else:
                router_entries.append(entry)

        def _render_entries(entries: list[tuple[int, str, str]]) -> None:
            """Dibuja cada línea con jerarquía según el nivel."""
            for level, label, msg in entries:
                text = f"{label}{': ' + msg if msg else ''}"
                if level >= 5:
                    st.header(text)
                elif level == 4:
                    st.subheader(text)
                elif level == 3:
                    st.markdown(f"**{text}**")
                else:
                    st.write(text)

        # Redirige show_h al handler
        set_ui_handler(_ui_handler)

        # Mostrar outputs.
        printOutputs(pc_sender, inputs)

        st.subheader("Resultado de la simulación")
        tx_tab, router_tab, rx_tab = st.tabs(
            ["Transmisor + switch", "Router", "Receptor + switch"]
        )

        with tx_tab:
            _render_entries(tx_entries)
        with router_tab:
            _render_entries(router_entries)
        with rx_tab:
            _render_entries(rx_entries)
