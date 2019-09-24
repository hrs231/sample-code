# Floyd Warshall Demo

### Overview

A quick PoC, to have a look at the viability of using Floyd Warshall algo to detect opportunities from inefficient pricing.

A detailed problem description is in the docs directory.

### Run on cloud

For testing on the new cloud run service

[![Run on Google Cloud](https://storage.googleapis.com/cloudrun/button.svg)](https://console.cloud.google.com/cloudshell/editor?shellonly=true&cloudshell_image=gcr.io/cloudrun/button&cloudshell_git_repo=https://github.com/hrs231/sample-code.git&cloudshell_working_dir=floyd_warshall)

Just click button above (open in new tab), it'll provision a server, build the container and deploy using cloud run.

It'll produce an endpoint you can check

```bash
curl https://floyd-warshall-hgpw32quoa-uc.a.run.app/run-sample-data
```

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
bin/run_system_from_input_file.py
```

Will push test messages from data/sample_test_messages.txt into the system

```bash
STDIN | bin/run_system_from_stdin.py
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

