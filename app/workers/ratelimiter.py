import time


class RateLimiter:
    

    def __init__(self, interval: int):
        self.interval = interval
        self.lastcalled = 0

    def wait(self):
        

        now = time.time()

        elapsed = now - self.lastcalled

        remaining = self.interval - elapsed

        if remaining > 0:
            print(f"[Limiter] Waiting {remaining:.2f}s")
            time.sleep(remaining)

        self.lastcalled = time.time()