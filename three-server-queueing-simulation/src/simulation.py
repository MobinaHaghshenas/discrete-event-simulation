
# ============================================================
# Three-Server Queueing System Simulation
# Discrete-Event Simulation using Python
#
# Simulation horizon: 8 hours (480 minutes)
# Number of replications: 1,000 / 2,000 / 4,000 / 6,000
#
# Outputs:
#   1. One comparison table for all replication counts
#   2. results_summary.csv
#   3. Four professional plots saved as PNG files
#   4. results.zip containing the CSV and plots
# ============================================================

import os
import heapq
import random
import itertools
import zipfile

import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display


# ------------------------------------------------------------
# 1. CONFIGURATION
# ------------------------------------------------------------

SIMULATION_HOURS = 8
SIMULATION_TIME = SIMULATION_HOURS * 60  # minutes

REPLICATION_COUNTS = [1000, 2000, 4000, 6000]

RANDOM_SEED = 2026

OUTPUT_DIR = "results"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Service-time ranges in minutes, inclusive.
SERVICE_TIME_RANGES = {
    1: (6, 15),
    2: (4, 16),
    3: (8, 14),
}

# Interarrival time range in minutes, inclusive.
INTERARRIVAL_TIME_RANGE = (2, 5)

SERVER_IDS = [1, 2, 3]


# ------------------------------------------------------------
# 2. SIMULATE ONE REPLICATION
# ------------------------------------------------------------

def simulate_one_replication(rng):
    """
    Simulate one replication of a three-server queueing system.

    Assumptions:
    - The first customer arrives at time 0.
    - Interarrival times are discrete uniform integers from 2 to 5.
    - Service times are discrete uniform integers within each
      server's specified service-time range.
    - Customers wait in one FIFO queue if all servers are busy.
    - An arriving customer selects randomly among idle servers.
    - Once a server completes service, it immediately serves the
      first waiting customer, if any.
    - No new arrivals are scheduled after the 480-minute horizon.
    - Customers already in the system are served until completion.
    - Utilization is measured only within [0, 480] minutes.

    Returns a dictionary containing statistics for this replication.
    """

    # Event format:
    # (event_time, priority, sequence_number, event_type,
    #  server_id, customer_id)
    #
    # Departure priority = 0
    # Arrival priority   = 1
    #
    # Thus, a departure at the same time as an arrival is processed
    # first. This makes a server completing service available before
    # the simultaneous arrival is handled.

    events = []
    event_sequence = itertools.count()

    def schedule_event(
        event_time,
        priority,
        event_type,
        server_id=None,
        customer_id=None
    ):
        heapq.heappush(
            events,
            (
                event_time,
                priority,
                next(event_sequence),
                event_type,
                server_id,
                customer_id,
            ),
        )

    # FIFO queue of customer IDs.
    waiting_queue = []

    # Server state: True means busy, False means idle.
    server_busy = {server_id: False for server_id in SERVER_IDS}

    # Customer information.
    customer_arrival_time = {}
    customer_service_start = {}

    # Statistics.
    total_arrivals = 0
    max_queue_length = 0

    total_waiting_time = 0.0
    total_time_in_system = 0.0

    number_served = {server_id: 0 for server_id in SERVER_IDS}
    busy_time_within_horizon = {
        server_id: 0.0 for server_id in SERVER_IDS
    }

    # Customer IDs start at 1.
    next_customer_id = 1

    # Schedule the first arrival at time zero.
    schedule_event(
        event_time=0,
        priority=1,
        event_type="arrival",
        customer_id=next_customer_id,
    )

    def start_service(server_id, customer_id, current_time):
        """
        Start service for a customer on a specified server.
        """

        service_start_time = current_time

        service_min, service_max = SERVICE_TIME_RANGES[server_id]
        service_duration = rng.randint(service_min, service_max)

        service_end_time = service_start_time + service_duration

        customer_service_start[customer_id] = service_start_time

        # Count the service assignment.
        number_served[server_id] += 1

        # Count only the portion of busy time inside the 8-hour
        # observation window.
        busy_overlap = max(
            0.0,
            min(service_end_time, SIMULATION_TIME)
            - min(service_start_time, SIMULATION_TIME),
        )

        busy_time_within_horizon[server_id] += busy_overlap

        server_busy[server_id] = True

        # Schedule the service-completion event.
        schedule_event(
            event_time=service_end_time,
            priority=0,
            event_type="departure",
            server_id=server_id,
            customer_id=customer_id,
        )

    # --------------------------------------------------------
    # Main discrete-event loop
    # --------------------------------------------------------

    while events:

        (
            current_time,
            priority,
            sequence_number,
            event_type,
            server_id,
            customer_id,
        ) = heapq.heappop(events)

        # ----------------------------
        # ARRIVAL EVENT
        # ----------------------------

        if event_type == "arrival":

            customer_arrival_time[customer_id] = current_time
            total_arrivals += 1

            # Schedule the next arrival only if it occurs within
            # the 8-hour arrival window.
            interarrival_min, interarrival_max = (
                INTERARRIVAL_TIME_RANGE
            )

            interarrival_time = rng.randint(
                interarrival_min,
                interarrival_max,
            )

            next_arrival_time = current_time + interarrival_time

            if next_arrival_time <= SIMULATION_TIME:

                next_customer_id += 1

                schedule_event(
                    event_time=next_arrival_time,
                    priority=1,
                    event_type="arrival",
                    customer_id=next_customer_id,
                )

            # Identify all currently idle servers.
            idle_servers = [
                sid
                for sid in SERVER_IDS
                if not server_busy[sid]
            ]

            if idle_servers:
                # Choose randomly among available servers.
                selected_server = rng.choice(idle_servers)

                start_service(
                    server_id=selected_server,
                    customer_id=customer_id,
                    current_time=current_time,
                )

            else:
                # All servers are busy: join the FIFO queue.
                waiting_queue.append(customer_id)

                max_queue_length = max(
                    max_queue_length,
                    len(waiting_queue),
                )

        # ----------------------------
        # DEPARTURE / SERVICE COMPLETION
        # ----------------------------

        elif event_type == "departure":

            arrival_time = customer_arrival_time[customer_id]
            service_start_time = customer_service_start[customer_id]

            waiting_time = service_start_time - arrival_time
            time_in_system = current_time - arrival_time

            total_waiting_time += waiting_time
            total_time_in_system += time_in_system

            # If customers are waiting, this server immediately
            # starts serving the first customer in the FIFO queue.
            if waiting_queue:

                next_waiting_customer = waiting_queue.pop(0)

                start_service(
                    server_id=server_id,
                    customer_id=next_waiting_customer,
                    current_time=current_time,
                )

            else:
                # No waiting customers: the server becomes idle.
                server_busy[server_id] = False

    # --------------------------------------------------------
    # Calculate statistics for this replication
    # --------------------------------------------------------

    average_waiting_time = total_waiting_time / total_arrivals

    average_time_in_system = (
        total_time_in_system / total_arrivals
    )

    utilization_percent = {
        sid: (
            busy_time_within_horizon[sid]
            / SIMULATION_TIME
            * 100.0
        )
        for sid in SERVER_IDS
    }

    result = {
        "total_arrivals": total_arrivals,
        "average_waiting_time_min": average_waiting_time,
        "average_time_in_system_min": average_time_in_system,
        "maximum_queue_length": max_queue_length,
    }

    for sid in SERVER_IDS:
        result[f"customers_served_server_{sid}"] = number_served[sid]
        result[f"utilization_server_{sid}_percent"] = (
            utilization_percent[sid]
        )

    return result


# ------------------------------------------------------------
# 3. RUN THE EXPERIMENT
# ------------------------------------------------------------

print("=" * 72)
print("THREE-SERVER QUEUEING SYSTEM SIMULATION")
print("=" * 72)

print(f"Simulation horizon: {SIMULATION_HOURS} hours")
print(f"Observation window: {SIMULATION_TIME} minutes")
print(f"Replication counts: {REPLICATION_COUNTS}")
print(f"Random seed: {RANDOM_SEED}")
print()

# Generate one reproducible sequence of independent replication seeds.
master_rng = random.Random(RANDOM_SEED)

max_replications = max(REPLICATION_COUNTS)

replication_seeds = [
    master_rng.getrandbits(64)
    for _ in range(max_replications)
]

replication_results = []

for replication_index, replication_seed in enumerate(
    replication_seeds,
    start=1,
):
    replication_rng = random.Random(replication_seed)

    one_result = simulate_one_replication(replication_rng)

    replication_results.append(one_result)

    if replication_index % 1000 == 0:
        print(
            f"Completed {replication_index:,} "
            f"of {max_replications:,} replications."
        )

raw_results = pd.DataFrame(replication_results)

print("\nAll replications completed successfully.")


# ------------------------------------------------------------
# 4. BUILD ONE COMPARISON TABLE
# ------------------------------------------------------------

# Every column is one experimental case.
# Every row is one performance measure.
#
# The 1,000-replication case uses the first 1,000 replications;
# the 2,000 case uses the first 2,000, and so on.
# This nested-prefix design makes the cases directly comparable.

metrics = [
    (
        "Average waiting time (minutes)",
        "average_waiting_time_min",
    ),
    (
        "Average time in system (minutes)",
        "average_time_in_system_min",
    ),
    (
        "Average total arrivals",
        "total_arrivals",
    ),
    (
        "Average maximum queue length",
        "maximum_queue_length",
    ),
    (
        "Average customers served - Server 1",
        "customers_served_server_1",
    ),
    (
        "Average customers served - Server 2",
        "customers_served_server_2",
    ),
    (
        "Average customers served - Server 3",
        "customers_served_server_3",
    ),
    (
        "Server 1 utilization (%)",
        "utilization_server_1_percent",
    ),
    (
        "Server 2 utilization (%)",
        "utilization_server_2_percent",
    ),
    (
        "Server 3 utilization (%)",
        "utilization_server_3_percent",
    ),
]

comparison_data = {}

for replication_count in REPLICATION_COUNTS:

    subset = raw_results.iloc[:replication_count]

    case_name = f"N = {replication_count:,}"

    comparison_data[case_name] = [
        subset[column_name].mean()
        for metric_name, column_name in metrics
    ]

comparison_table = pd.DataFrame(
    comparison_data,
    index=[metric_name for metric_name, _ in metrics],
)

comparison_table.index.name = "Performance measure"

# Display the one consolidated comparison table.
print("\n" + "=" * 72)
print("FINAL COMPARISON TABLE")
print("=" * 72)

display(comparison_table.round(4))

# Save the same comparison table as a CSV file.
csv_path = os.path.join(
    OUTPUT_DIR,
    "results_summary.csv",
)

comparison_table.round(8).to_csv(
    csv_path,
    encoding="utf-8-sig",
)


# ------------------------------------------------------------
# 5. PREPARE CONVERGENCE DATA
# ------------------------------------------------------------

# Cumulative means help show how estimates change as the number
# of replications increases.

cumulative_data = pd.DataFrame()

for metric_name, column_name in metrics:
    cumulative_data[metric_name] = (
        raw_results[column_name].expanding().mean()
    )

cumulative_data.insert(
    0,
    "replication",
    range(1, len(raw_results) + 1),
)


# ------------------------------------------------------------
# 6. GRAPH 1: AVERAGE WAITING TIME CONVERGENCE
# ------------------------------------------------------------

plt.figure(figsize=(10, 5))

plt.plot(
    cumulative_data["replication"],
    cumulative_data["Average waiting time (minutes)"],
)

plt.title("Convergence of Average Waiting Time")
plt.xlabel("Number of replications")
plt.ylabel("Average waiting time (minutes)")
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig(
    os.path.join(OUTPUT_DIR, "waiting_time_convergence.png"),
    dpi=300,
    bbox_inches="tight",
)

plt.show()


# ------------------------------------------------------------
# 7. GRAPH 2: AVERAGE TIME IN SYSTEM CONVERGENCE
# ------------------------------------------------------------

plt.figure(figsize=(10, 5))

plt.plot(
    cumulative_data["replication"],
    cumulative_data["Average time in system (minutes)"],
)

plt.title("Convergence of Average Time in System")
plt.xlabel("Number of replications")
plt.ylabel("Average time in system (minutes)")
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig(
    os.path.join(OUTPUT_DIR, "time_in_system_convergence.png"),
    dpi=300,
    bbox_inches="tight",
)

plt.show()


# ------------------------------------------------------------
# GRAPH 3: SERVER UTILIZATION COMPARISON
# ------------------------------------------------------------

utilization_columns = [
    "Server 1 utilization (%)",
    "Server 2 utilization (%)",
    "Server 3 utilization (%)",
]

utilization_labels = [
    "Server 1",
    "Server 2",
    "Server 3",
]

plt.figure(figsize=(9, 5))

for column_name, label in zip(
    utilization_columns,
    utilization_labels,
):
    plt.plot(
        cumulative_data["replication"],
        cumulative_data[column_name],
        label=label,
    )

plt.title("Convergence of Server Utilization")
plt.xlabel("Number of replications")
plt.ylabel("Utilization (%)")
plt.ylim(0, 100)
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "server_utilization_convergence.png"
    ),
    dpi=300,
    bbox_inches="tight",
)

plt.show()



# ------------------------------------------------------------
# 9. GRAPH 4: CUSTOMERS SERVED BY EACH SERVER
# ------------------------------------------------------------

served_columns = [
    "customers_served_server_1",
    "customers_served_server_2",
    "customers_served_server_3",
]

served_labels = [
    "Server 1",
    "Server 2",
    "Server 3",
]

mean_served = [
    raw_results[column_name].mean()
    for column_name in served_columns
]

plt.figure(figsize=(8, 5))

plt.bar(
    served_labels,
    mean_served,
)

plt.title("Average Customers Served by Each Server")
plt.xlabel("Server")
plt.ylabel("Average customers served per replication")
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()

plt.savefig(
    os.path.join(OUTPUT_DIR, "customers_served_by_server.png"),
    dpi=300,
    bbox_inches="tight",
)

plt.show()


# ------------------------------------------------------------
# 10. EXPORT ALL RESULTS
# ------------------------------------------------------------

# Save the replication-level data as an additional audit file.
# This file is optional for publication but useful for validation.

raw_results_path = os.path.join(
    OUTPUT_DIR,
    "replication_level_results.csv",
)

raw_results.to_csv(
    raw_results_path,
    index_label="replication",
    encoding="utf-8-sig",
)

# Save cumulative estimates to allow convergence analysis later.
convergence_path = os.path.join(
    OUTPUT_DIR,
    "convergence_data.csv",
)

cumulative_data.to_csv(
    convergence_path,
    index=False,
    encoding="utf-8-sig",
)

# Package the main comparison table, raw results, convergence data,
# and figures into one ZIP archive.

zip_path = "results.zip"

with zipfile.ZipFile(
    zip_path,
    mode="w",
    compression=zipfile.ZIP_DEFLATED,
) as zip_file:

    for filename in os.listdir(OUTPUT_DIR):
        file_path = os.path.join(OUTPUT_DIR, filename)

        if os.path.isfile(file_path):
            zip_file.write(
                file_path,
                arcname=os.path.join("results", filename),
            )

print("\n" + "=" * 72)
print("OUTPUT FILES")
print("=" * 72)

for filename in sorted(os.listdir(OUTPUT_DIR)):
    print(f"- {os.path.join(OUTPUT_DIR, filename)}")

print(f"- {zip_path}")

print("\nSimulation finished.")
