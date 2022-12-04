import subprocess
import psutil

from typing import Optional, Dict, Tuple, List


def restart_app(app: str, restart_path: str) -> None:
    """
    Forced kills the process, with children and restarts it again.
    Source:
    https://stackoverflow.com/questions/52818668/how-to-restart-other-program-in-python
    :param app: path to process to kill
    :param restart_path: path to restart process
    :return: None
    """
    subprocess.call(['taskkill', '/F', '/T', '/IM', app])
    subprocess.Popen([restart_path, '--fast'])


def get_process_dict() -> Dict[str, Tuple[str, List[str]]]:
    """
    Collects the dict of running processes.
    process_name -> Tuple[exe_path, cmdline]
    :return: resulted dict of processes
    """
    processes: Dict[str, Tuple[str, List[str]]] = {}
    for process in psutil.process_iter():
        process_params = __get_params(process)
        if process_params is not None:
            processes[process_params[0]] = (  # process_name
                process_params[1],  # exe_path
                process_params[2],  # cmdline
            )

    return processes


def __get_params(
        process: psutil.Process
) -> Optional[Tuple[str, str, List[str]]]:
    try:
        process_name = process.name()
        exe_path = process.exe()
        cmdline = process.cmdline()
        is_none_or_empty = any([
            attr is None or not attr
            for attr in (process_name, exe_path, cmdline)
        ])
        if is_none_or_empty or exe_path.startswith('C:\\Windows\\System'):
            return None

        return process_name, exe_path, cmdline
    except psutil.AccessDenied:
        return None
