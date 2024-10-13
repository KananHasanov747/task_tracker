import os
import argparse
import json
import time

now = time.strftime("%Y-%m-%d %I:%M:%S%p", time.localtime())

parser = argparse.ArgumentParser(
    prog="Task Tracker",
    description="Track and manage your tasks",
)

# 'action' argument
subparsers = parser.add_subparsers(
    dest="action",
    help="Action to be performed (list, add, update, delete, mark-in-progress, mark-done)",
)

# 'list' action
parser_list = subparsers.add_parser("list", help="List tasks")
parser_list.add_argument(
    "status",
    nargs="?",
    choices=["todo", "in-progress", "done"],
    help="Task status (optional)",
)

# 'add' action
parser_add = subparsers.add_parser("add", help="Add task")
parser_add.add_argument("description", help="Description of the task")

# 'update' action
parser_update = subparsers.add_parser("update", help="Update task")
parser_update.add_argument("id", help="Task ID to update")
parser_update.add_argument("description", help="New description for the task")

# 'delete' action
parser_delete = subparsers.add_parser("delete", help="Delete a task")
parser_delete.add_argument("id", help="Task ID to delete")

# 'make-in-progress' action
parser_mark_in_progress = subparsers.add_parser(
    "mark-in-progress", help="Mark a task as in progress"
)
parser_mark_in_progress.add_argument("id", help="Task ID to mark as in progress")

# 'mark-done' action
parser_mark_done = subparsers.add_parser("mark-done", help="Mark a task as done")
parser_mark_done.add_argument("id", help="Task ID to mark as done")

args = parser.parse_args()


def skeleton(
    id: int, description: str, status: str, createdAt: str, updatedAt: str
) -> dict:
    return {
        "id": id,  # A unique identifier for the task
        "description": description,  # A short description of the task
        "status": status,  # The status of the task (todo, in-progress, done)
        "createdAt": createdAt,  # The date and time when the task was created
        "updatedAt": updatedAt,  # The date and time when the task was last updated
    }


def fileDump(data: list, f):
    f.seek(0)  # move the pointer to the beginning line
    json.dump(data, f, indent=2)
    f.truncate()  # truncate the file to remove any leftover data


def task_list(status: str):
    try:
        with open(
            "data.json", mode="r", encoding="utf-8"
        ) as f:  # opens the file for reading
            data = json.load(f)
            if status:
                print(list(filter(lambda _: _["status"] == args.status, data)))
            else:
                print(json.dumps(data, indent=2))
    except FileNotFoundError:
        raise


def task_add(description: str):
    if not os.path.exists("data.json"):
        with open("data.json", mode="w", encoding="utf-8") as f:
            pass

    with open("data.json", mode="r+", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = []

        task = skeleton(
            len(data) + 1,
            description,
            "todo",
            now,
            now,
        )
        print(json.dumps(task, indent=2))

        data.append(task)
        fileDump(data, f)


def task_delete(id):
    with open("data.json", mode="r+", encoding="utf-8") as f:
        data = json.load(f)
        print(json.dumps(data.pop(int(id) - 1), indent=2))
        for _ in range(int(id) - 1, len(data)):
            data[_]["id"] -= 1

        fileDump(data, f)


def __task_modify(action, id, description=None):
    try:
        with open(
            "data.json", mode="r+", encoding="utf-8"
        ) as f:  # opens the file for reading & writing
            data = json.load(f)
            if id.isalnum():
                _filter = (
                    tuple(filter(lambda _: str(_[1]["id"]) == id, enumerate(data)))[0]
                    or None
                )

                if _filter:
                    index, task = _filter
                else:
                    raise Exception("Task with such ID not found")

                if action.startswith("mark"):
                    task["status"] = action.replace("mark-", "")
                else:  # args.action == "update"
                    task["description"] = description
                    task["updatedAt"] = now

                print(json.dumps(task, indent=2))
                data[index] = task
                fileDump(data, f)
            else:
                raise Exception("'id' is not an integer")

    except FileNotFoundError:
        raise


def task_update(id, description):
    return __task_modify("update", id, description)


def task_mark_in_progress(id):
    return __task_modify("mark-in-progress", id)


def task_mark_done(id):
    return __task_modify("mark-done", id)


if __name__ == "__main__":

    if args.action == "list":
        task_list(args.status)

    elif args.action == "add":
        task_add(args.description)

    elif args.action == "delete":
        task_delete(args.id)

    elif args.action == "mark-in-progress":
        task_mark_in_progress(args.id)

    elif args.action == "mark-done":
        task_mark_done(args.id)

    else:  # update
        task_update(args.id, args.description)
