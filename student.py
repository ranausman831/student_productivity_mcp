
from fastmcp import FastMCP

mcp = FastMCP("Student Productivity MCP")


# =========================
# In-Memory Storage
# =========================

data = {
    "notes": [],
    "tasks": [],
    "resources": []
}


# =========================
# Helper Functions
# =========================

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

    note = {
        "id": get_next_id(data["notes"]),
        "text": text
    }

    data["notes"].append(note)

    return f"Note added successfully. ID: {note['id']}"


@mcp.tool
def get_notes() -> list:
    """Get all student notes."""

    return data["notes"]


@mcp.tool
def get_note(note_id: int) -> dict:
    """Get a specific note by ID."""

    for note in data["notes"]:
        if note["id"] == note_id:
            return note

    return {
        "error": f"Note with ID {note_id} not found."
    }


@mcp.tool
def update_note(note_id: int, new_text: str) -> str:
    """Update an existing note."""

    for note in data["notes"]:
        if note["id"] == note_id:
            note["text"] = new_text

            return f"Note {note_id} updated successfully."

    return f"Note {note_id} not found."


@mcp.tool
def delete_note(note_id: int) -> str:
    """Delete a note by ID."""

    for note in data["notes"]:
        if note["id"] == note_id:
            data["notes"].remove(note)

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

    task = {
        "id": get_next_id(data["tasks"]),
        "title": title,
        "priority": priority,
        "deadline": deadline,
        "status": "pending"
    }

    data["tasks"].append(task)

    return f"Task added successfully. ID: {task['id']}"


@mcp.tool
def get_tasks() -> list:
    """Get all student tasks."""

    return data["tasks"]


@mcp.tool
def get_task(task_id: int) -> dict:
    """Get a specific task by ID."""

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

            return f"Task {task_id} updated successfully."

    return f"Task {task_id} not found."


@mcp.tool
def delete_task(task_id: int) -> str:
    """Delete a task by ID."""

    for task in data["tasks"]:
        if task["id"] == task_id:
            data["tasks"].remove(task)

            return f"Task {task_id} deleted successfully."

    return f"Task {task_id} not found."


@mcp.tool
def complete_task(task_id: int) -> str:
    """Mark a task as completed."""

    for task in data["tasks"]:
        if task["id"] == task_id:
            task["status"] = "completed"

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

    resource = {
        "id": get_next_id(data["resources"]),
        "title": title,
        "url": url,
        "category": category
    }

    data["resources"].append(resource)

    return f"Resource added successfully. ID: {resource['id']}"


@mcp.tool
def get_resources() -> list:
    """Get all saved resources."""

    return data["resources"]


@mcp.tool
def update_resource(
    resource_id: int,
    title: str = "",
    url: str = "",
    category: str = ""
) -> str:
    """Update a saved resource."""

    for resource in data["resources"]:
        if resource["id"] == resource_id:

            if title:
                resource["title"] = title

            if url:
                resource["url"] = url

            if category:
                resource["category"] = category

            return f"Resource {resource_id} updated successfully."

    return f"Resource {resource_id} not found."


@mcp.tool
def delete_resource(resource_id: int) -> str:
    """Delete a saved resource."""

    for resource in data["resources"]:
        if resource["id"] == resource_id:
            data["resources"].remove(resource)

            return f"Resource {resource_id} deleted successfully."

    return f"Resource {resource_id} not found."


# ============================================================
# SEARCH
# ============================================================

@mcp.tool
def search_productivity(query: str) -> dict:
    """Search across notes, tasks, and resources."""

    query = query.lower()

    matching_notes = [
        note
        for note in data["notes"]
        if query in note["text"].lower()
    ]

    matching_tasks = [
        task
        for task in data["tasks"]
        if (
            query in task["title"].lower()
            or query in task["priority"].lower()
            or query in task["status"].lower()
            or query in task["deadline"].lower()
        )
    ]

    matching_resources = [
        resource
        for resource in data["resources"]
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

