import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import random
import numpy as np
import pandas as pd
from algorithms import fcfs, sjf, priority_scheduling, round_robin

def random_process_set(num_processes):
    processes = []
    for i in range(num_processes):
        arrival = random.randint(0, 5)
        burst = random.randint(1, 10)
        priority = random.randint(1, 5)
        processes.append({'pid': i+1, 'arrival_time': arrival, 'burst_time': burst, 'priority': priority})
    return processes

def compute_avg_waiting(result):
    return np.mean([p['waiting_time'] for p in result])

def extract_features(processes):
    n = len(processes)
    burst = [p['burst_time'] for p in processes]
    arrival = [p['arrival_time'] for p in processes]
    priority = [p['priority'] for p in processes]
    return [
        n,
        np.mean(burst), np.std(burst),
        np.mean(arrival), np.std(arrival),
        np.mean(priority), np.std(priority),
        max(burst), min(burst),
        max(arrival), min(arrival),
    ]

def best_algorithm(processes, quantum=2):
    algos = {
        'FCFS': fcfs([p.copy() for p in processes]),
        'SJF': sjf([p.copy() for p in processes]),
        'Priority': priority_scheduling([p.copy() for p in processes]),
        'RR': round_robin([dict(p, remaining_time=p['burst_time'], response_time=-1) for p in processes], quantum)
    }
    avg_waits = {k: compute_avg_waiting(v) for k, v in algos.items()}
    return min(avg_waits, key=avg_waits.get)

records = []
for _ in range(2000):
    num = random.randint(3, 8)
    plist = random_process_set(num)
    label = best_algorithm(plist)
    feats = extract_features(plist)
    records.append(feats + [label])

columns = [
    "n", "mean_burst", "std_burst", "mean_arrival", "std_arrival",
    "mean_priority", "std_priority", "max_burst", "min_burst", "max_arrival", "min_arrival", "label"
]
df = pd.DataFrame(records, columns=columns)
df.to_csv("ml_models/scheduling_training_data.csv", index=False)
print("Training data generated and saved to ml_models/scheduling_training_data.csv")