import pathlib as pl
import tkinter as tk
import customtkinter as ctk
import shutil

from tkinter import ttk
from tkinter import filedialog
from pathlib import Path



# Funciones
def cerrar():
    ventana.destroy()

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
    origen = Path(carpetaSelectValue.get())
    destino = Path(carpetaMoverSelectValue.get())

    extension = archivoSelect.get().lower()
    prefijo = prefijoValue.get()
    sufijo = sufijoValue.get()
    nombre_carpeta = crearCarpeta.get()

    # Comprobar carpeta de origen
    if not origen.exists() or not origen.is_dir():
        print("La carpeta de origen no existe o no es válida.")
        return

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
    for numero, foto in enumerate(fotos, start=1):

        nuevo_nombre = f"{prefijo}{numero:04d}{sufijo}{foto.suffix}"
        nuevo_archivo = destino / nuevo_nombre
        shutil.move(
            str(foto),
            str(nuevo_archivo)
        )
        print(f"Movido: {foto.name} → {nuevo_nombre}")

    print("Proceso terminado.")

def cambiar_modo():
    print("Funciona bien")

# Estructura de la ventana principal
ventana = tk.Tk()
ventana.title("Auto Assigmnment")
contenido = tk.Frame(
    ventana,
    padx=20, 
    pady=20
    )
contenido.pack()

# Seleccionar carpeta
carpetaSelectLabel = tk.Label(contenido, text="Trabajar con carpeta:", fg="white")
carpetaSelectLabel.grid(row=0, column=0, padx=10, pady=10, sticky="w")
carpetaSelectValue = tk.StringVar(
    value="No hay carpeta seleccionada"
)
carpetaSelectEntry = tk.Label(
    contenido, 
    textvariable=carpetaSelectValue, 
    fg="white",
    width=30
    )
carpetaSelectEntry.grid(row=0, column=1, padx=10, pady=10, sticky="w")
carpetaSelect = ctk.CTkButton(
    contenido, text="Seleccionar",
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
archivoSelectLabel = tk.Label(contenido, text="Tipo de archivo:", fg="white")
archivoSelectLabel.grid(row=1, column=0, padx=10, pady=10, sticky="w")
archivoSelect = ctk.CTkComboBox(
    contenido, 
    values=[
        "ARW",
        "HEIF",
        "JPEG",
        "RAW",
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
PrefijoLabel = tk.Label(contenido, text="Prefijo:", fg="white")
PrefijoLabel.grid(
    row=2, column=0, padx=10, pady=10, sticky="w"
)
Prefijo = ctk.CTkEntry(
    contenido,
    width=150,
    height=25,
    corner_radius=10,
    fg_color="#373636",
    text_color="#DAD9D9",
    border_width=0,
    textvariable=prefijoValue
    )
Prefijo.grid(row=2, column=1, padx=10, pady=10)

SufijoLabel = tk.Label(contenido, text="Sufijo:", fg="white")
SufijoLabel.grid(
    row=3, column=0, padx=10, pady=10, sticky="w"
)
Sufijo = ctk.CTkEntry(
    contenido,
    width=150,
    height=25,
    corner_radius=10,
    fg_color="#373636",
    text_color="#DAD9D9",
    border_width=0,
    textvariable=sufijoValue
    )
Sufijo.grid(row=3, column=1, padx=10, pady=10)

carpetaMoverSelectLabel = tk.Label(contenido, text="Carpeta de destino:", fg="white")
carpetaMoverSelectLabel.grid(row=4, column=0, padx=10, pady=10, sticky="w")
carpetaMoverSelectValue = tk.StringVar(
    value="No hay carpeta seleccionada"
)
carpetaMoverSelectEntry = tk.Label(
    contenido, 
    textvariable=carpetaMoverSelectValue, 
    fg="white",
    width=30
    )
carpetaMoverSelectEntry.grid(row=4, column=1, padx=10, pady=10, sticky="w")
carpetaMoverSelect = ctk.CTkButton(
    contenido, text="Seleccionar",
    command=lambda: carpetaMoverSelectValue.set(mover_archivos()),
    fg_color="#F2F2F2",
    hover_color="#CDCDCD",
    text_color="#373636",
    corner_radius=20
    )
carpetaMoverSelect.grid(row=4, column=2, padx=10, pady=10)

crearCapertaLabel = tk.Label(contenido, text="Nombre de la carpeta:", fg="white")
crearCapertaLabel.grid(
    row=5, column=0, padx=10, pady=10, sticky="w"
)
crearCarpeta = ctk.CTkEntry(
    contenido,
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
    contenido,
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
previsualizarArchivoLabel = tk.Label(contenido, text="Previsualización:", fg="white")
previsualizarArchivoLabel.grid(
    row=1, column=2, padx=10, pady=10, sticky="w"
)
prefijoValue.trace_add("write", actualizar_previsualizacion)
sufijoValue.trace_add("write", actualizar_previsualizacion)
previsualizacion = ctk.CTkLabel(
    contenido,
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
    contenido,
    text="Procesar fotos",
    command=procesar_fotos
)

"""

botonCambiarModod = ctk.CTkButton(
    contenido,
    text="Cambiar modo",
    command=cambiar_modo,
    fg_color="#F2F2F2",
    hover_color="#CDCDCD",
    text_color="#373636"
)

botonCambiarModod.grid(row=7, column=1, padx=10, pady=10)

"""
botonProcesar.grid(row=7, column=2, padx=10, pady=10)
ventana.mainloop()
