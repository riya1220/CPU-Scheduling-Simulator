import pickle
import numpy as np
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "best_scheduler_model.pkl")
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

def extract_features(processes):
    n = len(processes)
    burst = [p['burst_time'] for p in processes]
    arrival = [p['arrival_time'] for p in processes]
    priority = [p.get('priority', 1) for p in processes]
    return np.array([[
        n,
        np.mean(burst), np.std(burst),
        np.mean(arrival), np.std(arrival),
        np.mean(priority), np.std(priority),
        max(burst), min(burst),
        max(arrival), min(arrival),
    ]])

def predict_best_algorithm(processes):
    feats = extract_features(processes)
    predicted_algo = model.predict(feats)[0]

    # Extract features for explanation
    n = len(processes)
    burst = [p['burst_time'] for p in processes]
    arrival = [p['arrival_time'] for p in processes]
    priority = [p.get('priority', 1) for p in processes]

    mean_burst = np.mean(burst)
    std_burst = np.std(burst)
    mean_arrival = np.mean(arrival)
    std_arrival = np.std(arrival)
    mean_priority = np.mean(priority)
    std_priority = np.std(priority)

    # Generate explanations
    explanation = f"Number of Processes: {n}\n"
    if predicted_algo == 'FCFS':
        explanation += "FCFS works best when processes have similar burst times and arrival times, ensuring fairness."
    elif predicted_algo == 'SJF':
        explanation += f"SJF is ideal since burst times vary (Std Dev: {std_burst:.2f}), prioritizing shorter jobs first."
    elif predicted_algo == 'Priority':
        explanation += f"Priority Scheduling is suitable as priorities vary (Std Dev: {std_priority:.2f}), favoring high-priority processes."
    elif predicted_algo == 'RR':
        explanation += f"Round Robin is chosen because multiple processes ({n}) need fair CPU time with potential similar burst times."
    else:
        explanation += "No clear reason identified. Defaulting to FCFS."

    return predicted_algo, explanation
