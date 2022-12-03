import serial
import tkinter as tk

from tkinter.ttk import Combobox
from serial.tools import list_ports


class ComChoosingFrame(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.rowconfigure(index=0,)
        # self.rowconfigure(index=1)
        # self.rowconfigure(index=2)

        tk.Label(
            self, text='Подключение к устройству', font=16, justify=tk.CENTER
        ).grid(row=0, column=0, sticky=tk.N, padx=1, pady=1)

        tk.Label(
            self, text='Serial:'
        ).grid(row=1, column=0, sticky=tk.W, pady=1)

        self.available_coms = Combobox(
            self, values=self.get_ports(), width=50, state='readonly',
        )
        self.available_coms.current(0)
        self.available_coms.grid(row=2, column=0, sticky=tk.W, padx=2, pady=1)

        tk.Button(
            self, text='Сканировать', command=self.update_com_ports,
        ).grid(row=2, column=1, padx=2, pady=1)

    def update_com_ports(self) -> None:
        """Updates list of available COMs in combobox."""
        self.available_coms.configure(values=self.get_ports())

    @staticmethod
    def get_ports() -> list:
        """Gets list of available COMs."""
        ports = list_ports.comports()
        return ['Не выбрано'] + [f'{port}: {desc}' for port, desc, _ in sorted(ports)]


class TimerConfigFrame(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # tk.Label(
        #     self, text='Конфигурация таймера', font=16
        # ).pack()
        # tk.Label(
        #     self, text='Время сброса:',
        # ).pack(anchor=tk.W)
        #
        # Combobox(
        #     self, values=tuple(str(i + 1) for i in range(5)), width=50, state='readonly',
        # ).pack(anchor=tk.E)


class TargetedAppsFrame(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class WatchDogApp:
    def __init__(self):
        self.root = tk.Tk()
        root = self.root
        root.title('USB WatchDog Agent v.1.0.0')
        root.geometry('600x700')
        root.resizable(width=False, height=False)

        # ComChoosingFrame(
        #     root, relief=tk.RAISED, borderwidth=2
        # ).pack(fill=tk.BOTH, expand=True)
        #
        # TimerConfigFrame(
        #     root, relief=tk.RAISED, borderwidth=1
        # ).pack(fill=tk.BOTH, expand=True)
        #
        # TargetedAppsFrame(
        #     root, relief=tk.RAISED, borderwidth=1
        # ).pack(fill=tk.BOTH, expand=True)
        com_choosing_frame = ComChoosingFrame(
            root, relief=tk.RAISED, borderwidth=2
        )

        timer_config_frame = TimerConfigFrame(
            root, relief=tk.RAISED, borderwidth=1
        )

        targeted_apps_frame = TargetedAppsFrame(
            root, relief=tk.RAISED, borderwidth=1
        )

        com_choosing_frame.grid(row=0, column=0)
        timer_config_frame.grid(row=1, column=0)
        targeted_apps_frame.grid(row=2, column=0)

    def run(self):
        self.root.mainloop()
