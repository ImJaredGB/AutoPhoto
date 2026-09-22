import pathlib as pl
import tkinter as tk
import customtkinter as ctk
import shutil

from tkinter import ttk
from tkinter import filedialog
from pathlib import Path



# Funciones
def seleccionar_carpeta():
    ventanaCarpeta = tk.Tk()
    ventanaCarpeta.withdraw()
    ventanaCarpeta.attributes('-topmost', True)

    ruta = tk.filedialog.askdirectory(
        title="Seleccionar carpeta"
    )

    ventanaCarpeta.destroy()

    if not ruta:
        print("No se seleccionó ninguna carpeta.")
        return None
    else:
        print(f"Carpeta seleccionada: {ruta}")
        carpetaSelectValue.set(ruta)

def seleccionar_carpeta_automatica():

    global sd_conectada

    ventanaCarpetaAuto = tk.Tk()
    ventanaCarpetaAuto.withdraw()
    ventanaCarpetaAuto.attributes('-topmost', True)

    ruta_auto = tk.filedialog.askdirectory(
        title="Seleccionar carpeta"
    )

    ventanaCarpetaAuto.destroy()

    if not ruta_auto:
        print("No se seleccionó ninguna carpeta.")
        return None
    
    
    print(f"Carpeta seleccionada: {ruta_auto}")
    carpetaAutomaticaSelectValue.set(ruta_auto)
    sd_conectada = False
    detectar_sd()

    


def mover_archivos():
    ventanaMover = tk.Tk()
    ventanaMover.withdraw()
    ventanaMover.attributes("-topmost", True)

    rutaMover = tk.filedialog.askdirectory(
        title="Seleccionar carpeta de destino"
    )
    ventanaMover.destroy()

    if not rutaMover:
        print("No se seleccionó ninguna carpeta de destino.")
        return None
    else:
        print(f"Carpeta de destino seleccionada: {rutaMover}")
        return rutaMover

def seleccionar_archivo():
    archivo = pl.Path(archivoSelect.get())
    print(f"Archivo seleccionado: {archivo}")

def actualizar_previsualizacion(*args):
    prefijo = prefijoValue.get()
    sufijo = sufijoValue.get()
    extension = archivoSelect.get()

    nombre = f"{prefijo}Archivo{sufijo}.{extension}"

    previsualizacion.configure(
        text=nombre
    )

def estado_checkbox():
    print(checkboxValue.get())

def procesar_fotos():
    if (
        carpetaSelectValue.get() == "No hay carpeta seleccionada"
        or
        carpetaMoverSelectValue.get() == "No hay carpeta seleccionada"
    ):
        animar_error()
        return

    animar_proceso()

    origen = Path(carpetaSelectValue.get())
    destino = Path(carpetaMoverSelectValue.get())

    extension = archivoSelect.get().lower()

    prefijo = prefijoValue.get()
    sufijo = sufijoValue.get()

    nombre_carpeta = crearCarpeta.get()

    # Comprobar crear o usar destino
    if checkboxValue.get():

        destino = destino / nombre_carpeta
        destino.mkdir(parents=True, exist_ok=True)

    else:

        destino.mkdir(parents=True, exist_ok=True)

    # Buscar fotos
    fotos = list(origen.glob(f"*.{extension}"))

    if not fotos:
        print(f"No se encontraron archivos {extension}")
        return

    # Procesar fotos
    for foto in fotos:

        nuevo_nombre = ( f"{prefijo}" f"{foto.stem}" f"{sufijo}" f"{foto.suffix}" )

        nuevo_archivo = destino / nuevo_nombre

        shutil.move(
            str(foto),
            str(nuevo_archivo)
        )

        print(f"Movido: {foto.name} → {nuevo_nombre}")

    print("Proceso terminado.")

def animar_error(paso=0):
    colores = [
        "#752121",
        "#852F2F",
        "#752121",
        "#852F2F",
        "#752121",
        "#852F2F",
        "#752121"
    ]

    if paso < len(colores):
        botonProcesar.configure(
            text="Faltan datos",
            fg_color=colores[paso]
        )

        ventana.after(
            100,
            lambda: animar_error(paso + 1)
        )

    else:

        botonProcesar.configure(
            text="x",
            fg_color="#622626"
        )

        ventana.after(
            1000,
            finalizar_animacion
        )

def animar_proceso(paso=0):
    colores = [
        "#555555",
        "#505C52",
        "#4C624F",
        "#48694C",
        "#43704A",
        "#3E7647",
        "#3A7D44"
    ]

    if paso < len(colores):

        botonProcesar.configure(
            text="Procesando...",
            fg_color=colores[paso]
        )

        ventana.after(
            100,
            lambda: animar_proceso(paso + 1)
        )

    else:

        botonProcesar.configure(
            text="✓",
            fg_color="#3A7D44"
        )

        ventana.after(
            1000,
            finalizar_animacion
        )


def finalizar_animacion():
    botonProcesar.configure(
        text="Procesar fotos",
        fg_color="#1F6AA5"
    )

def cambiar_modo():
    vista_principal.grid_remove()
    vista_automatica.grid(row=0, column=0)
    iniciar_modo_automatico()

"""
Experimental
"""
detector_activo = False
sd_conectada = False
def iniciar_modo_automatico():
    print("Modo automatico activo")
    global detector_activo

    if detector_activo:
        return

    detector_activo = True
    detectar_sd()
    

def detener_modo_automatico():
    print("Modo automatico pausado")
    global detector_activo

    detector_activo = False

def detectar_sd():

    global sd_conectada

    if not detector_activo:
        return

    ruta_sd = Path(carpetaAutomaticaSelectValue.get())

    conectada = ruta_sd.exists() and ruta_sd.is_dir()

    if conectada and not sd_conectada:
        print("SD conectada")
        sd_conectada = True
        procesar_sd(ruta_sd)

    elif not conectada and sd_conectada:
        print("SD desconectada")
        sd_conectada = False

    ventana.after(1000, detectar_sd)

def volver():
    detener_modo_automatico()
    vista_automatica.grid_remove()
    vista_principal.grid(row=0, column=0)

def procesar_sd(ruta_sd):
    print(f"Procesando SD: {ruta_sd}")

    carpetas_ignoradas = {
        "AVF_INFO",
        ".fseventsd"
    }

    archivos = []

    for archivo in ruta_sd.rglob("*"):

        if not archivo.is_file():
            continue

        # Ignorar archivos auxiliares de macOS
        if archivo.name.startswith("._"):
            continue

        # Ignorar carpetas del sistema de la SD
        if any(
            carpeta.name in carpetas_ignoradas
            for carpeta in archivo.parents
        ):
            continue

        # Ignorar carpetas creadas por AutoPhoto
        if any(
            carpeta.name.startswith("AP_")
            for carpeta in archivo.parents
        ):
            continue

        archivos.append(archivo)

    if not archivos:
        print("No se han encontrado archivos nuevos en la SD")
        return

    print(f"Se han encontrado {len(archivos)} archivos:")

    for archivo in archivos:

        extension = archivo.suffix.lower().replace(".", "")

        if not extension:
            continue

        carpeta_destino = ruta_sd / f"AP_{extension.upper()}"
        carpeta_destino.mkdir(exist_ok=True)

        destino = carpeta_destino / archivo.name

        shutil.move(str(archivo), str(destino))

        print(f"{archivo.name} -> {carpeta_destino.name}/")
"""
FIN EXPERIMENTAL
"""

# Estructura de la ventana principal
ventana = tk.Tk()
ventana.title("Auto Assignment")
contenedor = tk.Frame(
    ventana,
    padx=20,
    pady=20
)

contenedor.pack()


vista_principal = ctk.CTkFrame(contenedor)
vista_principal.grid(row=0, column=0)
vista_automatica = ctk.CTkFrame(contenedor)

# Vista automática
carpetaAutomaticaLabel = ctk.CTkLabel(
    vista_automatica,
    text="Trabajar con carpeta",
)
carpetaAutomaticaLabel.grid(row=0,column=0,padx=10,pady=10)


carpetaAutomaticaSelectValue = tk.StringVar(
    value="No hay carpeta seleccionada"
)
carpetaAutomaticaEntry = ctk.CTkLabel(
    vista_automatica,
    textvariable=carpetaAutomaticaSelectValue,
    text_color="#888888"
)
carpetaAutomaticaEntry.grid(row=0,column=1,padx=10,pady=10)


botonSeleccionarAutomatica = ctk.CTkButton(
    vista_automatica,
    command=seleccionar_carpeta_automatica,
    text="Seleccionar",
    fg_color="#F2F2F2",
    hover_color="#CDCDCD",
    text_color="#373636",
    corner_radius=20
)
botonSeleccionarAutomatica.grid(row=0,column=2,padx=10,pady=10)

botonVolver = ctk.CTkButton(
    vista_automatica,
    text="Volver",
    command=volver,
    fg_color="#F2F2F2",
    hover_color="#CDCDCD",
    text_color="#373636",
)
botonVolver.grid(row=1,column=1,padx=10,pady=10)

# Seleccionar carpeta
carpetaSelectLabel = tk.Label(vista_principal, text="Trabajar con carpeta:")
carpetaSelectLabel.grid(row=0, column=0, padx=10, pady=10)
carpetaSelectValue = tk.StringVar(
    value="No hay carpeta seleccionada"
)
carpetaSelectEntry = tk.Label(
    vista_principal, 
    textvariable=carpetaSelectValue,
    width=30
    )
carpetaSelectEntry.grid(row=0, column=1, padx=10, pady=10)
carpetaSelect = ctk.CTkButton(
    vista_principal, text="Seleccionar",
    command=seleccionar_carpeta,
    fg_color="#F2F2F2",
    hover_color="#CDCDCD",
    text_color="#373636",
    corner_radius=20
    )
carpetaSelect.grid(row=0, column=2, padx=10, pady=10)

prefijoValue = tk.StringVar()
sufijoValue = tk.StringVar()

# Archivos a trabajar
archivoSelectLabel = tk.Label(vista_principal, text="Tipo de archivo:")
archivoSelectLabel.grid(row=1, column=0, padx=10, pady=10)
archivoSelect = ctk.CTkComboBox(
    vista_principal, 
    values=[
        "ARW",
        "HEIF",
        "JPEG",
        "RAW",
        "JPG",
        "MP4"],
    width=150,
    height=25,
    corner_radius=10,
    fg_color="#373636",
    text_color="#DAD9D9",
    border_width=0,
    command=actualizar_previsualizacion
    )

archivoSelect.grid(row=1, column=1, padx=10, pady=10)
archivoSelectValue = archivoSelect.get()
print(archivoSelectValue)

# Estructura del nombre final del archivo
PrefijoLabel = tk.Label(vista_principal, text="Prefijo:")
PrefijoLabel.grid(
    row=2, column=0, padx=10, pady=10
)
Prefijo = ctk.CTkEntry(
    vista_principal,
    width=150,
    height=25,
    corner_radius=10,
    fg_color="#373636",
    text_color="#DAD9D9",
    border_width=0,
    textvariable=prefijoValue
    )
Prefijo.grid(row=2, column=1, padx=10, pady=10)

SufijoLabel = tk.Label(vista_principal, text="Sufijo:")
SufijoLabel.grid(
    row=3, column=0, padx=10, pady=10
)
Sufijo = ctk.CTkEntry(
    vista_principal,
    width=150,
    height=25,
    corner_radius=10,
    fg_color="#373636",
    text_color="#DAD9D9",
    border_width=0,
    textvariable=sufijoValue
    )
Sufijo.grid(row=3, column=1, padx=10, pady=10)

carpetaMoverSelectLabel = tk.Label(vista_principal, text="Carpeta de destino:")
carpetaMoverSelectLabel.grid(row=4, column=0, padx=10, pady=10)
carpetaMoverSelectValue = tk.StringVar(
    value="No hay carpeta seleccionada"
)
carpetaMoverSelectEntry = tk.Label(
    vista_principal, 
    textvariable=carpetaMoverSelectValue,
    width=30
    )
carpetaMoverSelectEntry.grid(row=4, column=1, padx=10, pady=10)
carpetaMoverSelect = ctk.CTkButton(
    vista_principal, text="Seleccionar",
    command=lambda: carpetaMoverSelectValue.set(mover_archivos()),
    fg_color="#F2F2F2",
    hover_color="#CDCDCD",
    text_color="#373636",
    corner_radius=20
    )
carpetaMoverSelect.grid(row=4, column=2, padx=10, pady=10)

crearCapertaLabel = tk.Label(vista_principal, text="Nombre de la carpeta:")
crearCapertaLabel.grid(
    row=5, column=0, padx=10, pady=10
)
crearCarpeta = ctk.CTkEntry(
    vista_principal,
    width=150,
    height=25,
    corner_radius=10,
    fg_color="#373636",
    text_color="#DAD9D9",
    border_width=0
    )
crearCarpeta.grid(row=5, column=1, padx=10, pady=10)

checkboxValue = tk.BooleanVar(value=False)

checkbox = ctk.CTkCheckBox(
    vista_principal,
    text="Crear carpeta",
    variable=checkboxValue,
    command=estado_checkbox
)
checkbox.grid(
    row=5,
    column=2,
    columnspan=2,
    pady=10
)
previsualizarArchivoLabel = tk.Label(vista_principal, text="Previsualización:")
previsualizarArchivoLabel.grid(
    row=1, column=2, padx=10, pady=10
)
prefijoValue.trace_add("write", actualizar_previsualizacion)
sufijoValue.trace_add("write", actualizar_previsualizacion)
previsualizacion = ctk.CTkLabel(
    vista_principal,
    text="Archivo.JPG",
    text_color="#888888"
)
previsualizacion.grid(
    row=2,
    column=2,
    columnspan=2,
    pady=5
)

botonProcesar = ctk.CTkButton(
    vista_principal,
    text="Procesar fotos",
    command=procesar_fotos
)

botonCambiarModo = ctk.CTkButton(
    vista_principal,
    text="Cambiar modo",
    command=cambiar_modo,
    fg_color="#F2F2F2",
    hover_color="#CDCDCD",
    text_color="#373636"
)

botonCambiarModo.grid(row=7, column=1, padx=10, pady=10)
botonProcesar.grid(row=7, column=2, padx=10, pady=10)

"""
Boton de Pruebas

botonTest = ctk.CTkButton(
    vista_automatica,  <-- Cambiar vista
    text="Test",
    command=detectar_sd #      <- Cambiar funcion
)
botonTest.grid(row=1,column=0,padx=10,pady=10)  <-- Cambiar posicion

"""


ventana.mainloop()
