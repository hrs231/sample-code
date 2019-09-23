import sys
from common.utils import Utils
from simulate_production_environment import SimulateProductionEnvironment


def main():
    """" Main Entry Point for this proof of concept production system """
    system_simulator = SimulateProductionEnvironment()

    input_data = Utils.get_input_file("data/sample_test_messages.txt")
    for msg_line in input_data:
        print(msg_line)
        response = system_simulator.process_input_data(msg_line)
        if response is not None:
            print(response)

if __name__ == "__main__":
    main()
