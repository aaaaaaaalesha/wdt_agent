import tkinter as tk

from tkinter.ttk import Combobox
from serial.tools import list_ports

from agent.utlis import get_process_dict, restart_app


class ComChoosingFrame(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        tk.Label(
            self, text='Подключение к устройству', font=16, justify=tk.CENTER,
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
        return ['Не выбрано'] + [f'{port}: {desc}' for port, desc, _ in
                                 sorted(ports)]


class TimerConfigFrame(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        tk.Label(
            self, text='Конфигурация таймера', font=16, justify=tk.CENTER,
        ).grid(row=0, column=0, sticky=tk.N, padx=1, pady=1)

        tk.Label(
            self, text='⚙ Время сброса:'
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
            self, text='Отслеживаемые процессы', font=16, justify=tk.CENTER,
        ).grid(row=0, column=0, sticky=tk.N, padx=1, pady=2)

        tk.Label(
            self, text='🔎 Введите имя процесса:'
        ).grid(row=1, column=0, sticky=tk.W)

        self.entry = tk.Entry(self)
        self.entry.grid(row=1, column=1)
        self.entry.bind('<KeyRelease>', self.search_entry)

        self.listbox = tk.Listbox(self, width=50)
        self.listbox.grid(row=2, column=0, pady=20)
        self.listbox.bind('<<ListboxSelect>>', self.fillout)
        self.processes_dict = get_process_dict()
        self.update_listbox(self.processes_list)

        tk.Button(
            self, text='Сканировать', command=self.scan_processes,
        ).grid(row=2, column=1, padx=2, pady=1)

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

    def update_listbox(self, process_list: list):
        self.listbox.delete(0, tk.END)
        for process_name in process_list:
            self.listbox.insert(tk.END, process_name)

    def search_entry(self, event) -> None:
        typed = self.entry.get()
        if not typed:
            self.update_listbox(self.processes_list)
            return

        self.update_listbox([
            process_name
            for process_name in self.processes_list
            if typed.lower() in process_name.lower()
        ])


class WatchDogApp:
    def __init__(self):
        self.root = tk.Tk()
        root = self.root
        root.title('USB WatchDog Agent v.1.0.0')
        root.geometry('500x600')
        root.resizable(width=False, height=False)

        com_choosing_frame = ComChoosingFrame(
            root, borderwidth=2,
        )

        timer_config_frame = TimerConfigFrame(
            root, borderwidth=1,
        )

        targeted_apps_frame = TargetedAppsFrame(
            root, borderwidth=1,
        )

        com_choosing_frame.grid(row=0, column=0)
        timer_config_frame.grid(row=1, column=0)
        targeted_apps_frame.grid(row=2, column=0)

    def run(self):
        self.root.mainloop()
