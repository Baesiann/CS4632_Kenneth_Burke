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
├── data/                      # CSV data management
├── src/                       # Source code
│   ├── __init__.py
│   ├── main.py                # Entry point
│   └── simulation/            # Simulation logic
│      ├── customer.py         # Customer class and behaviors
│      ├── barista.py          # Barista class and skill logic
│      ├── order.py            # Order class (service duration, profit)
│      └── queue_manager.py    # Queue handling, assignment logic
├── docs/                      # Documentation, diagrams, proposal PDFs
│   ├── CS4632_Kenneth_Burke_M1.pdf
│   ├── ClassUML.png
│   └── ActivityUML.png
└── notebooks/                 # Jupyter Testing
```