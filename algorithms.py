from collections import deque

def fcfs(processes):
    processes.sort(key=lambda p: p['arrival_time'])
    current_time = 0
    for p in processes:
        if current_time < p['arrival_time']:
            current_time = p['arrival_time']
        p['response_time'] = current_time - p['arrival_time']
        p['waiting_time'] = current_time - p['arrival_time']
        current_time += p['burst_time']
        p['completion_time'] = current_time
        p['turnaround_time'] = p['completion_time'] - p['arrival_time']
    return processes

def sjf(processes):
    processes.sort(key=lambda p: (p['arrival_time'], p['burst_time']))
    time, completed, n = 0, 0, len(processes)
    visited = [False] * n
    while completed < n:
        idx = -1
        min_bt = float('inf')
        for i in range(n):
            if not visited[i] and processes[i]['arrival_time'] <= time and processes[i]['burst_time'] < min_bt:
                min_bt = processes[i]['burst_time']
                idx = i
        if idx == -1:
            time += 1
            continue
        p = processes[idx]
        p['response_time'] = time - p['arrival_time']
        p['waiting_time'] = time - p['arrival_time']
        time += p['burst_time']
        p['completion_time'] = time
        p['turnaround_time'] = p['completion_time'] - p['arrival_time']
        visited[idx] = True
        completed += 1
    return processes

def priority_scheduling(processes):
    processes.sort(key=lambda p: (p['arrival_time'], p['priority']))
    time, completed = 0, 0
    n = len(processes)
    visited = [False] * n

    while completed < n:
        idx = -1
        min_prio = float('inf')
        for i in range(n):
            if not visited[i] and processes[i]['arrival_time'] <= time and processes[i]['priority'] < min_prio:
                idx = i
                min_prio = processes[i]['priority']
        if idx == -1:
            time += 1
            continue
        p = processes[idx]
        p['response_time'] = time - p['arrival_time']
        p['waiting_time'] = time - p['arrival_time']
        time += p['burst_time']
        p['completion_time'] = time
        p['turnaround_time'] = p['completion_time'] - p['arrival_time']
        visited[idx] = True
        completed += 1
    return processes

def round_robin(processes, quantum):
    time = 0
    queue = deque()
    index = 0
    n = len(processes)
    completed = 0

    while completed < n:
        while index < n and processes[index]['arrival_time'] <= time:
            queue.append(processes[index])
            index += 1

        if queue:
            p = queue.popleft()
            if p['response_time'] == -1:
                p['response_time'] = time - p['arrival_time']

            exec_time = min(quantum, p['remaining_time'])
            time += exec_time
            p['remaining_time'] -= exec_time

            while index < n and processes[index]['arrival_time'] <= time:
                queue.append(processes[index])
                index += 1

            if p['remaining_time'] > 0:
                queue.append(p)
            else:
                p['completion_time'] = time
                p['turnaround_time'] = p['completion_time'] - p['arrival_time']
                p['waiting_time'] = p['turnaround_time'] - p['burst_time']
                completed += 1
        else:
            time += 1
    return processes