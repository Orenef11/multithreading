import argparse


def command_line_arguments():
    parser = argparse.ArgumentParser(description="Welcome to Oren's simulate stress on the ScyllaDB database")
    parser.add_argument('--stress_duration', type=int, help='How long the stress will be applied (In seconds)',
                        required=True)

    return parser.parse_args()
