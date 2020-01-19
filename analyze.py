import logging
from datetime import datetime, timedelta
from random import choices
from threading import Event, Semaphore, Thread
from time import sleep

from tabulate import tabulate

from stress import StressThread

logger = logging.getLogger(__name__)


class Analyze(Thread):
    def __init__(self, num_of_threads, max_stress_duration):
        super().__init__(name='Analyze task')
        self.result = {}
        self.block_threads_event = Event()
        self.semaphore = Semaphore()
        runtime_duration_list = choices(range(1, max_stress_duration), k=num_of_threads)
        self.runtime_duration = max(runtime_duration_list) + 1
        self.start = None
        self.threads = []

        for idx, runtime_duration in enumerate(runtime_duration_list):
            self.threads.append(
                StressThread(name=f'thread-{idx}', runtime_duration=runtime_duration, event=self.block_threads_event))
            self.threads[-1].start()

    def run(self):
        if self.start is None:
            self.start = datetime.now()

        round_number = 1
        while datetime.now() < self.start + timedelta(seconds=self.runtime_duration):
            self.semaphore.acquire()
            self.block_threads_event.clear()
            logging.debug(f"Analyze thread - round number '{round_number}'")
            round_number += 1
            sleep(1)
            self.block_threads_event.set()
            self.semaphore.release()
        [thread.join() for thread in self.threads]

    def analyze(self):
        table_headers, threads_size = ['latency', 'throughput'], len(self.threads)
        summary_table, summary_headers = [], ['Latency', 'Throughput', '95th Percentile']
        result = {idx: [[0] * len(table_headers)] * threads_size for idx in range(0, self.runtime_duration)}
        logger.info(f"The number of stress threads that ran are '{len(self.threads)}'")
        for thread in self.threads:
            column_idx = int(thread.name.split('-', maxsplit=1)[1])
            logger.info(f"The thread '{thread.name}' started running at '{thread.start_time}' and ended at "
                        f"'{thread.end_time}' (total time '{thread.end_time - thread.start_time}')")

            [result[round_idx].__setitem__(column_idx, round_result)
             for round_idx, round_result in enumerate(thread.result)]

        logger.info('The summary:')
        for round_idx, table in result.items():
            table = [[min(line), max(line), sum(line) * 0.95] for line in table]
            table_to_print = tabulate(tabular_data=table, headers=summary_headers, tablefmt='grid')
            logger.info(f"The result of round '{round_idx}':\n{table_to_print}")
