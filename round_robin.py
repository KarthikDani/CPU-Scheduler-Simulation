from collections import deque
import matplotlib.pyplot as plt

# Define the processes
processes = [
    {"pid": "P1", "arrival_time": 0, "burst_time": 10},
    {"pid": "P2", "arrival_time": 0, "burst_time": 5},
    {"pid": "P3", "arrival_time": 0, "burst_time": 8},
]

time_quantum = 2

# Round Robin implementation
def round_robin(processes, time_quantum):
    current_time = 0
    ready_queue = deque()
    gantt_chart = []
    completed_processes = []
    remaining_burst = {p["pid"]: p["burst_time"] for p in processes}

    processes.sort(key=lambda x: x["arrival_time"])  # Sort by arrival time

    while len(completed_processes) < len(processes):
        # Add processes to the ready queue if they arrive
        for process in processes:
            if (
                process["arrival_time"] <= current_time
                and process not in ready_queue
                and process not in completed_processes
            ):
                ready_queue.append(process)
                # Debug
                print(f"Time {current_time}: Process {process['pid']} added to the ready queue.")

        if ready_queue:
            # Select the first process in the queue
            current_process = ready_queue.popleft()
            start_time = current_time
            exec_time = min(remaining_burst[current_process["pid"]], time_quantum)
            current_time += exec_time
            remaining_burst[current_process["pid"]] -= exec_time

            gantt_chart.append((current_process["pid"], start_time, current_time))

            # Process completion check
            if remaining_burst[current_process["pid"]] == 0:
                current_process["completion_time"] = current_time
                completed_processes.append(current_process)
                # Debug
                print(f"Time {current_time}: Process {current_process['pid']} completed.")
            else:
                ready_queue.append(current_process)  # Re-add to the queue if not finished
        else:
            # CPU idle time
            print(f"Time {current_time}: CPU is idle.")
            current_time += 1

    for process in completed_processes:
        process["turnaround_time"] = process["completion_time"] - process["arrival_time"]
        process["waiting_time"] = process["turnaround_time"] - process["burst_time"]
    return completed_processes, gantt_chart

# Round Robin scheduling
completed_processes, gantt_chart = round_robin(processes, time_quantum)

# Calculate average times
avg_tat = sum(p["turnaround_time"] for p in completed_processes) / len(completed_processes)
avg_wt = sum(p["waiting_time"] for p in completed_processes) / len(completed_processes)

# Print process details
print("\nProcess Details:")
print(
    "{:<5} {:<10} {:<10} {:<15} {:<15} {:<15}".format(
        "PID", "Arrival", "Burst", "Completion", "Turnaround", "Waiting"
    )
)
for process in completed_processes:
    print(
        "{:<5} {:<10} {:<10} {:<15} {:<15} {:<15}".format(
            process["pid"],
            process["arrival_time"],
            process["burst_time"],
            process["completion_time"],
            process["turnaround_time"],
            process["waiting_time"],
        )
    )

print(f"\nAverage Turnaround Time: {avg_tat:.2f}")
print(f"Average Waiting Time: {avg_wt:.2f}")

# Gantt chart plotting
def plot_gantt_chart_rr(gantt_chart):
    fig, ax = plt.subplots(figsize=(12, 6))

    for idx, (pid, start, end) in enumerate(gantt_chart):
        ax.barh(
            1, end - start, left=start, color="lightgreen", edgecolor="black", height=0.4
        )
        ax.text(
            (start + end) / 2,
            1,
            pid,
            ha="center",
            va="center",
            color="black",
            fontsize=12,
        )
        ax.text(start, 1.05, f"{start}", ha="center", va="bottom", fontsize=10)
        ax.text(end, 1.05, f"{end}", ha="center", va="bottom", fontsize=10)

    ax.set_yticks([1])
    ax.set_yticklabels(["CPU"])
    ax.set_xticks(range(0, max(end for _, _, end in gantt_chart) + 1))
    ax.set_xlabel("Time (ms)")
    ax.set_title(f"Gantt Chart - Round Robin Scheduling (Time Quantum = {time_quantum} ms)")
    ax.grid(axis="x", linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.show()

# Plot the Gantt chart
plot_gantt_chart_rr(gantt_chart)