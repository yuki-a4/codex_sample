from flask import Flask, render_template_string, request, redirect, send_file
import json
from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import io

TASKS_FILE = Path('tasks.json')

app = Flask(__name__)

def load_tasks(file_path: Path = TASKS_FILE):
    if file_path.exists():
        with open(file_path, 'r') as f:
            return json.load(f)
    return []

def save_tasks(tasks, file_path: Path = TASKS_FILE):
    with open(file_path, 'w') as f:
        json.dump(tasks, f, indent=2)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        start = request.form['start']
        deadline = request.form['deadline']
        tasks = load_tasks()
        tasks.append({'name': name, 'start': start, 'deadline': deadline})
        save_tasks(tasks)
        return redirect('/')
    tasks = load_tasks()
    html = '''
    <h1>TODO List</h1>
    <form method="post">
      Task: <input name="name" required>
      Start: <input name="start" type="date" required>
      Deadline: <input name="deadline" type="date" required>
      <input type="submit" value="Add">
    </form>
    <ul>
    {% for t in tasks %}
      <li>{{ t.name }} ({{ t.start }} - {{ t.deadline }})</li>
    {% endfor %}
    </ul>
    <p><a href="/gantt">View Gantt chart</a></p>
    '''
    return render_template_string(html, tasks=tasks)

@app.route('/gantt')
def gantt():
    tasks = load_tasks()
    if not tasks:
        return 'No tasks found.'

    starts = [datetime.strptime(t['start'], '%Y-%m-%d') for t in tasks]
    ends = [datetime.strptime(t['deadline'], '%Y-%m-%d') for t in tasks]
    durations = [(e - s).days for s, e in zip(starts, ends)]
    names = [t['name'] for t in tasks]

    fig, ax = plt.subplots(figsize=(8, 0.5 * len(tasks)))
    ax.barh(range(len(tasks)), durations, left=mdates.date2num(starts), height=0.4)
    ax.set_yticks(range(len(tasks)))
    ax.set_yticklabels(names)
    ax.xaxis_date()
    ax.set_xlabel('Date')
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

if __name__ == '__main__':
    app.run()
