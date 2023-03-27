from serial.tools import list_ports


def get_ports() -> list:
    """Gets list of available COMs."""
    ports = list_ports.comports()
    return [f'{port}: {desc}' for port, desc, _ in sorted(ports)]
