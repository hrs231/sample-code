from common.utils import Utils
from floyd_warshall.simulate_production_environment import SimulateProductionEnvironment


def main():
    """" Main Entry Point for this proof of concept production system """
    system_simulator = SimulateProductionEnvironment()

    input_data = Utils.get_input_file("data/sample_test_messages.txt")
    output_lines = []
    for msg_line in input_data:
        print(msg_line)
        output_lines.append(msg_line)
        response = system_simulator.process_input_data(msg_line)
        if response is not None:
            print(response)
            output_lines.append(response)
    
    # for flask
    return '\n'.join(output_lines)

if __name__ == "__main__":
    main()
