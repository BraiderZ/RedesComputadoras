# Instrucciones para ejecutar el programa

Este programa se recomienda ejecutarlo con el interprete de Python 3.12.1, ademas de utilizar  un entorno virtual para gestionar las dependencias. 

##  Requisitos previos
- Tener instalada la versión **Python 3.12** (64-bit).
- Tener disponible el comando `py` en Windows o `python3` en Linux/MacOS.


A continuación se muestran los pasos para crear y activar un `venv` en **Python 3.12**.

---

## 1. Verificar versión de Python instalada
En **Windows**, abre PowerShell o CMD y ejecuta:

```powershell
py --version
```
o en **Linux/MacOS**
```bash
python3 --version
```
Este debe corresponder a Python 3.12

## 2. Crear el entorno virtual
En la carpeta raíz del proyecto, ejecuta:

**Windows**
```powershell
py -3.12 -m venv env
```

o en **Linux/MacOS**
```bash
python3 -3.12 -m venv env
```
## 3. Activar el entorno virtual
En **Windows** 

```powershell
.\env\Scripts\Activate.ps1
```

En **Linux / MacOS**
```bash
source env/bin/activate
```
## 4. Instalar dependencias del proyecto

```bash
pip install -r requirements.txt
```

## 5. Ejecutar el programa

En la carpeta raíz del proyecto, ejecuta:

**Windows**
```powershell
py main.py
```

o en **Linux/MacOS**
```bash
python3 main.py
```

Al ejecutar el programa se abre una pestaña en el navegador donde se despliega el programa.

## 6. Desactivar el entorno virtual

Cuando termines de usar el programa, puedes salir del entorno virtual con:
```bash
deactivate
```
