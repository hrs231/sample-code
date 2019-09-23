# Floyd Warshall Demo

### Overview

A quick PoC

### SetUp

Best run using a virtual env
```python
python -m pip install --upgrade pip
py -m pip install --user virtualenv

python -m venv .venv
.venv/Scripts/activate.ps1

Run below to set the root directory
setprojectdir .
```

### Usage

 
```python
test_run_system_from_input_file.py
```

Will push test messages from data/sample_test_messages.txt into the system

```python
STDIN | test_run_system_from_stdin.py
```

System handles messages from STDIN

```python
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
* Unit tests light
* Split into microservices
* Build an adaptor to plug into live data feeds
