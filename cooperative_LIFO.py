"""

Question:
Three processes with process IDs P1, P2, P3 with estimated completion time 
10, 5, 7 milliseconds respectively enter the ready queue together with the 
order P1, P2, P3 (Assume only P1 is present in the 'Ready' queue when the 
scheduler picks it up and P2, P3 entered the 'Ready' queue after that).

Now a new process P4 with estimated completion time 6ms enters the 'Ready'
queue after 5ms of scheduling P1.

"""

from collections import deque # double ended queue
import matplotlib.pyplot as plt

processes = [
    {"pid": "P2", "arrival_time": 0, "burst_time": 5},
    {"pid": "P3", "arrival_time": 0, "burst_time": 7},
    {"pid": "P4", "arrival_time": 5, "burst_time": 6},
    {"pid": "P1", "arrival_time": 0, "burst_time": 10},
]

def lifo_non_preemptive(processes):
    current_time = 0
    completed_processes = []
    ready_stack = deque()
    gantt_chart = []

    processes.sort(key=lambda x: x["arrival_time"])
    
    # Debug: Sorted process list
    print("\nProcesses sorted by arrival time:")
    for process in processes:
        print(process)

    while len(completed_processes) < len(processes):
        for process in processes:
            if process not in ready_stack and process not in completed_processes:
                if process["arrival_time"] <= current_time:
                    ready_stack.append(process)
                    # Debug
                    print(f"\nTime {current_time}: Process {process['pid']} added to ready stack.")

        if ready_stack:
            # Process execution
            current_process = ready_stack.pop()
            start_time = current_time
            current_time += current_process["burst_time"]
            
            gantt_chart.append((current_process["pid"], start_time, current_time))
            
            current_process["completion_time"] = current_time
            completed_processes.append(current_process)
        else:
            # Debug: Idle CPU
            print(f"\nTime {current_time}: CPU is idle.")
            current_time += 1

    for process in completed_processes:
        process["turnaround_time"] = process["completion_time"] - process["arrival_time"]
        process["waiting_time"] = process["turnaround_time"] - process["burst_time"]
    return completed_processes, gantt_chart

# LIFO scheduling
completed_processes, gantt_chart = lifo_non_preemptive(processes)

avg_tat = sum(p["turnaround_time"] for p in completed_processes) / len(completed_processes)
avg_wt = sum(p["waiting_time"] for p in completed_processes) / len(completed_processes)

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

def plot_gantt_chart(gantt_chart, processes):
    fig, ax = plt.subplots(figsize=(12, 6))

    for idx, (pid, start, end) in enumerate(gantt_chart):
        process = next(p for p in processes if p["pid"] == pid)
        tat = process["turnaround_time"]
        wt = process["waiting_time"]

        ax.barh(
            1, end - start, left=start, color="skyblue", edgecolor="black", height=0.4
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
        ax.text(
            (start + end) / 2,
            0.6,
            f"TAT={tat}, WT={wt}",
            ha="center",
            va="center",
            fontsize=10,
        )

    ax.set_yticks([1])
    ax.set_yticklabels(["CPU"])
    ax.set_xticks(range(0, max(end for _, _, end in gantt_chart) + 1))
    
    ax.set_xlabel("Time (ms)")
    ax.set_title("Gantt Chart - LIFO Non-Preemptive Scheduling")
    ax.grid(axis="x", linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.show()

# Plot the Gantt chart
plot_gantt_chart(gantt_chart, completed_processes)
