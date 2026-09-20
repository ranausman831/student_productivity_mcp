import json
from pathlib import Path

from fastmcp import FastMCP

mcp = FastMCP("Student Productivity MCP")

DATA_FILE = Path("productivity.json")


# =========================
# Helper Functions
# =========================

def load_data():
    if not DATA_FILE.exists():
        return {
            "notes": [],
            "tasks": [],
            "resources": []
        }

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def get_next_id(items):
    return max(
        (item["id"] for item in items),
        default=0
    ) + 1


# ============================================================
# NOTES
# ============================================================

@mcp.tool
def add_note(text: str) -> str:
    """Add a new student note."""

    data = load_data()

    note = {
        "id": get_next_id(data["notes"]),
        "text": text
    }

    data["notes"].append(note)
    save_data(data)

    return f"Note added successfully. ID: {note['id']}"


@mcp.tool
def get_notes() -> list:
    """Get all student notes."""

    data = load_data()
    return data["notes"]


@mcp.tool
def get_note(note_id: int) -> dict:
    """Get a specific note by ID."""

    data = load_data()

    for note in data["notes"]:
        if note["id"] == note_id:
            return note

    return {
        "error": f"Note with ID {note_id} not found."
    }


@mcp.tool
def update_note(note_id: int, new_text: str) -> str:
    """Update an existing note."""

    data = load_data()

    for note in data["notes"]:
        if note["id"] == note_id:
            note["text"] = new_text
            save_data(data)

            return f"Note {note_id} updated successfully."

    return f"Note {note_id} not found."


@mcp.tool
def delete_note(note_id: int) -> str:
    """Delete a note by ID."""

    data = load_data()

    for note in data["notes"]:
        if note["id"] == note_id:
            data["notes"].remove(note)
            save_data(data)

            return f"Note {note_id} deleted successfully."

    return f"Note {note_id} not found."


# ============================================================
# TASKS
# ============================================================

@mcp.tool
def add_task(
    title: str,
    priority: str = "medium",
    deadline: str = ""
) -> str:
    """Add a new student task."""

    data = load_data()

    task = {
        "id": get_next_id(data["tasks"]),
        "title": title,
        "priority": priority,
        "deadline": deadline,
        "status": "pending"
    }

    data["tasks"].append(task)
    save_data(data)

    return f"Task added successfully. ID: {task['id']}"


@mcp.tool
def get_tasks() -> list:
    """Get all student tasks."""

    data = load_data()
    return data["tasks"]


@mcp.tool
def get_task(task_id: int) -> dict:
    """Get a specific task by ID."""

    data = load_data()

    for task in data["tasks"]:
        if task["id"] == task_id:
            return task

    return {
        "error": f"Task with ID {task_id} not found."
    }


@mcp.tool
def update_task(
    task_id: int,
    title: str = "",
    priority: str = "",
    deadline: str = "",
    status: str = ""
) -> str:
    """Update an existing task."""

    data = load_data()

    for task in data["tasks"]:
        if task["id"] == task_id:

            if title:
                task["title"] = title

            if priority:
                task["priority"] = priority

            if deadline:
                task["deadline"] = deadline

            if status:
                task["status"] = status

            save_data(data)

            return f"Task {task_id} updated successfully."

    return f"Task {task_id} not found."


@mcp.tool
def delete_task(task_id: int) -> str:
    """Delete a task by ID."""

    data = load_data()

    for task in data["tasks"]:
        if task["id"] == task_id:
            data["tasks"].remove(task)
            save_data(data)

            return f"Task {task_id} deleted successfully."

    return f"Task {task_id} not found."


@mcp.tool
def complete_task(task_id: int) -> str:
    """Mark a task as completed."""

    data = load_data()

    for task in data["tasks"]:
        if task["id"] == task_id:
            task["status"] = "completed"
            save_data(data)

            return f"Task {task_id} marked as completed."

    return f"Task {task_id} not found."


# ============================================================
# RESOURCES
# ============================================================

@mcp.tool
def add_resource(
    title: str,
    url: str,
    category: str = "general"
) -> str:
    """Save a useful student resource or learning link."""

    data = load_data()

    resource = {
        "id": get_next_id(data["resources"]),
        "title": title,
        "url": url,
        "category": category
    }

    data["resources"].append(resource)
    save_data(data)

    return f"Resource added successfully. ID: {resource['id']}"


@mcp.tool
def get_resources() -> list:
    """Get all saved resources."""

    data = load_data()
    return data["resources"]


@mcp.tool
def update_resource(
    resource_id: int,
    title: str = "",
    url: str = "",
    category: str = ""
) -> str:
    """Update a saved resource."""

    data = load_data()

    for resource in data["resources"]:
        if resource["id"] == resource_id:

            if title:
                resource["title"] = title

            if url:
                resource["url"] = url

            if category:
                resource["category"] = category

            save_data(data)

            return f"Resource {resource_id} updated successfully."

    return f"Resource {resource_id} not found."


@mcp.tool
def delete_resource(resource_id: int) -> str:
    """Delete a saved resource."""

    data = load_data()

    for resource in data["resources"]:
        if resource["id"] == resource_id:
            data["resources"].remove(resource)
            save_data(data)

            return f"Resource {resource_id} deleted successfully."

    return f"Resource {resource_id} not found."


# ============================================================
# SEARCH
# ============================================================

@mcp.tool
def search_productivity(query: str) -> dict:
    """Search across notes, tasks, and resources."""

    data = load_data()

    query = query.lower()

    matching_notes = [
        note for note in data["notes"]
        if query in note["text"].lower()
    ]

    matching_tasks = [
        task for task in data["tasks"]
        if (
            query in task["title"].lower()
            or query in task["priority"].lower()
            or query in task["status"].lower()
            or query in task["deadline"].lower()
        )
    ]

    matching_resources = [
        resource for resource in data["resources"]
        if (
            query in resource["title"].lower()
            or query in resource["url"].lower()
            or query in resource["category"].lower()
        )
    ]

    return {
        "query": query,
        "notes": matching_notes,
        "tasks": matching_tasks,
        "resources": matching_resources
    }


# ============================================================
# START SERVER
# ============================================================

if __name__ == "__main__":
    mcp.run()