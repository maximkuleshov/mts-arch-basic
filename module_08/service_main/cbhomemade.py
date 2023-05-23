# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from enum import Enum

class Status(Enum):
    CLOSED = 0
    HALF_OPEN = 1
    OPEN = 2 

class CircuitBreakerHome:
    def __init__(self, n):
        self.name = n
        self.status = Status.CLOSED
        self.failures = 0
    
    def wrap(self, func, exception, attempts, timeout, fallback):
        self.func = func
        self.exception = exception
        self.attempts = attempts
        self.timeout = timeout
        self.fallback = fallback

        return self.wrapper

    def wrapper(self, *args, **kwargs):
        if self.status == Status.OPEN:
            if self.latest_fail_ts + timedelta(seconds = self.timeout) > datetime.now():
                return self.fallback(*args, **kwargs)
            print("Timeout elapsed, retrying...")
            self.status = Status.HALF_OPEN

        try:
            result = self.func(*args, **kwargs)
            if self.status == Status.HALF_OPEN:
                print("Ok. Going back to CLOSED")
                self.status = Status.CLOSED
                self.failures = 0
            return result
        except Exception as err:
            if isinstance(err, self.exception):
                self.process_failure()
            raise err

    def process_failure(self):
        self.latest_fail_ts = datetime.now()
        self.failures += 1
        if self.failures >= self.attempts:
            print(f"Failed attempt count: {self.failures}, switching to OPEN")
            self.status = Status.OPEN


    


