# Cafe Optimization Simulation

## Overview

### Domain
Service industry — specifically, coffee shop operations and staffing efficiency.

### Problem Statement
This simulation addresses the question: How should resources (staffing) be allocated to maximize profits in a cafe environment, while balancing customer satisfaction and staff utilization?

### Scope
The simulation will focus on customer arrivals, order processing, staff scheduling, and profit optimization.  

**We will not simulate:**
- Supply chain logistics (ingredient restocking, vendor relationships)
- Long-term customer loyalty trends outside of a single day
- External events, such as marketing campaigns, weather effects, or competition
- Costs of overhead outside of labor (i.e., rent, utilities)

**We will simulate:**
- Bursts of customer arrivals
- Menu complexity (different categories with varying service times)
- Customer abandonment
- Adaptive scheduling based on performance metrics

## Project Structure

```
cafe-optimization-simulation/
├── README.md
├── .gitignore
├── requirements.txt
├── data/
└── src/
    ├── main.py
    ├── simulation/
    │   ├── __init__.py
    │   ├── barista.py
    │   ├── order.py
    │   ├── customer.py
    │   ├── schedule_manager.py
    │   └── simulation_runner.py
    ├── data_management/
    │   ├── __init__.py
    │   ├── collector.py
    │   ├── export.py
    │   └── metrics.py
    ├── gui/
    │   ├── components/
    │   │   └── treev.py
    │   └── tabs/
    │       ├── data_tab.py
    │       └── simulation_tab.py
    ├── docs/
    └── notebooks/
```

### Project Status
**Implemented so far**
- Baseline simulation environment has been developed
- Customer life cycle implemented and working (Arrival -> Queue)
- Data collection module functional
- Simple metric calculation
- Creation of a GUI
- User control of environment variables
- Scheduling Optimization
- Iteration of days

**Still to come**
- Skill level implementation (Efficiency of servers)
- Hourly Analysis and Scheduling

## Installation Instructions
1. Clone the repository
```bash
git clone https://github.com/Baesiann/CS4632_Kenneth_Burke
cd CS4632_Kenneth_Burke
```
2. Install dependencies
```
pip install -r requirements.txt
```
### Usage
Run the application from the project root directory
```
python src/main.py
```

## Parameter Explanations
 - The name of the save file of the simulation can be customized, and it supports .csv exports as well as .json exports through the radio buttons.
### Setup
#### Simulation Days
 - Number of days the simulation will run for

#### Starting Baristas
 - The amount of baristas scheduled for the first day

#### Random Seed
 - An option to use a seed to generate consistent random numbers

### Customer Arrival
#### Baseline arrival rate
 - Customer per hour arrival rate

#### Randomness Intensity
 - How harshly the realized rate of customer arrivals will differentiate from the baseline rate, value of 2 is suggested. Examples of what this actually mean will be linked below.

[Example Default Randomness (2)](docs/default_rand.png)

[Example High Randomness (4)](docs/high_rand.png)

#### Morning/Lunch Rush Intensity
 - Sets the peak of the rush

#### Morning/Lunch Rush Duration
 - Sets the span of time that the rush will last for

## Order Setup
 - A default set of orders is imported, though drinks can be added and removed through the interface, and the treeview's values can be edited by double clicking on a cell.

## Example Outputs
### Visualization of a default simulation run
[Example Data Visualization Output](docs/data_vis.png)

### CLI output of a default simulation run
```bash
Running simulation with parameters: {'num_days': 5, 'base_baristas': 2, 'seed': 5232654, 'baseline_rate': 5.0, 'morning_intensity': 10.0, 'lunch_intensity': 8.0, 'rand_intensity': 2.0, 'morning_dur': 60, 'lunch_dur': 90}
Simulating Day 1 with 2 baristas
Day 1 Summary:
 - Average Wait Time: 0.44 min
 - Total Revenue: $361.50
 - Throughput: 0.19 customers/min
 - Dropped: 0 Customers

Today's dropped customers: 0
Re-evaluating barista staffing for tomorrow...

Testing 1 barista(s)...
 -> Drops: 16
Testing 2 barista(s)...
 -> Drops: 0
 => Optimal staffing for tomorrow: 2 baristas

Simulating Day 2 with 2 baristas
Day 2 Summary:
 - Average Wait Time: 0.29 min
 - Total Revenue: $451.50
 - Throughput: 0.23 customers/min
 - Dropped: 0 Customers

Today's dropped customers: 0
Re-evaluating barista staffing for tomorrow...

Testing 1 barista(s)...
 -> Drops: 2
Testing 2 barista(s)...
 -> Drops: 0
 => Optimal staffing for tomorrow: 2 baristas

Simulating Day 3 with 2 baristas
Day 3 Summary:
 - Average Wait Time: 0.20 min
 - Total Revenue: $352.50
 - Throughput: 0.19 customers/min
 - Dropped: 1 Customers

Today's dropped customers: 1
Re-evaluating barista staffing for tomorrow...

Testing 1 barista(s)...
 -> Drops: 10
Testing 2 barista(s)...
 -> Drops: 0
 => Optimal staffing for tomorrow: 2 baristas

Simulating Day 4 with 2 baristas
Day 4 Summary:
 - Average Wait Time: 0.22 min
 - Total Revenue: $351.00
 - Throughput: 0.19 customers/min
 - Dropped: 0 Customers

Today's dropped customers: 0
Re-evaluating barista staffing for tomorrow...

Testing 1 barista(s)...
 -> Drops: 20
Testing 2 barista(s)...
 -> Drops: 0
 => Optimal staffing for tomorrow: 2 baristas

Simulating Day 5 with 2 baristas
Day 5 Summary:
 - Average Wait Time: 0.18 min
 - Total Revenue: $304.50
 - Throughput: 0.16 customers/min
 - Dropped: 0 Customers

Today's dropped customers: 0
Re-evaluating barista staffing for tomorrow...

Testing 1 barista(s)...
 -> Drops: 11
Testing 2 barista(s)...
 -> Drops: 0
 => Optimal staffing for tomorrow: 2 baristas


==============================
   SCHEDULE SUMMARY (FINAL)
==============================
Day 1: 2 baristas scheduled
Day 2: 2 baristas scheduled
Day 3: 2 baristas scheduled
Day 4: 2 baristas scheduled
Day 5: 2 baristas scheduled
[+] Data saved to C:\dev\CS4632_Kenneth_Burke\data\simulation_run.csv
Runtime: 0.0876 seconds
```