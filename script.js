let processes = [];
let pidCounter = 1;

const algorithmSelect = document.getElementById('algorithm');
const quantumDiv = document.getElementById('quantumInput');
const priorityHeader = document.querySelector('.priority-header');

algorithmSelect.addEventListener('change', () => {
  const algo = algorithmSelect.value;
  quantumDiv.classList.toggle('d-none', algo !== 'RR');
  priorityHeader.classList.toggle('d-none', algo !== 'Priority');
  document.querySelectorAll('.prio').forEach(input =>
    input.closest('td').classList.toggle('d-none', algo !== 'Priority')
  );
});

function addProcess() {
  const tbody = document.querySelector("#processTable tbody");
  const row = document.createElement('tr');
  row.innerHTML = `
    <td>${pidCounter}</td>
    <td><input type="number" value="0" class="form-control at" min="0" /></td>
    <td><input type="number" value="1" class="form-control bt" min="1" /></td>
    <td class="${algorithmSelect.value !== 'Priority' ? 'd-none' : ''}"><input type="number" value="1" class="form-control prio" min="1" /></td>
  `;
  row.classList.add("animate__animated", "animate__fadeIn", "new-highlight");
  setTimeout(() => row.classList.remove("new-highlight"), 2000);
  tbody.appendChild(row);
  row.querySelector("input").focus();
  pidCounter++;
}

document.getElementById('addProcessBtn').addEventListener('click', addProcess);
addProcess();

document.getElementById("schedulerForm").addEventListener("submit", async function(e) {
  e.preventDefault();
  let algorithm = algorithmSelect.value;
  let quantum = parseInt(document.getElementById("quantum").value) || 0;
  let rows = document.querySelectorAll("#processTable tbody tr");
  processes = [];

  for (let i = 0; i < rows.length; i++) {
    let inputs = rows[i].querySelectorAll("input");
    let arrival_time = parseInt(inputs[0].value);
    let burst_time = parseInt(inputs[1].value);
    let priority = algorithm === 'Priority' ? parseInt(inputs[2].value) : 1;

    if (isNaN(arrival_time) || arrival_time < 0 || isNaN(burst_time) || burst_time <= 0 || (algorithm === 'Priority' && (isNaN(priority) || priority <= 0))) {
      alert(`Please enter valid values for Process ${i + 1}`);
      return;
    }

    processes.push({ pid: i + 1, arrival_time, burst_time, priority });
  }

  if (processes.length === 0) {
    alert("Please add at least one process.");
    return;
  }

  try {
    const response = await fetch("/run", {
      method: "POST",
      body: JSON.stringify({ processes, algorithm, quantum }),
      headers: { "Content-Type": "application/json" }
    });
    if (!response.ok) throw new Error("Server error");
    const result = await response.json();
    displayResults(result);
  } catch (error) {
    alert("Error: " + error.message);
  }
});

function displayResults(data) {
  const output = document.getElementById("output");
  output.innerHTML = `<h3>Results</h3>
    <table class="table table-bordered">
    <thead><tr><th>PID</th><th>Completion Time</th><th>Turnaround Time</th><th>Waiting Time</th><th>Response Time</th></tr></thead>
    <tbody>
    ${data.map(p => `<tr>
      <td>${p.pid}</td>
      <td>${p.completion_time}</td>
      <td>${p.turnaround_time}</td>
      <td>${p.waiting_time}</td>
      <td>${p.response_time}</td>
    </tr>`).join('')}
    </tbody>
    </table>`;
  drawGanttChart(data);
}

function drawGanttChart(data) {
  const canvas = document.getElementById('ganttChart');
  const ctx = canvas.getContext('2d');
  canvas.width = 800;
  canvas.height = 100;
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  const colors = ['#4CAF50', '#2196F3', '#FFC107', '#E91E63', '#9C27B0', '#00BCD4'];
  const startX = 50;
  const blockHeight = 40;
  const scale = 30;
  let currentX = startX;

  data.forEach((p, i) => {
    const startTime = p.start_time ?? (i === 0 ? 0 : (data[i-1].completion_time || 0));
    const width = (p.completion_time - startTime) * scale;

    ctx.fillStyle = colors[i % colors.length];
    ctx.fillRect(currentX, 30, width, blockHeight);
    ctx.strokeRect(currentX, 30, width, blockHeight);

    ctx.fillStyle = '#fff';
    ctx.font = '16px Arial';
    ctx.fillText(`P${p.pid}`, currentX + width / 3, 55);

    ctx.fillStyle = '#000';
    ctx.fillText(startTime, currentX - 10, 80);

    currentX += width;
  });

  ctx.fillText(data[data.length - 1].completion_time, currentX - 10, 80);
}

// Suggestion functionality
document.getElementById("suggestBtn").addEventListener("click", async function(e) {
  e.preventDefault();
  let rows = document.querySelectorAll("#processTable tbody tr");
  let tempProcesses = [];
  for (let i = 0; i < rows.length; i++) {
    let inputs = rows[i].querySelectorAll("input");
    let arrival_time = parseInt(inputs[0].value);
    let burst_time = parseInt(inputs[1].value);
    let priority = algorithmSelect.value === 'Priority' ? parseInt(inputs[2].value) : 1;
    if (isNaN(arrival_time) || arrival_time < 0 || isNaN(burst_time) || burst_time <= 0 || (algorithmSelect.value === 'Priority' && (isNaN(priority) || priority <= 0))) {
      alert(`Please enter valid values for Process ${i + 1}`);
      return;
    }
    tempProcesses.push({ pid: i + 1, arrival_time, burst_time, priority });
  }
  if (tempProcesses.length === 0) {
    alert("Please add at least one process.");
    return;
  }
  try {
    const res = await fetch("/suggest", {
      method: "POST",
      body: JSON.stringify({ processes: tempProcesses }),
      headers: { "Content-Type": "application/json" }
    });
    const data = await res.json();
    document.getElementById("suggestionOutput").innerHTML = `
      <b>Suggested Best Algorithm:</b> ${data.suggested_algorithm}<br/>
      <b>Reason:</b> ${data.explanation.replace(/\n/g, "<br/>")}
    `;
  } catch (error) {
    alert("Unable to suggest algorithm: " + error.message);
  }
});
