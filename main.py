# Paquetes para streamlit
import subprocess
import importlib.util
import threading
import time

# Se busca si se tienen todos los paquetes
faltanPaquetes = False
listaPaquetes = ['streamlit', 'pynput', 'PIL']

print('Para usar este programa requiere tener instalado un navegador web' +
      ' . Se recomienda Firefox. Lea el Readme para mas información.')

for paquete in listaPaquetes:
    if importlib.util.find_spec(paquete) is None:
        faltanPaquetes = True

if not faltanPaquetes:
    # Dirección a interfaz
    app_path = 'include/Interfaz.py'

    # Correr aplicación
    command = ['streamlit', 'run', app_path]

    # Iniciar subproceso para interfaz
    process = subprocess.Popen(command)

    def monitor_process(process):
        # Finalizar el proceso si se cierra
        while True:
            retcode = process.poll()
            if retcode is not None:
                print("Programa cerrado correctamente")
                break
            time.sleep(1)

    # Usar un thread para monitoreo
    monitor_thread = threading.Thread(target=monitor_process, args=(process,))
    monitor_thread.start()

    try:
        monitor_thread.join()
    except KeyboardInterrupt:
        # Cerrar proceso
        process.terminate()
        process.wait()
        print("Programa finalizado con CTRL + C")
    finally:
        # Asegurarse de que se termina si no se cierra
        if process.poll() is None:
            print("Finalizando el proceso de streamlit...")
            process.kill()
else:
    print('\nNo tiene las librerías requeridas instaladas' +
          'Para usar el programa, debe instalarlas con el comando:\n' +
          'pip install -r requirements.txt')
