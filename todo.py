import json
from datetime import datetime
from typing import List, Dict, Tuple

DEFAULT_FILENAME = "tasks.json"
PRIORITY_LEVELS = ("low", "medium", "high")


def now_str() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def load_tasks(filename: str = DEFAULT_FILENAME) -> List[Dict]:
    """Load tasks from a JSON file. If file missing or invalid, return empty list."""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            tasks = json.load(f)
            if isinstance(tasks, list):
                return tasks
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f"Warning: could not load tasks ({e})")
    return []


def save_tasks(tasks: List[Dict], filename: str = DEFAULT_FILENAME) -> None:
    """Save tasks list to JSON file."""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(tasks, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error saving tasks: {e}")


def next_id(tasks: List[Dict]) -> int:
    """Compute the next available integer id."""
    if not tasks:
        return 1
    return max(task.get("id", 0) for task in tasks) + 1


def add_task(tasks: List[Dict], title: str, description: str = "", priority: str = "medium") -> Dict:
    """Create a new task dict and append it to tasks."""
    priority = priority.lower()
    if priority not in PRIORITY_LEVELS:
        priority = "medium"
    task = {
        "id": next_id(tasks),
        "title": title.strip(),
        "description": description.strip(),
        "priority": priority,
        "completed": False,
        "created_at": now_str(),
    }
    tasks.append(task)
    return task


def find_task(tasks: List[Dict], task_id: int) -> Tuple[int, Dict]:
    """Return (index, task) for given id, or (-1, None) if not found."""
    for i, t in enumerate(tasks):
        if t.get("id") == task_id:
            return i, t
    return -1, None


def remove_task(tasks: List[Dict], task_id: int) -> bool:
    """Remove task by id. Return True if removed."""
    idx, _ = find_task(tasks, task_id)
    if idx >= 0:
        tasks.pop(idx)
        return True
    return False


def mark_completed(tasks: List[Dict], task_id: int) -> bool:
    """Mark a task completed by id. Return True if changed."""
    _, t = find_task(tasks, task_id)
    if t and not t["completed"]:
        t["completed"] = True
        t["completed_at"] = now_str()
        return True
    return False


def change_priority(tasks: List[Dict], task_id: int, new_priority: str) -> bool:
    new_priority = new_priority.lower()
    if new_priority not in PRIORITY_LEVELS:
        return False
    _, t = find_task(tasks, task_id)
    if t:
        t["priority"] = new_priority
        return True
    return False


def sort_key_priority(task: Dict) -> int:
    """Mapping: high -> 3, medium -> 2, low -> 1"""
    mapping = {"low": 1, "medium": 2, "high": 3}
    return mapping.get(task.get("priority", "medium"), 2)


def view_tasks(tasks: List[Dict], filter_by: str = "all", sort_by_priority: bool = False) -> None:
    """
    Print tasks in a simple table.
    filter_by: "all", "pending", "completed"
    """
    filtered = []
    for t in tasks:
        if filter_by == "pending" and t.get("completed"):
            continue
        if filter_by == "completed" and not t.get("completed"):
            continue
        filtered.append(t)

    if sort_by_priority:
        filtered.sort(key=lambda x: (-sort_key_priority(x), x.get("created_at")))

    if not filtered:
        print("No tasks to show.")
        return

    # header
    header = f"{'ID':>3} | {'Title':30} | {'Priority':7} | {'Status':9} | {'Created At':19}"
    print(header)
    print("-" * len(header))
    for t in filtered:
        id_str = str(t["id"]).rjust(3)
        title = (t["title"][:27] + "...") if len(t["title"]) > 30 else t["title"].ljust(30)
        priority = t.get("priority", "medium").ljust(7)
        status = "Done" if t.get("completed") else "Pending"
        created = t.get("created_at", "")
        print(f"{id_str} | {title} | {priority} | {status:9} | {created}")


def input_priority(prompt: str = "Priority (low/medium/high) [medium]: ") -> str:
    p = input(prompt).strip().lower()
    if p == "":
        return "medium"
    return p if p in PRIORITY_LEVELS else "medium"


def main():
    tasks = load_tasks()
    print("Welcome, Agent. Your secure To-Do manager is ready.")
    while True:
        print("\nChoose an action:")
        print(" 1. Add task")
        print(" 2. Remove task")
        print(" 3. View tasks")
        print(" 4. Mark task completed")
        print(" 5. Change task priority")
        print(" 6. Save tasks now")
        print(" 0. Quit")
        choice = input("> ").strip()

        if choice == "1":
            title = input("Title (required): ").strip()
            if not title:
                print("Cannot add a task without a title.")
                continue
            desc = input("Description (optional): ").strip()
            pr = input_priority()
            task = add_task(tasks, title, desc, pr)
            save_tasks(tasks)
            print(f"Added task #{task['id']}: {task['title']} (priority: {task['priority']})")

        elif choice == "2":
            try:
                tid = int(input("Enter task id to remove: ").strip())
            except ValueError:
                print("Invalid id.")
                continue
            if remove_task(tasks, tid):
                save_tasks(tasks)
                print(f"Removed task #{tid}.")
            else:
                print(f"No task with id {tid} found.")

        elif choice == "3":
            sub = input("Show (a)ll / (p)ending / (c)ompleted ? [a]: ").strip().lower() or "a"
            mapping = {"a": "all", "p": "pending", "c": "completed"}
            filter_by = mapping.get(sub, "all")
            sort_choice = input("Sort by priority? (y/N): ").strip().lower()
            view_tasks(tasks, filter_by=filter_by, sort_by_priority=(sort_choice == "y"))

        elif choice == "4":
            try:
                tid = int(input("Enter task id to mark completed: ").strip())
            except ValueError:
                print("Invalid id.")
                continue
            if mark_completed(tasks, tid):
                save_tasks(tasks)
                print(f"Task #{tid} marked completed.")
            else:
                print(f"Could not mark task #{tid} (maybe it doesn't exist or is already completed).")

        elif choice == "5":
            try:
                tid = int(input("Task id to change priority: ").strip())
            except ValueError:
                print("Invalid id.")
                continue
            newp = input_priority("New priority (low/medium/high): ")
            if change_priority(tasks, tid, newp):
                save_tasks(tasks)
                print(f"Task #{tid} priority changed to {newp}.")
            else:
                print("Failed to change priority (invalid id or priority).")

        elif choice == "6":
            save_tasks(tasks)
            print("Tasks saved.")
        elif choice == "0":
            save_tasks(tasks)
            print("Good work, Agent — changes saved. Goodbye.")
            break
        else:
            print("Unknown choice. Try again.")


if __name__ == "__main__":
    main()
