import time

class Timer:
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.name = ''

    def start(self, name):
        self.start_time = time.time()
        self.name = name

    def stop(self, verbose):
        if self.start_time is None:
            return
        self.end_time = time.time()
        elapsed_time = self.end_time - self.start_time
        if verbose:
            print(f"{self.name}: {elapsed_time:.2f} seconds")
