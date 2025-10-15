from flask import Flask, request, jsonify
from controllers.task_controller import TaskController
from model.task import STATUS_TODO, STATUS_IN_PROGRESS, STATUS_DONE

app = Flask(__name__)
controller = TaskController()

@app.get("/health")
def health():
    return {"status": "ok"}, 200

@app.get("/tasks")
def list_tasks():
    status = request.args.get("status")
    tasks = controller.display(status=status)
    return jsonify([t.to_dict() for t in tasks]), 200

@app.post("/tasks")
def add_task():
    data = request.get_json(silent=True) or {}
    title = (data.get("title") or "").strip()
    notes = data.get("notes")
    if not title:
        return {"error": "title is required"}, 400
    t = controller.add(title=title, notes=notes)
    return jsonify(t.to_dict()), 201

@app.patch("/tasks/<task_id>")
def update_task(task_id):
    data = request.get_json(silent=True) or {}
    updated = controller.update(
        task_id=task_id,
        title=data.get("title"),
        notes=data.get("notes"),
        status=data.get("status"),
    )
    if not updated:
        return {"error": "task not found or invalid status"}, 404
    tasks = controller.display()
    for t in tasks:
        if t.id == task_id:
            return jsonify(t.to_dict()), 200
    return {"error": "task not found"}, 404

@app.delete("/tasks/<task_id>")
def delete_task(task_id):
    ok = controller.delete(task_id)
    return ({"deleted": True}, 200) if ok else ({"error": "task not found"}, 404)

@app.delete("/tasks")
def clear_tasks():
    controller.clear()
    return {"cleared": True}, 200

@app.post("/tasks/<task_id>/start")
def start_task(task_id):
    t = controller.set_status(task_id, STATUS_IN_PROGRESS)
    return (jsonify(t.to_dict()), 200) if t else ({"error": "task not found"}, 404)

@app.post("/tasks/<task_id>/done")
def done_task(task_id):
    t = controller.set_status(task_id, STATUS_DONE)
    return (jsonify(t.to_dict()), 200) if t else ({"error": "task not found"}, 404)

if __name__ == "__main__":
    app.run(debug=True)
