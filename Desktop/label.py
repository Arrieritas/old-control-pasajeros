import tkinter as ttk

def create_label(text:str, x:int, y:int):
    label = ttk.Label(text=text)
    label.place(x=y, y=y)