import time


def retry(attempt: int):
    """
    Exponential backoff.

    first try -> 1 second
    second try -> 2 seconds
    third try -> 4 seconds
    """

    delay = 2 ** (attempt - 1)

    print(f"[Retry] Waiting {delay}s before retry")

    time.sleep(delay)