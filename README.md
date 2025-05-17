# codex_sample

This repository contains a minimal TODO application that can store tasks with deadlines and generate a simple Gantt chart. A small Flask web interface is also included.

## Requirements

- Python 3
- matplotlib (`pip install matplotlib`)
- Flask (`pip install flask`)

## CLI Usage

Add tasks specifying a start date and a deadline:

```bash
python todo.py add "Write report" 2023-12-01 2023-12-05
```

Tasks are saved in `tasks.json` by default. You can specify a custom file with `--file`.

Generate a Gantt chart showing all tasks:

```bash
python todo.py gantt chart.png
```

This will create `chart.png` containing a horizontal bar chart of your tasks.

## Web Usage

Run the Flask app and open `http://localhost:5000` in your browser:

```bash
python webapp.py
```

You can add tasks through the form and view the Gantt chart via the link on the page.
