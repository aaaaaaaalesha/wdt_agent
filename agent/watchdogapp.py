import tkinter as tk

from tkinter.ttk import Combobox
from serial.tools import list_ports

from agent.utlis import get_process_dict, restart_app


class ComChoosingFrame(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        tk.Label(
            self, text='Подключение к устройству', font=16,
        ).grid(row=0, column=0, padx=1, pady=1)

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
        return ['Не выбрано'] + [f'{port}: {desc}' for port, desc, _ in
                                 sorted(ports)]


class TimerConfigFrame(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        tk.Label(
            self, text='Конфигурация таймера', font=16,
        ).grid(row=0, column=0, sticky=tk.N, padx=1, pady=1)

        tk.Label(
            self, text='Время сброса:'
        ).grid(row=1, column=0, sticky=tk.W, pady=1)

        Combobox(
            self, values=tuple(str(i + 1) for i in range(5)), state='readonly',
        ).grid(row=1, column=1, padx=2, pady=1)
        tk.Label(
            self, text='мс'
        ).grid(row=1, column=2, pady=1)


class TargetedAppsFrame(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        tk.Label(
            self, text='Отслеживание процессов', font=16,
        ).grid(row=0, column=0, padx=1, pady=2)

        tk.Label(
            self, text='Введите имя процесса:'
        ).grid(row=1, column=0, sticky=tk.E, padx=1, pady=2)

        self.entry = tk.Entry(self)
        self.entry.grid(row=1, column=1, pady=2)
        self.entry.bind('<KeyRelease>', self.search_entry)

        tk.Label(
            self, text='Запущенные процессы:',
        ).grid(row=2, column=0, sticky='SW')
        self.listbox = tk.Listbox(self, width=50, relief=tk.RAISED)
        self.listbox.grid(rowspan=2, columnspan=2, row=3, column=0, ipadx=6)
        self.listbox.bind('<<ListboxSelect>>', self.fillout)

        tk.Button(
            self, text='Сканировать', command=self.scan_processes,
        ).grid(row=3, column=2, padx=2, pady=1)

        self.add_target_btn = tk.Button(
            self, text='Отслеживать', command=self.add_target, state='disabled'
        )
        self.add_target_btn.grid(row=3, column=2, sticky=tk.E)

        self.processes_dict = get_process_dict()
        self.update_listbox(self.processes_list)

    @property
    def processes_list(self):
        return list(self.processes_dict.keys())

    def scan_processes(self):
        self.processes_dict = get_process_dict()
        self.update_listbox(self.processes_list)
        self.entry.delete(0, tk.END)

    def fillout(self, event):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, self.listbox.get(tk.ANCHOR))
        self.add_target_btn.config(state='normal')

    def update_listbox(self, process_list: list):
        self.listbox.delete(0, tk.END)
        for process_name in process_list:
            self.listbox.insert(tk.END, process_name)

    def search_entry(self, event) -> None:
        self.add_target_btn.config(state='disabled')
        typed = self.entry.get()
        if not typed:
            self.update_listbox(self.processes_list)
            return

        self.update_listbox([
            process_name
            for process_name in self.processes_list
            if typed.lower() in process_name.lower()
        ])

    def add_target(self):
        pass


class WatchDogApp:
    TITLE = 'USB WatchDog Agent v.1.0.0'

    # WEIGHT = 500
    # HEIGHT = 600

    def __init__(self):
        self.root = tk.Tk()
        root = self.root
        root.title(self.TITLE)
        # root.geometry(f'{self.WEIGHT}x{self.HEIGHT}')
        root.resizable(width=False, height=True)

        com_choosing_frame = ComChoosingFrame(
            root, borderwidth=5, background='gray'
        )

        timer_config_frame = TimerConfigFrame(
            root, borderwidth=5, background='gray',
        )

        targeted_apps_frame = TargetedAppsFrame(
            root, borderwidth=5, background='gray',
        )

        com_choosing_frame.grid(row=0, sticky='WE')
        timer_config_frame.grid(row=1, sticky='WE')
        targeted_apps_frame.grid(row=2, sticky='WE')

    def run(self):
        self.root.mainloop()
