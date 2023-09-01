import tkinter as tk
from tkinter import ttk
from Processor.main import generate_passengers_control
from Writer.json import create_json_file
from Writer.excel import write_data
from Loader.file import get_data, select_file
from Desktop.button import create_button
from Desktop.label import create_label

def generate():
    print("Loading...")
    create_label(text="Generando...", x=120, y=260)

    data = get_data()
    result, despachos = generate_passengers_control(data)

    create_json_file(result)
    write_data(result, despachos)

    create_label(text="Completado :)", x=120, y=280)
    print("Complete :)")


window = tk.Tk()
window.title("Control de Pasajeros")
window.resizable(False, False)
window.config(width=500, height=340)
create_label(text="Generador de Control de Pasajeros", x=20, y=10)

create_label(text="Archivos Necesarios para el proceso:", x=40, y=40)

create_label(text="Itenerarios", x=50, y=110)
open_file_2 = ttk.Button(
    window,
    text='Seleccionar Archivo',
    command=lambda: select_file("itineraries")
)
open_file_2.pack(expand=True)
open_file_2.place(x=50, y=130)

create_label(text="Pasajeros", x=50, y=160)
open_file_3 = ttk.Button(
    window,
    text='Seleccionar Archivo',
    command=lambda: select_file("passengers")
)
open_file_3.pack(expand=True)
open_file_3.place(x=50, y=180)

create_button(text="Generar", command=generate, x=20, y=240)

window.mainloop()