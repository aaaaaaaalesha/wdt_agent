import tkinter as tk

from typing import Optional
from serial import Serial
from tkinter.ttk import Combobox
from tkinter.messagebox import showerror

from agent.utlis import get_process_dict, restart_app
from agent.serial_com import get_ports

BACKGROUND = '#D3D3D3'


class ComChoosingFrame(tk.Frame):
    NOT_CHOSEN = 'Не выбрано'
    CONNECTED = 'подключено'
    NOT_CONNECTED = f'не {CONNECTED}'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connected_port: Optional[Serial] = None

        tk.Label(
            self, text='Подключение к устройству', font=20,
            background=BACKGROUND
        ).grid(row=0, column=0, padx=1, pady=1, sticky=tk.W)

        tk.Label(
            self, text='Serial:', background=BACKGROUND
        ).grid(row=1, column=0, sticky=tk.W, pady=1)

        self.available_coms = Combobox(
            self, values=self.combobox_values, width=50, state='readonly',
        )
        self.available_coms.grid(
            row=2, column=0, sticky=tk.W, padx=2, pady=1
        )
        self.available_coms.current(0)
        self.available_coms.bind('<<ComboboxSelected>>', self.com_selected)

        tk.Button(
            self, text='Сканировать', command=self.update_com_ports,
        ).grid(row=2, column=1, padx=2, pady=1)

        self.status = tk.StringVar(value=f'Статус: {self.NOT_CONNECTED}')
        tk.Label(
            self, textvariable=self.status, background=BACKGROUND
        ).grid(row=3, column=0, padx=2, pady=1, sticky=tk.E)

        self.connect_btn = tk.Button(
            self, text='Подключиться', command=self.connect, state='disabled',
        )
        self.connect_btn.grid(row=3, column=1, padx=2, pady=3)

        self.disconnect_btn = tk.Button(
            self, text='Отключиться', command=self.disconnect,
            state='disabled',
        )
        self.disconnect_btn.grid(row=4, column=1, padx=2, pady=3)

    def update_com_ports(self) -> None:
        """Updates list of available COMs in combobox."""
        self.available_coms.configure(values=self.combobox_values)

    @property
    def combobox_values(self):
        return [self.NOT_CHOSEN] + get_ports()

    def com_selected(self, event):
        if self.available_coms.get() != self.NOT_CHOSEN:
            self.connect_btn.config(state='normal')
            return

        self.connect_btn.config(state='disabled')

    def connect(self):
        chosen = self.available_coms.get()
        if chosen == self.NOT_CHOSEN:
            showerror(
                title='Упс!', message='Вы не выбрали подходящий COM.'
            )
            return

        try:
            name = chosen.split(':')[0]
            self.connected_port = Serial(name, 9600)
            print(f'Connected successfully {self.connected_port}')
        except Exception as err:
            self.connected_port = None
            self.status.set(f'Статус: {self.NOT_CONNECTED}')
            showerror('Критическая ошибка!', str(err))
            return

        self.status.set(f'Статус: {self.CONNECTED}')
        self.disconnect_btn.config(state='normal')

    def disconnect(self):
        try:
            self.connected_port.close()
            self.connected_port = None
            self.status.set(f'Статус: {self.NOT_CONNECTED}')
            self.disconnect_btn.config(state='disabled')
        except Exception as err:
            self.status.set(f'Статус: {self.NOT_CONNECTED}')
            showerror('Критическая ошибка!', str(err))
            return


class TimerConfigFrame(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        tk.Label(
            self, text='Конфигурация таймера', font=20, background=BACKGROUND
        ).grid(columnspan=3, row=0, column=0, padx=1, pady=1, sticky=tk.W)

        tk.Label(
            self, text='Время сброса:', background=BACKGROUND
        ).grid(row=1, column=0, sticky=tk.W, pady=1)

        Combobox(
            self, values=tuple(str(i + 1) for i in range(5)), state='readonly',
        ).grid(row=1, column=1, padx=2, pady=1)
        tk.Label(
            self, text='мс', background=BACKGROUND
        ).grid(row=1, column=2, pady=1)


class TargetedAppsFrame(tk.Frame):
    target_processes = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        tk.Label(
            self, text='Отслеживание процессов', font=20,
            background=BACKGROUND
        ).grid(columnspan=3, row=0, column=0, padx=1, pady=2, sticky=tk.W)

        tk.Label(
            self, text='Введите имя процесса:', background=BACKGROUND
        ).grid(row=1, column=0, sticky=tk.W, padx=1, pady=2)

        self.entry = tk.Entry(self)
        self.entry.grid(row=1, column=1, pady=2)
        self.entry.bind('<KeyRelease>', self.search_entry)

        self.add_target_btn = tk.Button(
            self, text='Отслеживать', command=self.add_target, state='disabled'
        )
        self.add_target_btn.grid(row=1, column=2, sticky=tk.E, pady=10)

        #############################

        tk.Label(
            self, text='Запущенные процессы:', background=BACKGROUND
        ).grid(row=2, column=0, sticky='SW')

        tk.Button(
            self, text='Обновить', command=self.scan_processes,
        ).grid(row=2, column=1, padx=5, pady=1, sticky=tk.E)

        self.listbox_processes = tk.Listbox(self, width=50, relief=tk.RAISED)
        self.listbox_processes.grid(columnspan=2, row=3, column=0,
                                    padx=5, pady=3)
        self.listbox_processes.bind('<<ListboxSelect>>', self.fill_out)

        self.processes_dict = get_process_dict()
        self.update_listbox(self.processes_list)

        #############################

        tk.Label(
            self, text='Отслеживаемые процессы:', background=BACKGROUND
        ).grid(row=4, column=0, sticky='SW')

        self.listbox_targets = tk.Listbox(
            self, width=50, relief=tk.RAISED, selectmode=tk.EXTENDED
        )
        self.listbox_targets.grid(
            columnspan=2, row=5, column=0, padx=5, pady=3
        )
        self.listbox_targets.bind(
            '<<ListboxSelect>>', self.raise_buttons
        )

        self.restart_target_btn = tk.Button(
            self, text='Рестарт', command=self.target_restart, state='disabled'
        )
        self.restart_target_btn.grid(
            row=5, column=2, padx=5, pady=1,
        )

        self.remove_target_btn = tk.Button(
            self, text='Удалить', command=self.remove_target, state='disabled'
        )
        self.remove_target_btn.grid(
            row=6, column=1, padx=5, pady=1, sticky=tk.E
        )

    @property
    def processes_list(self):
        return list(self.processes_dict.keys())

    def scan_processes(self):
        self.processes_dict = get_process_dict()
        self.update_listbox(self.processes_list)
        self.entry.delete(0, tk.END)

    def fill_out(self, event):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, self.listbox_processes.get(tk.ANCHOR))
        self.add_target_btn.config(state='normal')

    def update_listbox(self, process_list: list):
        self.listbox_processes.delete(0, tk.END)
        for process_name in process_list:
            self.listbox_processes.insert(tk.END, process_name)

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
        process_name = self.entry.get()
        exe_path, cmdline = self.processes_dict[process_name]
        if process_name in self.target_processes:
            showerror(
                title='Внимание',
                message='Данный процесс уже отслеживается!'
            )
        else:
            self.listbox_targets.insert(tk.END, process_name)
            self.target_processes[process_name] = (exe_path, cmdline)

        self.entry.delete(0, tk.END)
        self.search_entry(event=None)

    def remove_target(self):
        process_name = self.listbox_targets.get(tk.ANCHOR)
        self.target_processes.pop(process_name)
        self.listbox_targets.delete(tk.ANCHOR)
        self.disable_buttons()

    def raise_buttons(self, event):
        self.remove_target_btn.config(state='normal')
        self.restart_target_btn.config(state='normal')

    def disable_buttons(self):
        self.remove_target_btn.config(state='disabled')
        self.restart_target_btn.config(state='disabled')

    def target_restart(self):
        process_name = self.listbox_targets.get(tk.ANCHOR)
        exe_path, _ = self.processes_dict[process_name]
        kill_code, process_open = restart_app(process_name, exe_path)
        if kill_code != 0:
            showerror(
                title='Увы и ах!',
                message='Не удалось "убить" процесс :('
            )
            return
        if process_open is not None:
            showerror(
                title='Увы и ах!',
                message='Процесс убит, но не перезапущен :('
            )
            return

        self.remove_target()
