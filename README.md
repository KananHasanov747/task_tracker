# Task CLI app

Task Tracker CLI is a feature that allows to add, update, mark, and delete task in JSON file with a simple command line application in it. It also allows to view a list of task based on their status. The project was built according to [roadmap.sh](https://roadmap.sh/projects/task-tracker).

## Features

- Add: Add a new task with a description and a default status of "todo",
- List: View tasks based on their status (todo, in progress, done, or all).
- Update: Update the description of an existing task based on their ID.
- Mark: Change the status of a task into "in progress" or "done" based on their ID.
- Delete: Remove an existing task based on their ID.

## Usage

### List Tasks

To list tasks, use `list` argument. You can optionally specify the status ('todo', "done", "in-progress"):

```bash
python3 task-cli.py list
python3 task-cli.py list todo # to print tasks with status 'todo'
python3 task-cli.py list in-progress # to print tasks with status 'in-progress'
python3 task-cli.py list done # to print tasks with status 'done'
```

### Add Task

To add a new task, use `add` argument:

```bash
python3 task-cli.py add "Buy groceries"
```

### Delete Task

To delete a specific task, use `delete` argument with specified `id`:

```bash
python3 task-cli.py delete 2
```

### Update Task

To update a specific task, use `update` argument with specified `id` and `description`:

```bash
python3 task-cli.py update 2 "Do chores"
```

### Mark Task Status

To mark task status, use either `mark-in-progress` or `mark-done` argument with specified `id`:

```bash
python3 task-cli.py mark-in-progress 5 # to change the status to "in-progress"
python3 task-cli.py mark-done 1 # to change the status to "done"
```
