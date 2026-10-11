# Three-Server Queueing System Simulation

A Python-based discrete-event simulation of a queueing system with three parallel service stations. The project studies customer arrivals, waiting-line behavior, server workload, and system performance over an eight-hour operating period. It also compares the stability of estimated performance measures across 1,000, 2,000, 4,000, and 6,000 independent replications.

## Project overview

Customers arrive at a system with three servers. If one or more servers are idle, an arriving customer is assigned randomly to one of the available servers. If all servers are busy, the customer joins a shared first-in, first-out (FIFO) waiting queue. When a service finishes, the server immediately takes the first waiting customer, if one is available.

The model is implemented as a discrete-event simulation: the simulation clock advances from one scheduled arrival or service-completion event to the next, rather than advancing minute by minute.

## Model assumptions and input parameters

| Parameter | Specification |
|---|---|
| Number of servers | 3 parallel servers |
| Observation / arrival horizon | 8 hours (480 minutes) |
| First arrival | At simulation time 0 |
| Interarrival time | Discrete uniform integer from 2 to 5 minutes, inclusive |
| Server 1 service time | Discrete uniform integer from 6 to 15 minutes, inclusive |
| Server 2 service time | Discrete uniform integer from 4 to 16 minutes, inclusive |
| Server 3 service time | Discrete uniform integer from 8 to 14 minutes, inclusive |
| Queue discipline | One shared FIFO queue |
| Server selection | Random selection among currently idle servers |
| Replication counts compared | 1,000; 2,000; 4,000; 6,000 |
| Random seed | 2026 |

**End-of-horizon rule:** no new arrivals are scheduled after minute 480. Customers who arrived by the end of the arrival window are still allowed to finish service after minute 480. Server utilization is calculated only over the 480-minute observation window.

When an arrival and a service completion occur at the same simulation time, the service-completion event is processed first. This makes the newly available server eligible for the simultaneous arrival.

## Performance measures

For each replication, the simulation records:

- Total number of customer arrivals during the arrival window.
- Average customer waiting time before service, in minutes.
- Average time in the system, from arrival until service completion, in minutes.
- Maximum length of the waiting queue.
- Number of customers assigned to each server.
- Utilization percentage of each server during the 480-minute observation window.

The experiment aggregates these measures across replications. It also records replication-level results and cumulative averages to help inspect convergence as the number of replications increases.

## Results

The following values are the results obtained from the current run of the simulation. Each column uses the first *N* replications from the same reproducible sequence, so the four cases are nested and directly comparable.

| Performance measure | 1,000 replications | 2,000 replications | 4,000 replications | 6,000 replications |
|---|---:|---:|---:|---:|
| Average waiting time (minutes) | 8.0568 | 8.0982 | 8.1473 | 8.1675 |
| Average time in system (minutes) | 18.5486 | 18.5853 | 18.6360 | 18.6537 |
| Average arrivals per replication | 137.6420 | 137.7360 | 137.7832 | 137.8477 |
| Average maximum queue length | 6.2730 | 6.2910 | 6.3398 | 6.3437 |
| Average customers assigned to Server 1 | 45.8020 | 45.8570 | 45.8757 | 45.8867 |
| Average customers assigned to Server 2 | 47.9490 | 48.0220 | 48.0182 | 48.0695 |
| Average customers assigned to Server 3 | 43.8910 | 43.8570 | 43.8892 | 43.8915 |
| Server 1 utilization (%) | 96.4371 | 96.4599 | 96.4920 | 96.5035 |
| Server 2 utilization (%) | 96.2181 | 96.2369 | 96.2237 | 96.2363 |
| Server 3 utilization (%) | 96.7240 | 96.7484 | 96.7546 | 96.7541 |

### Initial interpretation

In the 6,000-replication case, the estimated average waiting time is approximately **8.17 minutes**, while the average time in the system is approximately **18.65 minutes**. Estimated server utilization is around **96% for all three servers** under the specified assumptions. The reported estimates change modestly as the replication count increases; the convergence plots provide a visual check of that behavior.

These are simulation estimates for this model and its assumptions, not universal queueing-system performance guarantees.

## Visualizations and output files

The script is designed to generate the following outputs in a `results/` directory:

| File | Purpose |
|---|---|
| `results_summary.csv` | Consolidated comparison of the four replication counts |
| `waiting_time_convergence.png` | Cumulative average waiting time as replications increase |
| `time_in_system_convergence.png` | Cumulative average time in the system as replications increase |
| `server_utilization_convergence.png` | Cumulative utilization estimates for the three servers |
| `customers_served_by_server.png` | Average number of customers assigned to each server |
| `replication_level_results.csv` | Results for each individual replication |
| `convergence_data.csv` | Cumulative-average data used by the convergence plots |
| `results.zip` | ZIP archive of the generated result files |

The project also includes the model diagrams and editable Visio materials supplied with the project, which document the conceptual model and the main simulation events.

## Project structure

```text
three-server-queueing-simulation/
├── README.md
├── src/
│   └── simulation.py
├── results/
│   ├── results_summary.csv
│   ├── replication_level_results.csv
│   ├── convergence_data.csv
│   └── *.png
└── model diagrams and editable Visio files
```

The exact set of generated output files depends on whether the simulation has been run and all output artifacts have been committed to the repository.

## How to run

### Option 1: Google Colab

1. Open [Google Colab](https://colab.research.google.com/).
2. Upload or open `src/simulation.py` in the notebook environment.
3. Run the script in a notebook cell. If needed, install the dependencies first:

   ```python
   %pip install pandas matplotlib
   ```

4. After execution, inspect the comparison table and plots. The script writes output files to `results/` and creates `results.zip` in the current working directory.

### Option 2: Local Python environment

Use Python 3.9 or later with `pandas` and `matplotlib` installed. The script also imports `IPython.display` to display the comparison table; this is available in Jupyter and Colab environments.

From the repository root, run:

```bash
python -m pip install pandas matplotlib ipython
python src/simulation.py
```

If running outside a notebook, the simulation and files can still be generated; the table display may depend on the environment.

## Implementation notes

- A priority queue implemented with Python's `heapq` stores future events.
- A monotonically increasing sequence number provides deterministic event ordering when event times and priorities match.
- Each replication uses its own pseudo-random generator, seeded from a master generator initialized with `2026`, making the experiment reproducible.
- The four reported replication counts are cumulative prefixes of the same 6,000-replication experiment, rather than four unrelated experiments.
- Service-time ranges and the interarrival-time range are inclusive integer ranges.

## Limitations

The results depend on the chosen arrival and service-time distributions, the random server-selection rule, the FIFO discipline, and the eight-hour arrival horizon. The model does not represent additional real-world factors such as server breaks, customer abandonment, priorities, or variable staffing. Those features would need to be explicitly added before applying the results to an operational setting.

## Technologies

- Python
- Discrete-event simulation
- `heapq` and `random` for event scheduling and random sampling
- pandas for result aggregation and CSV export
- Matplotlib for plots
