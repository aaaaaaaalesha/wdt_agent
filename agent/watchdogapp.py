import serial
import tkinter as tk

from tkinter.ttk import Combobox
from serial.tools import list_ports


class ComChoosingFrame(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        tk.Label(
            self, text='Serial:'
        ).pack(anchor=tk.W)

        self.com_ports = Combobox(
            self, values=self.get_ports(), width=50, state='readonly',
        )
        self.com_ports.pack(anchor=tk.W)

        tk.Button(
            self, text='Сканировать', command=self.update_com_ports,
        ).pack(anchor=tk.E)

    def update_com_ports(self) -> None:
        return

    @staticmethod
    def get_ports() -> list:
        ports = list_ports.comports()

        return [f'{port}: {desc}' for port, desc, _ in sorted(ports)]


class WatchDogApp:
    def __init__(self):
        self.root = tk.Tk()
        root = self.root
        root.title('USB WatchDog Agent v.1.0.0')
        root.geometry('600x700')
        root.resizable(width=False, height=False)

        ComChoosingFrame(
            root, relief=tk.RAISED, borderwidth=2
        ).pack(fill=tk.BOTH, expand=True)

        tk.Frame(
            root, relief=tk.RAISED, borderwidth=1
        ).pack(fill=tk.BOTH, expand=True)

        tk.Frame(
            root, relief=tk.RAISED, borderwidth=1
        ).pack(fill=tk.BOTH, expand=True)

    def run(self):
        self.root.mainloop()
