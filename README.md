# Discrete-Event Simulation Projects

A portfolio of **Python-based discrete-event simulation (DES) projects** focused on modeling dynamic systems, analyzing performance, and comparing alternative resource configurations. Each project has its own folder with source code, model documentation, and results.

The repository currently contains two projects:

1. [Repairman–Spare Machine System](./repairman-spare-machine-system/)
2. [Three-Server Queueing System Simulation](./three-server-queueing-simulation/)

---

## Projects

### 1. Repairman–Spare Machine System

**Focus:** Reliability, maintenance operations, repair capacity, spare inventory, and resource-cost trade-offs.

This project models a system of operating machines that may fail and require repair. Spare machines help maintain operation when failures occur, while limited repair capacity can create waiting queues and machine downtime.

The project includes separate Python scripts for:
- Simulating system performance under different numbers of repairmen.
- Estimating performance measures across repeated runs, including point estimates and 95% Student's *t* confidence intervals.
- Comparing repairman and spare-machine configurations using a cost function to identify a low-cost configuration within the explored search range.

**Selected measures and analyses**
- Machine failures and unavailable-machine counts
- Lost machine time and transition time
- Maximum repair queue length
- Repairman workload / utilization
- Cost comparison across resource configurations

**Technologies:** Python, NumPy, SciPy, Matplotlib.

**Explore the project:** [Open Repairman–Spare Machine System](./repairman-spare-machine-system/)

For model assumptions, reported estimates, charts, and run instructions, see the [project README](./repairman-spare-machine-system/README.md).

### 2. Three-Server Queueing System Simulation

**Focus:** Customer waiting, shared-queue behavior, server workload, and simulation replication analysis.

This project implements an event-driven queueing model with three parallel servers and a shared first-in, first-out (FIFO) queue. Customers are assigned to an idle server; when all servers are busy, they wait in the shared queue.

**Model highlights**
- An eight-hour (480-minute) arrival window.
- Discrete uniform interarrival and server-specific service-time distributions.
- A shared FIFO queue and random assignment among available idle servers.
- A rule that stops generating new arrivals after the arrival window while allowing customers already in the system to finish.
- A reproducible random seed and comparison across 1,000, 2,000, 4,000, and 6,000 replications.

**Performance measures**
- Average waiting time and average time in the system
- Average total arrivals and maximum queue length
- Average number of customers served by each server
- Server utilization during the observation window
- Cumulative averages to inspect how estimates change as replications increase

**Technologies:** Python, pandas, Matplotlib, heap-based event scheduling.

**Explore the project:** [Open Three-Server Queueing Simulation](./three-server-queueing-simulation/)

The project README includes the parameter assumptions, result summary, convergence plots, individual output-file descriptions, model diagrams, and instructions for running the simulation.

---

## How to Explore

1. Choose a project from the sections above.
2. Open its README for the model assumptions, performance measures, and reported results.
3. Review the Python source files to understand the event logic and analysis workflow.
4. Inspect the plots and result files provided with each project.
5. Follow the project-specific run instructions to reproduce the analysis.

## Skills Demonstrated

- Discrete-event system modeling and event scheduling
- Queueing and resource-allocation logic
- Simulation experiments and replication-based analysis
- Performance measurement and visualization
- Statistical estimation and confidence intervals
- Resource configuration and cost-based comparison
- Python programming and research-oriented documentation

---
