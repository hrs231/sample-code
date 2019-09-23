import sys
from simulate_production_environment import SimulateProductionEnvironment


def main():
    """" Run this script to push data from stdin into the proof of concept production system """
    system_simulator = SimulateProductionEnvironment()

    for msg_line in sys.stdin:
        response = system_simulator.process_input_data(msg_line)
        if response is not None:
            print(response)

if __name__ == "__main__":
    main()
