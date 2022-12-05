import tkinter as tk


def infinite_loop():
    while True:
        pass


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Приложение')
    root.geometry('300x300')
    tk.Button(
        root, text='Зависнуть!', command=infinite_loop
    ).pack(fill=tk.BOTH)

    root.mainloop()
