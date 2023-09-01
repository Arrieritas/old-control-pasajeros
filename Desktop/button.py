import tkinter as ttk

def create_button(text:str, command, x:int, y:int):
    button = ttk.Button(text=text, command=command)
    button.place(x=x, y=y)