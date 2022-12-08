from concurrent.futures import ThreadPoolExecutor

from agent.watchdogapp import WatchDogApp

if __name__ == '__main__':
    app = WatchDogApp()
    with ThreadPoolExecutor() as pool:
        pool.submit(app.listening)
        pool.submit(app.check_targets)
        pool.submit(app.run())
