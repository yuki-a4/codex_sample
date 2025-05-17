import argparse
import json
from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

TASKS_FILE = Path('tasks.json')


def load_tasks(file_path: Path = TASKS_FILE):
    if file_path.exists():
        with open(file_path, 'r') as f:
            return json.load(f)
    return []


def save_tasks(tasks, file_path: Path = TASKS_FILE):
    with open(file_path, 'w') as f:
        json.dump(tasks, f, indent=2)


def add_task(args):
    tasks = load_tasks(Path(args.file))
    tasks.append({
        'name': args.name,
        'start': args.start,
        'deadline': args.deadline,
    })
    save_tasks(tasks, Path(args.file))
    print(f"Added task '{args.name}'")


def plot_gantt(args):
    tasks = load_tasks(Path(args.file))
    if not tasks:
        print('No tasks found.')
        return

    # Prepare data
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
    plt.savefig(args.output)
    print(f'Gantt chart saved to {args.output}')


def main():
    parser = argparse.ArgumentParser(description='Simple TODO app with Gantt chart')
    parser.add_argument('--file', default=str(TASKS_FILE), help='Tasks JSON file')
    subparsers = parser.add_subparsers(dest='command')

    add_p = subparsers.add_parser('add', help='Add a new task')
    add_p.add_argument('name', help='Task name')
    add_p.add_argument('start', help='Start date YYYY-MM-DD')
    add_p.add_argument('deadline', help='Deadline date YYYY-MM-DD')
    add_p.set_defaults(func=add_task)

    gantt_p = subparsers.add_parser('gantt', help='Generate Gantt chart')
    gantt_p.add_argument('output', help='Output image file')
    gantt_p.set_defaults(func=plot_gantt)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
