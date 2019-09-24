# Floyd Warshall Demo

### Overview

A quick PoC, to have a look at the viability of using Floyd Warshall algo to detect opportunities from inefficient pricing.

### SetUp

Best run using a virtual env

```bash
python -m pip install --upgrade pip
py -m pip install --user virtualenv

python -m venv .venv
.venv/Scripts/activate.ps1

Run below to set the root directory
setprojectdir .
```

### Usage

 
```bash
test_run_system_from_input_file.py
```

Will push test messages from data/sample_test_messages.txt into the system

```bash
STDIN | test_run_system_from_stdin.py
```

System handles messages from STDIN

```bash
tests/price_engine_tests.py
```

Runs very some (rather limited) unit tests ()

### Notes
* Components that have logging, create log files in the logs/ directory
* System built in Python, choose over C++, as quick to share and run
* This is a high level PoC knocked up, not intended for production use
* Large rate changes cause a recursive loop when outputting the path, this needs to be resolved.


### System Overview
System design to mimic an actual production environment, and uses the following components

* Input Handler - STDIN or Test File
* Environment Simulator
    * Exchange Simulator - pushes messages to line readers
    * Line Reader - accepts and logs the messages
    * Message Handler - creates messages
    * Price Engine - store the rates and contains logic
    * Rate Requesting Client Handler - to push user queries to the price engine

Price Update Message Path
````
PriceUpdates -> Simulated Exchange -> Line Reader -> Message Parser -> Price Engine
````

Rate Request Message Path
````
RateRequests <-> Client Handler <-> Price Engine
````

### ToDo
* Integrate into CI/CD environment
* Further Unit tests
* Split into microservices
* Build an adaptor to plug into live data feeds

### Notes
* 2019-09-23
* PoC needs much more work, to as trade fees and quantity available are real world factor that need to be taken into account.
* However, it does have potential to be a useful algo, and is worth looking at in further depth.

