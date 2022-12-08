import tkinter as tk
import psutil

from time import sleep

from agent.frames import ComChoosingFrame, TimerConfigFrame, TargetedAppsFrame
from agent.utlis import run_app

BACKGROUND = '#D3D3D3'


class WatchDogApp:
    TITLE = 'USB WatchDog Agent v.1.0.0'

    def __init__(self):
        self.root = tk.Tk()
        self.is_running = True
        root = self.root
        root.title(self.TITLE)
        root.resizable(width=False, height=False)
        root.protocol('WM_DELETE_WINDOW', self.on_exit)

        self.com_choosing_frame = ComChoosingFrame(
            root, borderwidth=5, background=BACKGROUND, border=1
        )

        self.timer_config_frame = TimerConfigFrame(
            root, borderwidth=5, background=BACKGROUND, border=1
        )

        self.targeted_apps_frame = TargetedAppsFrame(
            root, borderwidth=5, background=BACKGROUND, border=1
        )

        self.com_choosing_frame.grid(row=0, sticky='WE')
        self.timer_config_frame.grid(row=1, sticky='WE')
        self.targeted_apps_frame.grid(row=2, sticky='WE')

    def run(self):
        self.is_running = True
        self.root.mainloop()

    def on_exit(self):
        self.is_running = False
        self.root.destroy()

    def check_targets(self):
        while self.is_running:
            running_proc_names = {
                process.name()
                for process in psutil.process_iter()
            }
            target_processes = self.targeted_apps_frame.target_processes
            for name_process, exe_cmdline in target_processes.items():
                if name_process not in running_proc_names:
                    run_app(exe_cmdline[0])

            sleep(3)
