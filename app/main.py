# app/main.py
# Fathima Sarah - 2026-03-09
from flask import Flask, request, jsonify
from app.models import User, Task
from app.utils import (
    validate_email,
    calculate_priority_score,
    sanitize_input,
    get_days_until_due,
)

app = Flask(__name__)

# In-memory storage (for simplicity)
users = {}
tasks = {}
task_counter = 0

# ============================================
# EXISTING ENDPOINTS (DO NOT MODIFY)
# ============================================

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy", "version": "1.0.0"})


@app.route("/users", methods=["POST"])
def create_user():
    """Create a new user"""
    data = request.get_json()

    if not data or "email" not in data or "name" not in data:
        return jsonify({"error": "Missing required fields: email, name"}), 400

    email = data["email"]
    name = data["name"]

    # Validate email
    if not validate_email(email):
        return jsonify({"error": "Invalid email format"}), 400

    # Check if user exists
    if email in users:
        return jsonify({"error": "User already exists"}), 409

    user = User(email=email, name=name)
    users[email] = user

    return jsonify(user.to_dict()), 201


@app.route("/users/<email>", methods=["GET"])
def get_user(email):
    """Get user by email"""
    if email not in users:
        return jsonify({"error": "User not found"}), 404
    return jsonify(users[email].to_dict())


# ============================================
# TASK 2: ADD YOUR NEW ENDPOINT BELOW
# ============================================

ALLOWED_PRIORITIES = {"low", "medium", "high", "critical"}
ALLOWED_STATUSES = {"pending", "in_progress", "completed"}
ALLOWED_SORT_FIELDS = {"priority_score", "due_date", "created_at"}


def _task_priority_score(task):
    if task.due_date:
        days_until_due = get_days_until_due(task.due_date)
    else:
        days_until_due = 36500
    return calculate_priority_score(task.priority, days_until_due)


@app.route("/tasks", methods=["POST"])
def create_task():
    """Create a new task"""
    global task_counter
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    required = ["title", "user_email", "priority"]
    for field in required:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    title = sanitize_input(data["title"])
    user_email = data["user_email"]
    priority = data["priority"]
    description = sanitize_input(data.get("description", ""))

    if not isinstance(title, str) or not title.strip():
        return jsonify({"error": "Invalid field: title"}), 400

    if not isinstance(user_email, str) or not validate_email(user_email):
        return jsonify({"error": "Invalid field: user_email"}), 400

    if priority not in ALLOWED_PRIORITIES:
        return jsonify({"error": "Invalid field: priority"}), 400

    if user_email not in users:
        return jsonify({"error": "User not found"}), 404

    task_counter += 1
    task = Task(
        id=task_counter,
        title=title,
        description=description,
        user_email=user_email,
        priority=priority,
        status="pending",
    )
    tasks[task_counter] = task
    return jsonify(task.to_dict()), 201


@app.route("/tasks", methods=["GET"])
def list_tasks():
    """List tasks with optional filtering and sorting"""
    filtered_tasks = list(tasks.values())

    user_email = request.args.get("user_email")
    status = request.args.get("status")
    priority = request.args.get("priority")
    sort_by = request.args.get("sort_by")
    sort_order = request.args.get("sort_order", "asc")

    if user_email:
        filtered_tasks = [task for task in filtered_tasks if task.user_email == user_email]

    if status:
        if status not in ALLOWED_STATUSES:
            return jsonify({"error": "Invalid status filter"}), 400
        filtered_tasks = [task for task in filtered_tasks if task.status == status]

    if priority:
        if priority not in ALLOWED_PRIORITIES:
            return jsonify({"error": "Invalid priority filter"}), 400
        filtered_tasks = [task for task in filtered_tasks if task.priority == priority]

    if sort_by:
        if sort_by not in ALLOWED_SORT_FIELDS:
            return jsonify({"error": "Invalid sort field"}), 400

        if sort_order not in {"asc", "desc"}:
            return jsonify({"error": "Invalid sort_order"}), 400

        reverse = sort_order == "desc"

        if sort_by == "priority_score":
            filtered_tasks.sort(key=_task_priority_score, reverse=reverse)
        elif sort_by == "due_date":
            filtered_tasks.sort(
                key=lambda task: (task.due_date is None, task.due_date or ""),
                reverse=reverse,
            )
        elif sort_by == "created_at":
            filtered_tasks.sort(key=lambda task: task.created_at, reverse=reverse)

    return jsonify([task.to_dict() for task in filtered_tasks])


if __name__ == "__main__":
    app.run(debug=True, port=5000)
