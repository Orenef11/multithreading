from random import choice

from analyze import Analyze
from tools.args_parser import command_line_arguments
from tools.create_loggger import create_console_logger_handler

if __name__ == '__main__':
    args = command_line_arguments()
    create_console_logger_handler()
    analyze = Analyze(num_of_threads=choice(range(2, 10)), max_stress_duration=args.stress_duration)
    analyze.run()
    analyze.analyze()
