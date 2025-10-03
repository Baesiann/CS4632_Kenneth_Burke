# Cafe Optimization Simulation

## Overview

### Domain
Service industry — specifically, coffee shop operations and staffing efficiency.

### Problem Statement
This simulation addresses the question: How should resources (staffing, skill allocation, and scheduling) be allocated to maximize profits in a cafe environment, while balancing customer satisfaction and staff utilization?

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
├── README.md                  # Project overview and instructions
├── .gitignore                 # Ignored files (Python cache, envs, etc.)
├── requirements.txt           # Python dependencies
├── data/                      # CSV data export
├── src/                       # Source code
│   ├── main.py                # Entry point
│   ├── simulation/            # Simulation logic
│   |  ├── __init__.py
│   |  ├── barista.py          # Barista class and skill logic
│   |  ├── order.py            # Order class (service duration, profit)
│   |  └── customer.py         # Customer class and behaviors
|   └── data_management/       # Data Collection
│      ├── __init__.py         
│      ├── collector.py        # Helper class for customer dictionary
│      ├── export.py           # Helper class to export as CSV
│      └── metrics.py          # Calculation of metrics
├── docs/                      # Documentation, diagrams, proposal PDFs
│   ├── CS4632_Kenneth_Burke_M1.pdf
|   ├── CS4632_Kenneth_Burke_M2.pdf
│   ├── ClassUML.png
│   └── ActivityUML.png
└── notebooks/                 # Jupyter Testing
```

### Project Status
**Implemented so far**
- Baseline simulation environment has been developed
- Customer life cycle implemented and working (Arrival -> Queue)
- Data collection module functional
- Simple metric calculation
**Still to come**
- Creation of a GUI
- User control of environment variables
- Skill level implementation (Efficiency of servers)
- Scheduling Optimization
- Iteration of days

## Installation Instructions
1. Clone the repository
```bash
git clone https://github.com/Baesiann/CS4632_Kenneth_Burke
cd root-folder
```
2. Install dependencies
```
pip install -r requirements.txt
```
### Usage
Run the application from the project root directory
```
python main.py
```

## Arcitecture Overview
### Customer
Arrives from a doubly stochasitc Poisson process (Cox Model), enters queue in line for the next available barista. Each customer has their own ID, as well as metrics such as patience that are based off of a distribution. This matches well to my initial UML design.

### Barista
SimPy server resource, takes in and processes a Customer based on their Order. Compared to my UML design, many aspects of this class was stripped and it has simply become a SimPy resource.

### Order
Dictionary containing different types of order, the order the customer chooses is based off of a fixed probabilty, and the time it takes the server to prepare the order is based off of a normal distribution. This fits well into my initial UML design.

### Data Collection
Various helper classes and calculation classes for the purpose of collecting and calculating metrics. This was not a part of my UML design, a past overlook that I will not mistake for again in the future.