# Versión de python: 3.12.1
# Diego Alfaro Segura (C20259), Ismael José Alvarado Pérez (C20366)

import streamlit as st
import os
import signal
import time
from pynput.keyboard import Controller, Key
from InputOutput import getInputs, printOutputs

# Limpieza de cache y establecer si se cierra quitar ventana
st.cache_data.clear()
st.cache_resource.clear()

keyboard = Controller()

# Header
# TODO: Agreguen sus carnets
st.title(':blue[Simulador de transmisión de mensajes] ')
st.subheader("Diego Alfaro Segura (C20259)," +
             "AGREGUEN CARNETS. Grupo \"Los Hamming\" ")

st.sidebar.write(':blue[Instrucciones de uso: ]\n' +
                 'Ingrese los datos a simular y presione \'Simular\'. \n'
                 )

st.sidebar.write('Para cerrar el programa porfavor usar este botón, ' +
                 'no cerrar la pestaña pues tendrá que cerrar la terminal' +
                 ' con CTRL + C ¡En windows podría tardar unos segundos!')

if st.sidebar.button("Cerrar programa."):
    time.sleep(0.0005)
    with keyboard.pressed(Key.ctrl):  # This will hold down the 'ctrl' key
        keyboard.press('w')            # Press 'w'
        time.sleep(0.1)
        keyboard.release('w')          # Release 'w'
    os.kill(os.getppid(), signal.SIGINT)
else:

    # Inputs generales.
    pc_sender, inputs = getInputs()

    # Mostrar outputs.
    printOutputs(pc_sender, inputs)
