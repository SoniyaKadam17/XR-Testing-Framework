# Automated XR Network Performance Testing Framework
I developed an Automated XR Network Performance Testing Framework in Python. The framework simulates XR workloads under different network conditions such as latency, jitter, packet loss, and bandwidth constraints. It includes six major components: an XR workload generator, a network impairment engine, a metrics collection engine, an experiment controller for automated testing, a data analysis module, and a reporting engine that generates graphs and summary reports. The framework can automatically execute multiple network scenarios, collect performance metrics, and produce visual reports for evaluating XR application performance.


## XR Workload Generator

Simulates:

- XR users
- Head tracking
- Hand interactions
- Video streams
- Network traffic

## Run

python src/main.py

## Profiles

low_load.json
medium_load.json
high_load.json
