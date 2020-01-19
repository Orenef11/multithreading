import argparse


def command_line_arguments():
    parser = argparse.ArgumentParser(description="Welcome to Oren's simulate stress on the ScyllaDB database")
    parser.add_argument('--stress_duration', help='How long the stress will be applied (In seconds)', type=int,
                        required=False)

    return parser.parse_args()
