from flask import Flask, render_template, request, jsonify
from algorithms import fcfs, sjf, priority_scheduling, round_robin
from ml_models.model_predictor import predict_best_algorithm

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run', methods=['POST'])
def run_scheduler():
    data = request.get_json()
    processes = data['processes']
    algo = data['algorithm']
    quantum = data.get('quantum', 2)

    for p in processes:
        p['response_time'] = -1
        p['remaining_time'] = p['burst_time']

    if algo == 'FCFS':
        result = fcfs(processes)
    elif algo == 'SJF':
        result = sjf(processes)
    elif algo == 'Priority':
        result = priority_scheduling(processes)
    elif algo == 'RR':
        result = round_robin(processes, quantum)
    else:
        return jsonify([])

    return jsonify(result)

@app.route('/suggest', methods=['POST'])
def suggest_algorithm():
    data = request.json
    processes = data['processes']
    suggested_algorithm, explanation = predict_best_algorithm(processes)
    return jsonify({'suggested_algorithm': suggested_algorithm, 'explanation': explanation})


if __name__ == '__main__':
    app.run(debug=True)