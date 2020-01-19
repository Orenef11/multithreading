import logging
from datetime import datetime, timedelta
from random import choice
from threading import Thread

LATENCY = range(0, 20000)
THROUGHPUT = range(0, 100000)
logger = logging.getLogger(__name__)


class StressThread(Thread):
    def __init__(self, name, runtime_duration, event):
        super().__init__(name=name)
        self.name = name
        self.runtime_duration = runtime_duration
        self.start_time = None
        self.end_time = None
        self.event = event
        self.daemon = True
        self.result = []

    @property
    def latency(self):
        return choice(LATENCY)

    @property
    def throughput(self):
        return choice(THROUGHPUT)

    def run(self):
        round_number = 1

        while not self.event.is_set():
            self.event.wait()
            if self.start_time is None:
                self.start_time = datetime.now()
            logging.debug(f"Print result of thread name '{self.name}' (round number '{round_number}')")
            self.result.append([self.latency, self.throughput])
            if self.end_time and self.end_time - self.start_time > timedelta(seconds=self.runtime_duration):
                self.end_time = datetime.now()
                return
            self.end_time = datetime.now()
            round_number += 1
